"""
Mapping Parser Module
Parses CSV mapping documents and extracts transformation rules
"""
import pandas as pd
from typing import List, Dict, Any


class MappingParser:
    """Parse ETL mapping documents from CSV files"""
    
    def __init__(self, csv_path: str):
        """
        Initialize the parser with a CSV file path
        
        Args:
            csv_path: Path to the CSV mapping document
        """
        self.csv_path = csv_path
        self.mappings = []
        
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse the CSV or Excel file and extract mapping information
        
        Returns:
            List of mapping dictionaries
        """
        try:
            # Read CSV or Excel file based on extension
            if self.csv_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(self.csv_path)
            else:
                df = pd.read_csv(self.csv_path)
            
            # Clean column names (strip whitespace)
            df.columns = df.columns.str.strip()
            
            # Convert DataFrame to list of dictionaries
            self.mappings = df.to_dict('records')
            
            # Clean up NaN values
            for mapping in self.mappings:
                for key, value in mapping.items():
                    if pd.isna(value):
                        mapping[key] = None
            
            return self.mappings
            
        except Exception as e:
            raise ValueError(f"Error parsing file: {str(e)}")
    
    def get_source_columns(self) -> List[str]:
        """Get list of unique source columns"""
        columns = set()
        for mapping in self.mappings:
            if mapping.get('source_column'):
                columns.add(mapping['source_column'])
        return sorted(list(columns))
    
    def get_target_columns(self) -> List[str]:
        """Get list of unique target columns"""
        columns = set()
        for mapping in self.mappings:
            if mapping.get('target_column'):
                columns.add(mapping['target_column'])
        return sorted(list(columns))
    
    def get_transformations(self) -> Dict[str, str]:
        """Get mapping of target columns to their transformations"""
        transformations = {}
        for mapping in self.mappings:
            target = mapping.get('target_column')
            transformation = mapping.get('transformation')
            if target and transformation:
                transformations[target] = transformation
        return transformations
    
    def extract_source_tables(self) -> List[str]:
        """
        Extract unique source table names from transformations
        
        Returns:
            List of unique source table names found in transformations
        """
        import re
        tables = set()
        
        for mapping in self.mappings:
            transformation = mapping.get('transformation', '')
            if transformation and isinstance(transformation, str):
                # Match patterns like "table_name.column_name"
                # This regex finds words followed by a dot (table references)
                matches = re.findall(r'(\w+)\.', transformation)
                tables.update(matches)
        
        return sorted(list(tables))
