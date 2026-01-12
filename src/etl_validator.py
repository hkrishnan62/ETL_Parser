"""
ETL Validator Module
Main orchestrator for ETL mapping validation
"""
from typing import Dict, Any
from .mapping_parser import MappingParser
from .sql_generator import SQLGenerator


class ETLValidator:
    """Main class for ETL validation workflow"""
    
    def __init__(self, csv_path: str):
        """
        Initialize ETL validator
        
        Args:
            csv_path: Path to CSV mapping document
        """
        self.csv_path = csv_path
        self.parser = MappingParser(csv_path)
        self.mappings = []
        self.generator = None
        
    def load_mappings(self) -> None:
        """Load and parse mapping document"""
        self.mappings = self.parser.parse()
        self.generator = SQLGenerator(self.mappings)
        
    def generate_validation_queries(self,
                                   source_table: str,
                                   target_table: str,
                                   source_schema: str = None,
                                   target_schema: str = None,
                                   query_type: str = 'both') -> Dict[str, str]:
        """
        Generate validation queries
        
        Args:
            source_table: Source table name
            target_table: Target table name
            source_schema: Optional source schema name
            target_schema: Optional target schema name
            query_type: Type of query - 'both', 'source_minus_target', or 'target_minus_source'
            
        Returns:
            Dictionary with generated queries
        """
        if not self.generator:
            raise ValueError("Mappings not loaded. Call load_mappings() first.")
        
        queries = {}
        
        if query_type in ['both', 'source_minus_target']:
            queries['source_minus_target'] = self.generator.generate_source_minus_target(
                source_table, target_table, source_schema, target_schema
            )
        
        if query_type in ['both', 'target_minus_source']:
            queries['target_minus_source'] = self.generator.generate_target_minus_source(
                source_table, target_table, source_schema, target_schema
            )
        
        if query_type == 'both':
            queries['complete'] = self.generator.generate_complete_validation(
                source_table, target_table, source_schema, target_schema
            )
        
        return queries
    
    def get_mapping_summary(self) -> Dict[str, Any]:
        """
        Get summary of loaded mappings
        
        Returns:
            Dictionary with mapping statistics
        """
        if not self.mappings:
            return {}
        
        # Extract source tables from transformations
        source_tables = self.parser.extract_source_tables()
        
        return {
            'total_mappings': len(self.mappings),
            'source_columns': self.parser.get_source_columns(),
            'target_columns': self.parser.get_target_columns(),
            'transformations': self.parser.get_transformations(),
            'detected_source_tables': source_tables
        }
