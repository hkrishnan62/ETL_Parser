"""
Mapping Parser Module
Parses CSV mapping documents and extracts transformation rules
"""
import pandas as pd
from typing import List, Dict, Any


class MappingParser:
    """Parse ETL mapping documents from CSV files"""
    
    # Required columns for a valid mapping file
    REQUIRED_COLUMNS = {'source_column', 'target_column', 'transformation'}
    
    def __init__(self, csv_path: str):
        """
        Initialize the parser with a CSV file path
        
        Args:
            csv_path: Path to the CSV mapping document
        """
        self.csv_path = csv_path
        self.mappings = []
        
    def validate_format(self, df: pd.DataFrame) -> tuple[bool, str]:
        """
        Validate if the DataFrame has the expected format
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if DataFrame is empty
        if df.empty:
            return False, "❌ File is empty. Please provide a mapping file with data."
        
        # Clean and normalize column names
        df.columns = df.columns.str.strip().str.lower()
        
        # Get available columns
        available_columns = set(df.columns)
        
        # Check for missing required columns
        missing_columns = self.REQUIRED_COLUMNS - available_columns
        if missing_columns:
            missing_str = ', '.join(sorted(missing_columns))
            available_str = ', '.join(sorted(available_columns)) if available_columns else "none"
            return False, f"❌ Missing required columns: {missing_str}\n\n📋 Expected columns: source_column, target_column, transformation\n\n📊 Found columns: {available_str}"
        
        # Check if all required columns have at least some data
        for col in self.REQUIRED_COLUMNS:
            non_null_count = df[col].notna().sum()
            if non_null_count == 0:
                return False, f"❌ Column '{col}' is empty. All required columns must have at least some data."
        
        # Warn if there are rows with missing critical data
        empty_rows = 0
        for idx, row in df.iterrows():
            if pd.isna(row.get('source_column')) or pd.isna(row.get('target_column')) or pd.isna(row.get('transformation')):
                empty_rows += 1
        
        if empty_rows > 0:
            return False, f"❌ Found {empty_rows} row(s) with missing required data (source_column, target_column, or transformation). Please fill in all required fields."
        
        return True, ""
        
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse the CSV or Excel file and extract mapping information
        
        Returns:
            List of mapping dictionaries
            
        Raises:
            ValueError: If file format is invalid
        """
        try:
            # Read CSV or Excel file based on extension
            if self.csv_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(self.csv_path)
            else:
                df = pd.read_csv(self.csv_path)
            
            # Validate format
            is_valid, error_message = self.validate_format(df)
            if not is_valid:
                raise ValueError(error_message)
            
            # Clean column names (strip whitespace and lowercase)
            df.columns = df.columns.str.strip().str.lower()
            
            # Convert DataFrame to list of dictionaries
            self.mappings = df.to_dict('records')
            
            # Clean up NaN values
            for mapping in self.mappings:
                for key, value in mapping.items():
                    if pd.isna(value):
                        mapping[key] = None
            
            return self.mappings
            
        except ValueError as e:
            # Re-raise validation errors as-is
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"❌ Error parsing file: {str(e)}")
    
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
