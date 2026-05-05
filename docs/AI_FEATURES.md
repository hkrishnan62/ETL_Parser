# 🤖 AI-Powered ETL Parser - Features & Setup

## Overview

The ETL Parser now includes powerful AI capabilities using OpenAI's GPT models to provide intelligent assistance with ETL mappings, transformations, and SQL query optimization.

## 🎯 AI Features

### 1. **Intelligent Transformation Suggestions**
Get AI-powered suggestions for SQL transformations based on column names and data types.

**Example:**
```python
from src.ai_enhanced_validator import AIEnhancedValidator

validator = AIEnhancedValidator()
suggestion = validator.suggest_transformation(
    source_column='phone_number',
    target_column='contact_phone',
    source_type='VARCHAR',
    target_type='VARCHAR'
)

print(suggestion['transformation'])
# Output: REGEXP_REPLACE(source_table.phone_number, '[^0-9]', '')
print(suggestion['explanation'])
# Output: Remove all non-numeric characters from phone number
```

### 2. **Natural Language to SQL Mapping**
Describe your ETL mapping in plain English, and AI generates the complete mapping CSV.

**Example:**
```python
validator = AIEnhancedValidator()
mappings = validator.generate_from_description(
    "Map customer ID as key, combine first and last name into full_name, "
    "convert email to lowercase, extract year from order_date"
)

# Returns structured mappings ready to use
```

### 3. **SQL Query Optimization**
Automatically optimize generated SQL queries for your specific database.

**Example:**
```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

result = validator.generate_with_optimization(
    source_table='orders',
    target_table='orders_fact',
    database_type='postgres',
    query_type='both'
)

# Get optimized queries
optimized_sql = result['optimized_queries']['source_minus_target']
notes = result['optimization_notes']
```

### 4. **Mapping Quality Analysis**
AI analyzes your mapping document and provides quality assessment with recommendations.

**Example:**
```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

analysis = validator.analyze_mapping_quality()

print(analysis['quality_score'])  # excellent/good/fair/poor
print(analysis['issues'])         # List of potential problems
print(analysis['recommendations']) # Suggestions for improvement
```

### 5. **Transformation Explanations**
Convert technical SQL transformations into plain English explanations.

**Example:**
```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

explanations = validator.explain_transformations()

# Returns: {
#   'full_name': 'Combines first and last name with a space between them',
#   'email_clean': 'Converts email to lowercase for consistency',
#   ...
# }
```

### 6. **Syntax Validation**
Validate transformation syntax for your specific database dialect.

**Example:**
```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

validation = validator.validate_transformation_syntax(database_type='postgres')

for result in validation:
    if not result['valid']:
        print(f"Issue in {result['target_column']}: {result['issues']}")
```

## 🔧 Setup & Configuration

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `langchain` - LangChain framework
- `python-dotenv` - Environment variable management

### Step 2: Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
AI_MODEL=gpt-4
AI_TEMPERATURE=0.3
ENABLE_AI_FEATURES=true
```

### Step 3: Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Alternative: Azure OpenAI

If using Azure OpenAI:

```env
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AI_MODEL=gpt-4
```

## 💻 Usage

### Web Interface

1. Start the application:
```bash
python app.py
```

2. Open http://localhost:5000

3. Enable AI features:
   - Check "🤖 Use AI Optimization & Analysis"
   - Upload your CSV mapping
   - Select database type
   - Generate queries with AI optimization

4. Use AI tools:
   - **"Get AI Transformation Suggestion"** - Get suggestions for individual transformations
   - **"Generate Mapping from Description"** - Create mappings from natural language

### Command Line Interface

```python
from src.ai_enhanced_validator import AIEnhancedValidator

# Initialize with AI features
validator = AIEnhancedValidator('examples/sample_mapping.csv')
validator.load_mappings()

# Check if AI is available
if validator.is_ai_available():
    print("AI features enabled!")
else:
    print("AI not available - configure OPENAI_API_KEY")

# Get comprehensive analysis
analysis = validator.get_comprehensive_analysis(database_type='postgres')
print(analysis['quality_analysis'])
print(analysis['transformation_explanations'])

# Generate optimized queries
result = validator.generate_with_optimization(
    source_table='customers',
    target_table='dim_customer',
    database_type='postgres'
)

print(result['optimized_queries']['complete'])
```

## 📊 AI Feature Examples

### Example 1: Smart Transformation Suggestions

```python
# Input: Column names and types
validator.suggest_transformation(
    source_column='customer_email',
    target_column='email_address',
    source_type='VARCHAR(255)',
    target_type='VARCHAR(255)'
)

# Output:
{
    'transformation': 'LOWER(TRIM(source_table.customer_email))',
    'explanation': 'Converts email to lowercase and removes whitespace for standardization',
    'confidence': 'high',
    'ai_generated': True
}
```

### Example 2: Natural Language Mapping Generation

```python
description = """
I need to map a customer table where:
- customer_id should be the primary key
- Combine fname and lname into full_name
- Convert email to lowercase
- Parse date_of_birth to extract age
- Map status code: A=Active, I=Inactive, D=Deleted
"""

mappings = validator.generate_from_description(description)

# Generates complete CSV mapping structure
```

### Example 3: Query Optimization

```python
# Original query
original_query = """
SELECT * FROM source_table st
LEFT JOIN target_table tt ON st.id = tt.id
WHERE tt.id IS NULL
"""

# Optimize for PostgreSQL
optimization = validator.ai_agent.optimize_query(
    original_query,
    database_type='postgres'
)

print(optimization['optimized_query'])
print(optimization['suggestions'])
# Suggestions: Use indexes on id columns, consider EXCEPT operator, etc.
```

## 🎓 Best Practices

### 1. API Usage Optimization

```python
# Configure temperature for different use cases
# Lower temperature (0.1-0.3) for factual, consistent results
# Higher temperature (0.5-0.8) for creative suggestions

os.environ['AI_TEMPERATURE'] = '0.2'  # For transformations
os.environ['AI_TEMPERATURE'] = '0.5'  # For explanations
```

### 2. Cost Management

```python
# AI features can be toggled per request
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

# Generate without AI (free)
basic_queries = validator.generate_validation_queries(...)

# Generate with AI (uses API credits)
ai_queries = validator.generate_with_optimization(...)
```

### 3. Batch Processing

```python
# For multiple mappings, batch your requests
descriptions = [
    "Map customer data...",
    "Map order data...",
    "Map product data..."
]

for desc in descriptions:
    mappings = validator.generate_from_description(desc)
    # Process each mapping
```

## 🔍 Feature Availability Matrix

| Feature | Free (No API Key) | With OpenAI API | Notes |
|---------|------------------|-----------------|-------|
| Basic SQL Generation | ✅ | ✅ | Always available |
| CSV Parsing | ✅ | ✅ | Always available |
| Transformation Suggestions | ❌ | ✅ | Requires API |
| Query Optimization | ❌ | ✅ | Requires API |
| NL to Mapping | ❌ | ✅ | Requires API |
| Quality Analysis | ❌ | ✅ | Requires API |
| Syntax Validation | ❌ | ✅ | Requires API |
| Plain English Explanations | ❌ | ✅ | Requires API |

## 🛡️ Error Handling

The AI agent gracefully degrades when API is unavailable:

```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

# Always check availability
if validator.is_ai_available():
    # Use AI features
    result = validator.analyze_mapping_quality()
else:
    # Fallback to basic features
    result = validator.get_mapping_summary()
```

## 📈 Performance Considerations

- **Response Time**: AI features add 2-10 seconds per request
- **API Costs**: GPT-4 costs ~$0.03-0.06 per 1K tokens
- **Caching**: Consider caching AI responses for repeated queries
- **Rate Limits**: OpenAI has rate limits (check your tier)

## 🔐 Security

- Never commit `.env` file with API keys
- Use environment variables for production
- Rotate API keys regularly
- Monitor usage in OpenAI dashboard

## 🐛 Troubleshooting

### Issue: "AI features not available"
**Solution**: 
1. Check `.env` file exists
2. Verify `OPENAI_API_KEY` is set
3. Ensure `ENABLE_AI_FEATURES=true`
4. Restart the application

### Issue: "API rate limit exceeded"
**Solution**: 
1. Wait for rate limit reset
2. Upgrade OpenAI plan
3. Implement request throttling

### Issue: "Invalid API key"
**Solution**: 
1. Regenerate key in OpenAI dashboard
2. Update `.env` file
3. Restart application

## 📚 Advanced Usage

### Custom AI Models

```python
import os
os.environ['AI_MODEL'] = 'gpt-4-turbo-preview'  # Use latest model
os.environ['AI_MODEL'] = 'gpt-3.5-turbo'        # Use faster/cheaper model
```

### Fine-tuning Parameters

```python
os.environ['AI_TEMPERATURE'] = '0.1'  # More deterministic
os.environ['AI_MAX_TOKENS'] = '3000'  # Longer responses
```

## 🎉 Summary

The AI-enhanced ETL Parser provides:
- ✅ Intelligent transformation suggestions
- ✅ Natural language mapping generation  
- ✅ SQL query optimization
- ✅ Quality analysis and recommendations
- ✅ Plain English explanations
- ✅ Syntax validation
- ✅ Graceful degradation without API key

All AI features are **optional** - the base functionality works without any API keys!

---

**Ready to get started?** Configure your API key and enable AI features in the web interface!
