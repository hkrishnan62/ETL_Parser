"""
AI Agent Module for ETL Mapping Intelligence
Provides AI-powered features for transformation suggestions, optimization, and validation
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if OpenAI is available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


class AIAgent:
    """AI Agent for intelligent ETL mapping assistance"""
    
    def __init__(self):
        """Initialize AI agent with API credentials"""
        self.enabled = os.getenv('ENABLE_AI_FEATURES', 'false').lower() == 'true'
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if self.enabled and OPENAI_AVAILABLE and self.api_key:
            openai.api_key = self.api_key
            self.model = os.getenv('AI_MODEL', 'gpt-4')
            self.temperature = float(os.getenv('AI_TEMPERATURE', '0.3'))
            self.max_tokens = int(os.getenv('AI_MAX_TOKENS', '2000'))
        else:
            self.enabled = False
    
    def is_available(self) -> bool:
        """Check if AI features are available"""
        return self.enabled and OPENAI_AVAILABLE and self.api_key is not None
    
    def suggest_transformation(self, source_column: str, target_column: str, 
                              source_type: str = None, target_type: str = None,
                              sample_data: List[str] = None) -> Dict[str, Any]:
        """
        Suggest SQL transformation based on column names and types
        
        Args:
            source_column: Source column name
            target_column: Target column name
            source_type: Source data type (optional)
            target_type: Target data type (optional)
            sample_data: Sample source values (optional)
            
        Returns:
            Dictionary with transformation suggestion and explanation
        """
        if not self.is_available():
            return {
                'transformation': f'source_table.{source_column}',
                'explanation': 'AI suggestions not available (API key not configured)',
                'confidence': 'low',
                'ai_generated': False
            }
        
        try:
            # Build context
            context = f"""
Source Column: {source_column} {f'({source_type})' if source_type else ''}
Target Column: {target_column} {f'({target_type})' if target_type else ''}
"""
            if sample_data:
                context += f"\nSample Data: {', '.join(str(s) for s in sample_data[:5])}"
            
            # Create prompt
            prompt = f"""You are an expert ETL developer. Based on the column information below, suggest an appropriate SQL transformation.

{context}

Provide a SQL transformation expression that:
1. Properly maps the source column to target column
2. Handles data type conversions if needed
3. Applies appropriate string cleaning, formatting, or calculations
4. Uses standard SQL functions

Respond in JSON format:
{{
    "transformation": "SQL expression here (use source_table prefix)",
    "explanation": "Brief explanation of the transformation",
    "confidence": "high/medium/low"
}}

Example transformations:
- String concatenation: CONCAT(source_table.first_name, ' ', source_table.last_name)
- Case conversion: UPPER(TRIM(source_table.column))
- Type casting: CAST(source_table.column AS DATE)
- CASE statements for status mapping
"""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert ETL developer specializing in data transformations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            result['ai_generated'] = True
            return result
            
        except Exception as e:
            return {
                'transformation': f'source_table.{source_column}',
                'explanation': f'Error generating suggestion: {str(e)}',
                'confidence': 'low',
                'ai_generated': False
            }
    
    def optimize_query(self, sql_query: str, database_type: str = 'generic') -> Dict[str, Any]:
        """
        Analyze and optimize generated SQL query
        
        Args:
            sql_query: SQL query to optimize
            database_type: Target database (postgres, mysql, oracle, etc.)
            
        Returns:
            Dictionary with optimized query and suggestions
        """
        if not self.is_available():
            return {
                'optimized_query': sql_query,
                'suggestions': ['AI optimization not available'],
                'improvements': []
            }
        
        try:
            prompt = f"""Analyze this SQL validation query and provide optimization suggestions for {database_type} database.

Query:
{sql_query}

Provide analysis in JSON format:
{{
    "optimized_query": "Optimized version of the query",
    "suggestions": ["List of optimization suggestions"],
    "improvements": ["Specific improvements made"],
    "performance_notes": "Expected performance improvements"
}}

Consider:
1. Index usage and JOIN optimization
2. CTE efficiency
3. EXCEPT vs LEFT JOIN performance
4. Database-specific optimizations
5. Query readability and maintainability
"""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a database performance expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                'optimized_query': sql_query,
                'suggestions': [f'Error: {str(e)}'],
                'improvements': []
            }
    
    def generate_mapping_from_description(self, description: str) -> List[Dict[str, str]]:
        """
        Generate mapping CSV from natural language description
        
        Args:
            description: Natural language description of the mapping
            
        Returns:
            List of mapping dictionaries
        """
        if not self.is_available():
            return []
        
        try:
            prompt = f"""Convert this natural language ETL mapping description into a structured CSV mapping.

Description:
{description}

Generate a JSON array of mappings with this structure:
[
    {{
        "source_column": "column_name",
        "target_column": "target_name",
        "transformation": "SQL transformation expression",
        "is_key": "TRUE or FALSE"
    }}
]

Example:
Input: "Map customer ID directly, combine first and last name into full_name, convert email to lowercase"
Output: [
    {{"source_column": "customer_id", "target_column": "customer_id", "transformation": "source_table.customer_id", "is_key": "TRUE"}},
    {{"source_column": "first_name", "target_column": "full_name", "transformation": "CONCAT(source_table.first_name, ' ', source_table.last_name)", "is_key": "FALSE"}},
    {{"source_column": "email", "target_column": "email", "transformation": "LOWER(source_table.email)", "is_key": "FALSE"}}
]
"""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an ETL mapping expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating mapping: {str(e)}")
            return []
    
    def analyze_mapping_quality(self, mappings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze mapping quality and provide recommendations
        
        Args:
            mappings: List of mapping dictionaries
            
        Returns:
            Analysis results with recommendations
        """
        if not self.is_available():
            return {
                'quality_score': 'unknown',
                'issues': ['AI analysis not available'],
                'recommendations': []
            }
        
        try:
            mappings_str = '\n'.join([
                f"- {m.get('source_column', 'N/A')} -> {m.get('target_column', 'N/A')}: {m.get('transformation', 'direct')}"
                for m in mappings[:20]  # Limit to first 20
            ])
            
            prompt = f"""Analyze this ETL mapping for quality, completeness, and potential issues.

Mappings:
{mappings_str}

Total mappings: {len(mappings)}

Provide analysis in JSON format:
{{
    "quality_score": "excellent/good/fair/poor",
    "issues": ["List of potential issues or concerns"],
    "recommendations": ["List of improvement recommendations"],
    "strengths": ["Positive aspects of the mapping"],
    "risk_assessment": "Overall risk level and explanation"
}}

Check for:
1. Missing key columns
2. Potential data type mismatches
3. Complex transformations that might fail
4. NULL handling
5. Performance concerns
6. Best practices adherence
"""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an ETL quality assurance expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                'quality_score': 'unknown',
                'issues': [f'Error: {str(e)}'],
                'recommendations': []
            }
    
    def explain_transformation(self, transformation: str) -> str:
        """
        Explain a SQL transformation in plain English
        
        Args:
            transformation: SQL transformation expression
            
        Returns:
            Plain English explanation
        """
        if not self.is_available():
            return "AI explanation not available"
        
        try:
            prompt = f"""Explain this SQL transformation in simple, plain English that a business user can understand:

{transformation}

Provide a clear, concise explanation without technical jargon.
"""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical translator explaining SQL to business users."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def validate_transformation_syntax(self, transformation: str, 
                                      database_type: str = 'generic') -> Dict[str, Any]:
        """
        Validate SQL transformation syntax
        
        Args:
            transformation: SQL transformation to validate
            database_type: Target database type
            
        Returns:
            Validation results
        """
        if not self.is_available():
            return {
                'valid': True,
                'issues': [],
                'warnings': ['AI validation not available']
            }
        
        try:
            prompt = f"""Validate this SQL transformation for {database_type} database:

{transformation}

Check for:
1. Syntax errors
2. Function compatibility with {database_type}
3. Common mistakes
4. Potential runtime issues

Respond in JSON format:
{{
    "valid": true/false,
    "issues": ["List of errors or problems"],
    "warnings": ["List of warnings or suggestions"],
    "corrected_version": "Corrected SQL if there are issues"
}}
"""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a {database_type} SQL expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=1000
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                'valid': True,
                'issues': [],
                'warnings': [f'Validation error: {str(e)}']
            }


# Singleton instance
_ai_agent = None

def get_ai_agent() -> AIAgent:
    """Get singleton AI agent instance"""
    global _ai_agent
    if _ai_agent is None:
        _ai_agent = AIAgent()
    return _ai_agent
