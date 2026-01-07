"""
AI-Enhanced ETL Validator
Extends base validator with AI-powered features
"""
from typing import Dict, Any, List
from .etl_validator import ETLValidator
from .ai_agent import get_ai_agent


class AIEnhancedValidator(ETLValidator):
    """ETL Validator with AI capabilities"""
    
    def __init__(self, csv_path: str = None):
        """
        Initialize AI-enhanced validator
        
        Args:
            csv_path: Path to CSV mapping document (optional)
        """
        if csv_path:
            super().__init__(csv_path)
        else:
            self.csv_path = None
            self.mappings = []
            self.parser = None
            self.generator = None
        
        self.ai_agent = get_ai_agent()
    
    def is_ai_available(self) -> bool:
        """Check if AI features are available"""
        return self.ai_agent.is_available()
    
    def suggest_transformation(self, source_column: str, target_column: str,
                              source_type: str = None, target_type: str = None) -> Dict[str, Any]:
        """
        Get AI-powered transformation suggestion
        
        Args:
            source_column: Source column name
            target_column: Target column name
            source_type: Source data type (optional)
            target_type: Target data type (optional)
            
        Returns:
            Transformation suggestion with explanation
        """
        return self.ai_agent.suggest_transformation(
            source_column, target_column, source_type, target_type
        )
    
    def analyze_mapping_quality(self) -> Dict[str, Any]:
        """
        Analyze loaded mapping quality using AI
        
        Returns:
            Quality analysis with recommendations
        """
        if not self.mappings:
            return {
                'quality_score': 'unknown',
                'issues': ['No mappings loaded'],
                'recommendations': ['Load a mapping file first']
            }
        
        return self.ai_agent.analyze_mapping_quality(self.mappings)
    
    def optimize_generated_query(self, query: str, database_type: str = 'generic') -> Dict[str, Any]:
        """
        Optimize a generated SQL query using AI
        
        Args:
            query: SQL query to optimize
            database_type: Target database type
            
        Returns:
            Optimization results
        """
        return self.ai_agent.optimize_query(query, database_type)
    
    def explain_transformations(self) -> Dict[str, str]:
        """
        Get plain English explanations for all transformations
        
        Returns:
            Dictionary mapping target columns to explanations
        """
        if not self.mappings:
            return {}
        
        explanations = {}
        for mapping in self.mappings:
            target = mapping.get('target_column')
            transformation = mapping.get('transformation')
            
            if target and transformation:
                explanations[target] = self.ai_agent.explain_transformation(transformation)
        
        return explanations
    
    def validate_transformation_syntax(self, database_type: str = 'generic') -> List[Dict[str, Any]]:
        """
        Validate all transformation syntax using AI
        
        Args:
            database_type: Target database type
            
        Returns:
            List of validation results for each transformation
        """
        if not self.mappings:
            return []
        
        results = []
        for mapping in self.mappings:
            transformation = mapping.get('transformation')
            target_col = mapping.get('target_column')
            
            if transformation and transformation.strip():
                validation = self.ai_agent.validate_transformation_syntax(
                    transformation, database_type
                )
                validation['target_column'] = target_col
                validation['transformation'] = transformation
                results.append(validation)
        
        return results
    
    def generate_from_description(self, description: str) -> List[Dict[str, str]]:
        """
        Generate mapping from natural language description
        
        Args:
            description: Natural language description of mapping
            
        Returns:
            List of generated mappings
        """
        return self.ai_agent.generate_mapping_from_description(description)
    
    def get_comprehensive_analysis(self, database_type: str = 'generic') -> Dict[str, Any]:
        """
        Get comprehensive AI analysis of the mapping
        
        Args:
            database_type: Target database type
            
        Returns:
            Complete analysis including quality, validation, and explanations
        """
        if not self.mappings:
            return {
                'error': 'No mappings loaded',
                'ai_available': self.is_ai_available()
            }
        
        analysis = {
            'ai_available': self.is_ai_available(),
            'mapping_summary': self.get_mapping_summary(),
        }
        
        if self.is_ai_available():
            analysis['quality_analysis'] = self.analyze_mapping_quality()
            analysis['syntax_validation'] = self.validate_transformation_syntax(database_type)
            analysis['transformation_explanations'] = self.explain_transformations()
        else:
            analysis['ai_message'] = 'AI features not available. Set OPENAI_API_KEY to enable.'
        
        return analysis
    
    def generate_with_optimization(self,
                                   source_table: str,
                                   target_table: str,
                                   source_schema: str = None,
                                   target_schema: str = None,
                                   database_type: str = 'generic',
                                   query_type: str = 'both') -> Dict[str, Any]:
        """
        Generate validation queries with AI optimization
        
        Args:
            source_table: Source table name
            target_table: Target table name
            source_schema: Optional source schema name
            target_schema: Optional target schema name
            database_type: Target database type
            query_type: Type of query to generate
            
        Returns:
            Dictionary with queries and AI optimizations
        """
        # Generate base queries
        queries = self.generate_validation_queries(
            source_table, target_table, source_schema, target_schema, query_type
        )
        
        result = {
            'original_queries': queries,
            'ai_available': self.is_ai_available()
        }
        
        # Add AI optimizations if available
        if self.is_ai_available():
            result['optimized_queries'] = {}
            result['optimization_notes'] = {}
            
            for query_name, query_sql in queries.items():
                optimization = self.optimize_generated_query(query_sql, database_type)
                result['optimized_queries'][query_name] = optimization.get('optimized_query', query_sql)
                result['optimization_notes'][query_name] = {
                    'suggestions': optimization.get('suggestions', []),
                    'improvements': optimization.get('improvements', []),
                    'performance_notes': optimization.get('performance_notes', '')
                }
        
        return result
