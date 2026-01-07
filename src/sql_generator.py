"""
SQL Generator Module
Generates validation SQL queries from mapping definitions
"""
from typing import List, Dict, Any
import re


class SQLGenerator:
    """Generate SQL validation queries from ETL mappings"""
    
    def __init__(self, mappings: List[Dict[str, Any]]):
        """
        Initialize SQL generator with parsed mappings
        
        Args:
            mappings: List of mapping dictionaries from MappingParser
        """
        self.mappings = mappings
        
    def _clean_transformation(self, transformation: str) -> str:
        """
        Clean and prepare transformation expression for SQL
        
        Args:
            transformation: Transformation expression from mapping
            
        Returns:
            Cleaned SQL expression
        """
        if not transformation:
            return ""
        
        # Remove extra whitespace
        transformation = ' '.join(transformation.split())
        
        return transformation
    
    def _build_select_clause(self, source_table: str, target_table: str) -> str:
        """
        Build SELECT clause with transformations
        
        Args:
            source_table: Source table name
            target_table: Target table name
            
        Returns:
            SELECT clause as string
        """
        select_items = []
        
        for mapping in self.mappings:
            target_col = mapping.get('target_column')
            source_col = mapping.get('source_column')
            transformation = mapping.get('transformation')
            
            if not target_col:
                continue
            
            # If transformation exists, use it
            if transformation and transformation.strip():
                transformed_expr = self._clean_transformation(transformation)
                select_items.append(f"    {transformed_expr} AS {target_col}")
            # Otherwise, use direct mapping
            elif source_col:
                select_items.append(f"    {source_table}.{source_col} AS {target_col}")
            else:
                # If neither transformation nor source column, use NULL
                select_items.append(f"    NULL AS {target_col}")
        
        return ",\n".join(select_items)
    
    def _get_join_keys(self) -> List[str]:
        """
        Extract join keys from mappings
        
        Returns:
            List of join key column names
        """
        join_keys = []
        
        for mapping in self.mappings:
            if mapping.get('is_key') or mapping.get('join_key'):
                key_col = mapping.get('target_column') or mapping.get('source_column')
                if key_col:
                    join_keys.append(key_col)
        
        # If no explicit keys, use first column as default
        if not join_keys and self.mappings:
            first_col = self.mappings[0].get('target_column') or self.mappings[0].get('source_column')
            if first_col:
                join_keys.append(first_col)
        
        return join_keys
    
    def generate_source_minus_target(self, 
                                     source_table: str, 
                                     target_table: str,
                                     source_schema: str = None,
                                     target_schema: str = None) -> str:
        """
        Generate Source MINUS Target validation query
        
        Args:
            source_table: Source table name
            target_table: Target table name
            source_schema: Optional source schema name
            target_schema: Optional target schema name
            
        Returns:
            SQL query as string
        """
        # Build full table names with schema if provided
        source_full = f"{source_schema}.{source_table}" if source_schema else source_table
        target_full = f"{target_schema}.{target_table}" if target_schema else target_table
        
        # Build SELECT clause with transformations
        select_clause = self._build_select_clause(source_table, target_table)
        
        # Get join keys
        join_keys = self._get_join_keys()
        
        query = f"""-- Source MINUS Target Validation Query
-- This query shows records that exist in source but not in target after transformation

WITH source_transformed AS (
  SELECT
{select_clause}
  FROM {source_full} {source_table}
),
target_data AS (
  SELECT *
  FROM {target_full}
)
SELECT 
  'SOURCE_MINUS_TARGET' AS validation_type,
  COUNT(*) AS record_count
FROM (
  SELECT * FROM source_transformed
  EXCEPT
  SELECT * FROM target_data
) diff
UNION ALL
SELECT 
  'DETAIL' AS validation_type,
  NULL AS record_count
FROM (
  SELECT * FROM source_transformed
  EXCEPT
  SELECT * FROM target_data
) diff
LIMIT 100;  -- Show first 100 discrepancies

-- Alternative using LEFT JOIN for databases that don't support EXCEPT:
/*
SELECT 
  s.*,
  'Missing in Target' AS issue
FROM source_transformed s
LEFT JOIN target_data t
  ON {self._generate_join_condition('s', 't', join_keys)}
WHERE t.{join_keys[0] if join_keys else 'id'} IS NULL;
*/
"""
        return query
    
    def generate_target_minus_source(self, 
                                     source_table: str, 
                                     target_table: str,
                                     source_schema: str = None,
                                     target_schema: str = None) -> str:
        """
        Generate Target MINUS Source validation query
        
        Args:
            source_table: Source table name
            target_table: Target table name
            source_schema: Optional source schema name
            target_schema: Optional target schema name
            
        Returns:
            SQL query as string
        """
        # Build full table names with schema if provided
        source_full = f"{source_schema}.{source_table}" if source_schema else source_table
        target_full = f"{target_schema}.{target_table}" if target_schema else target_table
        
        # Build SELECT clause with transformations
        select_clause = self._build_select_clause(source_table, target_table)
        
        # Get join keys
        join_keys = self._get_join_keys()
        
        query = f"""-- Target MINUS Source Validation Query
-- This query shows records that exist in target but not in transformed source

WITH source_transformed AS (
  SELECT
{select_clause}
  FROM {source_full} {source_table}
),
target_data AS (
  SELECT *
  FROM {target_full}
)
SELECT 
  'TARGET_MINUS_SOURCE' AS validation_type,
  COUNT(*) AS record_count
FROM (
  SELECT * FROM target_data
  EXCEPT
  SELECT * FROM source_transformed
) diff
UNION ALL
SELECT 
  'DETAIL' AS validation_type,
  NULL AS record_count
FROM (
  SELECT * FROM target_data
  EXCEPT
  SELECT * FROM source_transformed
) diff
LIMIT 100;  -- Show first 100 discrepancies

-- Alternative using LEFT JOIN for databases that don't support EXCEPT:
/*
SELECT 
  t.*,
  'Missing in Source' AS issue
FROM target_data t
LEFT JOIN source_transformed s
  ON {self._generate_join_condition('t', 's', join_keys)}
WHERE s.{join_keys[0] if join_keys else 'id'} IS NULL;
*/
"""
        return query
    
    def _generate_join_condition(self, alias1: str, alias2: str, keys: List[str]) -> str:
        """
        Generate JOIN condition from key columns
        
        Args:
            alias1: First table alias
            alias2: Second table alias
            keys: List of key column names
            
        Returns:
            JOIN condition string
        """
        if not keys:
            return "1=1"
        
        conditions = [f"{alias1}.{key} = {alias2}.{key}" for key in keys]
        return " AND ".join(conditions)
    
    def generate_complete_validation(self,
                                     source_table: str,
                                     target_table: str,
                                     source_schema: str = None,
                                     target_schema: str = None) -> str:
        """
        Generate complete validation query (both directions)
        
        Args:
            source_table: Source table name
            target_table: Target table name
            source_schema: Optional source schema name
            target_schema: Optional target schema name
            
        Returns:
            Combined SQL query as string
        """
        source_minus_target = self.generate_source_minus_target(
            source_table, target_table, source_schema, target_schema
        )
        target_minus_source = self.generate_target_minus_source(
            source_table, target_table, source_schema, target_schema
        )
        
        query = f"""-- Complete Bidirectional Validation Query
-- Generated from ETL Mapping Document

{source_minus_target}

-- ========================================

{target_minus_source}
"""
        return query
