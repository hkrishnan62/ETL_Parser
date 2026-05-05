# ETL Mapping Validator

A Python-based application that converts SQL mapping documents into transformation validation SQL queries for ETL (Extract, Transform, Load) processes.

## Statement of need

Data engineering teams already maintain mapping specifications as CSV or Excel workbooks, but validation SQL is still often written by hand for every source-to-target rule. That manual step is slow, inconsistent, and difficult to review at scale across large migrations and warehouse projects. This project closes that gap by converting structured mapping documents into repeatable SQL validation queries and related testing artifacts.

## 🚀 Features

### Core Features
- **CSV and Excel Mapping Parser**: Upload `.csv`, `.xlsx`, or `.xls` files containing ETL mapping definitions
- **Complex Transformation Support**: Handles SQL transformations including:
  - CONCAT operations
  - CASE statements
  - Type casting
  - String functions (UPPER, LOWER, TRIM)
  - Regular expressions
  - Mathematical operations
- **Bidirectional Validation**: Generates both Source → Target and Target → Source validation queries
- **Web Interface**: User-friendly Flask-based web application
- **CLI Support**: Command-line interface for automation

### 🧪 NEW: Test Case Generation
- **Automated Test Case Creation**: Generate comprehensive test cases for your ETL mappings
- **Positive & Negative Scenarios**: Covers both successful transformations and error handling
- **Multiple Export Formats**: Export to qTest, Zephyr, TestRail, Azure DevOps (ADO), or JSON
- **Preview Before Download**: Review generated test cases in the browser
- **Comprehensive Coverage**: Includes data validation, NULL handling, data type tests, and more
- **Time-Saving**: Generate dozens of test cases in seconds

> 🎯 **See Documentation**: [Test Case Generation Guide](docs/TEST_CASE_GENERATION_GUIDE.md)
> Perfect for QA teams, data engineers, and anyone testing ETL processes!

### 🎮 Interactive SQL Playground
- **Live SQL Editor**: Write and execute SQL queries with syntax highlighting
- **Sample Data**: Pre-loaded customers and orders tables for testing
- **Instant Results**: See query results in real-time with formatted tables
- **Share Queries**: Generate shareable links for queries and results
- **6 Sample Queries**: Learn from pre-built examples (JOINs, aggregations, ETL transformations)
- **Schema Browser**: View table structures while writing queries
- **Safe Execution**: Sandboxed environment with read-only access

> 🎯 **Try it now**: [Launch SQL Playground](https://etl-mapping-converter-to-sql.onrender.com/playground/)
> Perfect for testing transformations, learning SQL, and sharing query examples!

### 🤖 AI-Powered Features
- **Intelligent Transformation Suggestions**: Get AI-recommended SQL transformations based on column names and types
- **Natural Language Mapping Generation**: Describe your ETL mapping in plain English, AI generates the CSV
- **SQL Query Optimization**: Automatically optimize generated queries for your database
- **Mapping Quality Analysis**: AI analyzes your mappings and provides recommendations
- **Plain English Explanations**: Convert technical SQL into business-friendly explanations
- **Syntax Validation**: Validate transformation syntax for different database dialects

> 💡 **AI features are optional** - the application works fully without them. Configure OpenAI API key to enable.
> See [AI features documentation](docs/AI_FEATURES.md) for detailed setup and usage notes.

## 📋 Requirements

- Python 3.8+
- Flask 3.0.0
- Pandas 2.1.4
- Werkzeug 3.0.1

## 🔧 Installation

### For Users (Quick Setup)

```bash
# Clone the repository
git clone https://github.com/hkrishnan62/ETL_Parser.git
cd ETL_Parser

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser to: https://etl-mapping-converter-to-sql.onrender.com (or http://localhost:5000 for local)
```

That's it! The application works immediately.

### For Developers

1. Clone the repository:
```bash
git clone https://github.com/hkrishnan62/ETL_Parser.git
cd ETL_Parser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **(Optional) Enable AI Features:**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
# ENABLE_AI_FEATURES=true
```

> Without AI configuration, all core features work normally. AI features gracefully degrade to basic functionality.

### Docker Deployment

```bash
# Clone and run with Docker
git clone https://github.com/hkrishnan62/ETL_Parser.git
cd ETL_Parser

# (Optional) Configure AI
cp .env.example .env

# Run
docker-compose up -d

# Access at: https://etl-mapping-converter-to-sql.onrender.com (or http://localhost:5000 for local)
```

### Desktop Application (Installable App)

Want to run this as a **native desktop application**?

```bash
# Install desktop dependencies
pip install -r desktop_requirements.txt

# Run as desktop app
python desktop_app.py
```

**Build standalone executable for distribution:**
```bash
python build_desktop_app.py
```

This creates an installable desktop app (`.exe` for Windows, `.app` for macOS) that users can run without Python!

📖 See [Desktop quick start](docs/DESKTOP_QUICK_START.md) for details.

### Sharing with Others

See [Deployment guide](docs/DEPLOYMENT_GUIDE.md) for complete deployment options including:
- **Desktop App** - Installable executables (Windows/Mac/Linux)
- GitHub sharing
- Docker containers
- Cloud deployment (Heroku, AWS, Azure)
- Standalone executables
- Shared server setup

## 🎯 Usage

### Web Interface

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
https://etl-mapping-converter-to-sql.onrender.com (Production)
http://localhost:5000 (Local development)
```

The Render deployment is currently live. Because it runs on the Render free tier, the first request after inactivity can take 30-60 seconds while the service wakes up.

3. Upload your CSV or Excel mapping document and configure:
   - Source table name
   - Target table name
   - Source schema (optional)
   - Target schema (optional)
   - Database type (for AI optimization)
   - Query type (both, source-minus-target, or target-minus-source)
   - **NEW:** Enable AI features checkbox

4. Click "Generate SQL Queries" to create validation queries

5. **NEW:** Use AI Tools:
   - **"Get AI Transformation Suggestion"**: Get smart transformation recommendations
   - **"Generate Mapping from Description"**: Create mappings from natural language

### Command Line Interface

**Basic Usage:**
```python
from src.etl_validator import ETLValidator

# Initialize validator
validator = ETLValidator('path/to/mapping.csv')  # or path/to/mapping.xlsx

# Load mappings
validator.load_mappings()

# Generate queries
queries = validator.generate_validation_queries(
    source_table='source_table',
    target_table='target_table',
    source_schema='source_db',
    target_schema='target_db',
    query_type='both'
)

# Access generated queries
print(queries['source_minus_target'])
print(queries['target_minus_source'])
```

**With AI Features:**
```python
from src.ai_enhanced_validator import AIEnhancedValidator

# Initialize AI-enhanced validator
validator = AIEnhancedValidator('path/to/mapping.csv')
validator.load_mappings()

# Check if AI is available
if validator.is_ai_available():
    print("AI features enabled!")
    
    # Get quality analysis
    analysis = validator.analyze_mapping_quality()
    print(analysis['quality_score'])
    print(analysis['recommendations'])
    
    # Generate with optimization
    result = validator.generate_with_optimization(
        source_table='orders',
        target_table='orders_fact',
        database_type='postgres'
    )
    
    print(result['optimized_queries']['complete'])
else:
    print("Using basic features (AI not configured)")
    queries = validator.generate_validation_queries(...)
```

## 📄 Mapping File Format

Your CSV or Excel mapping file should contain the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| `source_column` | Source column name | Yes |
| `target_column` | Target column name | Yes |
| `transformation` | SQL transformation expression | No |
| `is_key` | Whether column is a join key (TRUE/FALSE) | No |

### Example Mapping File:

```csv
source_column,target_column,transformation,is_key
customer_id,customer_id,source_table.customer_id,TRUE
first_name,full_name,"CONCAT(source_table.first_name, ' ', source_table.last_name)",FALSE
email,email_address,LOWER(TRIM(source_table.email)),FALSE
status,status_code,"CASE WHEN source_table.status = 'A' THEN 'ACTIVE' ELSE 'INACTIVE' END",FALSE
```

## 🔍 Generated Query Types

### 1. Source MINUS Target
Identifies records that exist in the source (after transformation) but are missing in the target table.

### 2. Target MINUS Source
Identifies records that exist in the target but are missing in the transformed source.

### 3. Complete Validation
Combines both queries for comprehensive bidirectional validation.

## 📁 Project Structure

```
ETL_Parser/
├── app.py                      # Flask web application
├── requirements.txt            # Python dependencies
├── src/
│   ├── __init__.py
│   ├── mapping_parser.py       # CSV parsing logic
│   ├── sql_generator.py        # SQL query generation
│   └── etl_validator.py        # Main orchestrator
├── templates/
│   └── index.html              # Web interface
├── examples/
│   └── sample_mapping.csv      # Example mapping file
├── example_usage.py            # CLI usage example
└── README.md
```

## 🎨 Supported Transformations

The application supports various SQL transformations including:

- **String Functions**: CONCAT, UPPER, LOWER, TRIM, SUBSTRING, REGEXP_REPLACE
- **Date Functions**: CAST, DATE_FORMAT, DATEDIFF
- **Conditional Logic**: CASE WHEN statements
- **Mathematical**: ROUND, FLOOR, CEIL, arithmetic operations
- **Type Conversions**: CAST, CONVERT
- **Aggregations**: SUM, AVG, COUNT (with appropriate grouping)

## 🛠️ Example Output

For a given mapping, the tool generates SQL queries like:

```sql
-- Source MINUS Target Validation Query
WITH source_transformed AS (
  SELECT
    source_table.customer_id AS customer_id,
    CONCAT(source_table.first_name, ' ', source_table.last_name) AS full_name,
    LOWER(TRIM(source_table.email)) AS email_address
  FROM source_db.customers source_table
),
target_data AS (
  SELECT * FROM target_db.customers_dim
)
SELECT 
  'SOURCE_MINUS_TARGET' AS validation_type,
  COUNT(*) AS record_count
FROM (
  SELECT * FROM source_transformed
  EXCEPT
  SELECT * FROM target_data
) diff;
```

## 🧪 Testing

Run the example script to test the functionality:

```bash
# Basic functionality test
python example_usage.py

# AI features demonstration (optional - requires API key)
python ai_demo.py

# Automated test suite
pytest tests/
```

This will:
1. Load the sample mapping CSV
2. Generate validation queries
3. Save queries to the `output/` directory
4. (If AI enabled) Show AI-powered features

## 📚 Documentation

- **[README.md](README.md)** - This file (main documentation)
- **[docs/QUICK_START.md](docs/QUICK_START.md)** - Quick start guide
- **[docs/SQL_PLAYGROUND.md](docs/SQL_PLAYGROUND.md)** - SQL Playground guide and API reference
- **[docs/COMPLETE_GUIDE.md](docs/COMPLETE_GUIDE.md)** - Comprehensive usage guide
- **[docs/AI_FEATURES.md](docs/AI_FEATURES.md)** - AI features documentation and setup
- **[docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Project overview
- **Example Scripts:**
  - `example_usage.py` - Basic CLI usage
  - `ai_demo.py` - AI features demonstration
  - `demo.py` - Full feature showcase

## 🤝 Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for issue reporting, pull request workflow, code style, and test instructions. Please also review [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 📝 License

This project is licensed under the MIT License.

## 🔗 Use Cases

- **ETL Testing**: Validate data transformations in ETL pipelines
- **Data Migration**: Verify data accuracy after migration
- **Data Quality**: Continuous monitoring of data quality
- **Reconciliation**: Compare source and target datasets
- **Audit**: Generate audit trails for data transformations

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

Made with ❤️ for Data Engineers