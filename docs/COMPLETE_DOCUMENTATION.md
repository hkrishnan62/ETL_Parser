# ETL Mapping Validator - Complete Documentation

**Table of Contents:**
1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [CSV Mapping Format](#csv-mapping-format)
7. [Generated Query Types](#generated-query-types)
8. [Architecture](#architecture)
9. [AI Features](#ai-features)
10. [Desktop Application](#desktop-application)
11. [Deployment](#deployment)
12. [Database Testing](#database-testing)
13. [Troubleshooting](#troubleshooting)
14. [Google Indexing Guide](#google-indexing-guide)

---

## Project Overview

### What This Application Does

This application **automatically converts ETL mapping documents (CSV files) into SQL validation queries** that can be used to verify data transformations between source and target systems.

### The Problem It Solves

In ETL processes, you need to validate that:
1. All data from source made it to target (with transformations applied)
2. No extra data exists in target that shouldn't be there
3. Transformations were applied correctly

Traditionally, writing these validation queries manually is:
- ⏰ Time-consuming
- 🐛 Error-prone
- 🔄 Repetitive for each mapping change

### The Solution

Upload a CSV mapping document → Get production-ready SQL validation queries instantly!

---

## Quick Start

### 3 Steps to Start Using

**Step 1: Clone or Download**
```bash
git clone https://github.com/hkrishnan62/ETL_Parser.git
cd ETL_Parser
```

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run the Application**
```bash
python app.py
```

Open your browser to: **http://localhost:5000**

### First Use
1. Download a sample mapping: [sample_mapping.csv](examples/sample_mapping.csv)
2. Upload to the web interface
3. Configure your source/target tables
4. Click "Generate SQL Queries"
5. Copy the generated SQL to your database

---

## Features

### ✨ Core Features

- **CSV Mapping Parser**: Upload CSV files containing ETL mapping definitions
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

### 🤖 AI-Powered Features (Optional)

- **Intelligent Transformation Suggestions**: Get AI-recommended SQL transformations based on column names and types
- **Natural Language Mapping Generation**: Describe your ETL mapping in plain English, AI generates the CSV
- **SQL Query Optimization**: Automatically optimize generated queries for your database
- **Mapping Quality Analysis**: AI analyzes your mappings and provides recommendations
- **Plain English Explanations**: Convert technical SQL into business-friendly explanations
- **Syntax Validation**: Validate transformation syntax for different database dialects

> 💡 **AI features are optional** - the application works fully without them. Configure OpenAI API key to enable.

---

## Installation & Setup

### Requirements

- Python 3.8+
- Flask 3.0.0
- Pandas 2.1.4
- Werkzeug 3.0.1

### For Users (Quick Setup)

```bash
# Clone the repository
git clone https://github.com/hkrishnan62/ETL_Parser.git
cd ETL_Parser

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser to: http://localhost:5000
```

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

# Access at: http://localhost:5000
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

---

## Usage Guide

### Web Interface

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload your CSV mapping document and configure:
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
validator = ETLValidator('path/to/mapping.csv')

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

---

## CSV Mapping Format

### Required Format

Your CSV file must contain the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| `source_column` | Source column name | Yes* |
| `target_column` | Target column name | Yes |
| `transformation` | SQL transformation expression | No |
| `is_key` | Whether column is a join key (TRUE/FALSE) | No |

*Can be empty for calculated/derived fields

### Example Mapping CSV

```csv
source_column,target_column,transformation,is_key
customer_id,customer_id,source_table.customer_id,TRUE
first_name,full_name,"CONCAT(source_table.first_name, ' ', source_table.last_name)",FALSE
email,email_address,LOWER(TRIM(source_table.email)),FALSE
status,status_code,"CASE WHEN source_table.status = 'A' THEN 'ACTIVE' ELSE 'INACTIVE' END",FALSE
```

### Supported Transformations

#### String Operations
```csv
# Concatenation
first_name,full_name,"CONCAT(source_table.first_name, ' ', source_table.last_name)"

# Case conversion
email,email_lower,LOWER(source_table.email)
region,region_upper,UPPER(source_table.region)

# Trimming
name,name_trimmed,TRIM(source_table.name)

# Combining multiple
email,email_clean,"LOWER(TRIM(source_table.email))"

# Advanced concatenation
address,full_address,"CONCAT_WS(', ', source_table.street, source_table.city, source_table.state)"
```

#### Conditional Logic
```csv
# Simple case
status,status_desc,"CASE WHEN source_table.status = 'A' THEN 'ACTIVE' ELSE 'INACTIVE' END"

# Multiple conditions
priority,priority_level,"CASE WHEN source_table.amount > 1000 THEN 'HIGH' WHEN source_table.amount > 500 THEN 'MEDIUM' ELSE 'LOW' END"
```

#### Date & Time
```csv
# Type conversion
date_string,date_value,"CAST(source_table.date_string AS DATE)"

# Timestamp conversion
date_str,timestamp_value,"TO_TIMESTAMP(source_table.date_str, 'YYYY-MM-DD')"

# Extract parts
order_date,order_year,"EXTRACT(YEAR FROM source_table.order_date)"
order_date,order_month,"EXTRACT(MONTH FROM source_table.order_date)"
```

#### Numeric Operations
```csv
# Rounding
price,price_rounded,"ROUND(source_table.price, 2)"

# Type casting
amount,amount_decimal,"CAST(source_table.amount AS DECIMAL(10,2))"

# Calculations
,total_amount,"(source_table.quantity * source_table.unit_price) - COALESCE(source_table.discount, 0)"

# Percentage conversion
discount_decimal,discount_pct,"source_table.discount_decimal * 100"
```

#### NULL Handling
```csv
# Default values
discount,discount_value,"COALESCE(source_table.discount, 0)"

# NULL replacement
middle_name,middle_initial,"COALESCE(source_table.middle_name, 'N/A')"
```

#### Regular Expressions
```csv
# Remove non-numeric characters
phone,phone_digits,"REGEXP_REPLACE(source_table.phone, '[^0-9]', '')"

# Clean special characters
product,product_clean,"REGEXP_REPLACE(source_table.product, '[^a-zA-Z0-9 ]', '')"
```

#### Calculated Fields
```csv
# No source column needed - leave empty
,total_sales,"(source_table.quantity * source_table.price)"
,profit_margin,"((source_table.revenue - source_table.cost) / source_table.revenue) * 100"
```

---

## Generated Query Types

### 1. Source MINUS Target

**Purpose**: Identifies records that exist in the source (after transformation) but are missing in the target table.

**Use case**: Find data that didn't load properly into target

**Example Output**:
```sql
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
SELECT * FROM source_transformed
EXCEPT
SELECT * FROM target_data;
```

### 2. Target MINUS Source

**Purpose**: Identifies records that exist in the target but are missing in the transformed source.

**Use case**: Find extra or unexpected data in target

### 3. Complete Validation

**Purpose**: Combines both queries for comprehensive bidirectional validation.

**Use case**: Full reconciliation report

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐          ┌──────────────────────┐        │
│  │   Web Interface      │          │  Command Line        │        │
│  │   (Flask + HTML)     │          │  Interface (CLI)     │        │
│  └──────────┬───────────┘          └──────────┬───────────┘        │
└─────────────┼──────────────────────────────────┼─────────────────────┘
              │                                  │
              └──────────────┬───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐       │
│  │              ETL Validator (etl_validator.py)           │       │
│  │                    [Main Orchestrator]                  │       │
│  └──────────────┬────────────────────────┬─────────────────┘       │
│                 │                        │                          │
│                 ▼                        ▼                          │
│  ┌──────────────────────┐    ┌──────────────────────┐             │
│  │  Mapping Parser      │    │  SQL Generator       │             │
│  │  (mapping_parser.py) │    │  (sql_generator.py)  │             │
│  └──────────────────────┘    └──────────────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

**Mapping Parser (`mapping_parser.py`)**
- Read and parse CSV file
- Validate required columns
- Extract source/target columns
- Identify transformation rules
- Handle NULL values

**SQL Generator (`sql_generator.py`)**
- Build SELECT clauses with transformations
- Create CTEs for source and target
- Generate EXCEPT queries
- Format and comment SQL

**ETL Validator (`etl_validator.py`)**
- Orchestrate parsing and generation
- Coordinate workflow between components
- Generate mapping summaries
- Provide unified API

**Web Application (`app.py`)**
- Handle file uploads
- Validate input files
- Process form parameters
- Call ETL Validator
- Return formatted responses

### File Structure

```
ETL_Parser/
│
├── 🌐 Web Layer
│   ├── app.py                    # Flask application
│   └── templates/
│       └── index.html            # Web interface
│
├── 🧠 Core Logic
│   └── src/
│       ├── __init__.py
│       ├── mapping_parser.py     # CSV parsing
│       ├── sql_generator.py      # SQL generation
│       ├── etl_validator.py      # Orchestrator
│       ├── ai_agent.py           # AI integration
│       └── ai_enhanced_validator.py  # AI validator
│
├── 📝 Examples & Documentation
│   ├── README.md                 # Full documentation
│   ├── QUICK_START.md            # Quick start guide
│   ├── COMPLETE_GUIDE.md         # Comprehensive guide
│   ├── PROJECT_SUMMARY.md        # Project summary
│   └── ARCHITECTURE.md           # Architecture details
│
├── 🧪 Testing
│   ├── tests/
│   │   └── test_suite.py         # Automated tests
│   ├── demo.py                   # Feature demonstrations
│   └── example_usage.py          # CLI usage example
│
├── 📂 Data & Examples
│   ├── examples/
│   │   ├── sample_mapping.csv    # Basic example
│   │   └── complex_mapping.csv   # Advanced example
│   ├── uploads/                  # User uploads
│   └── output/                   # Generated queries
│
└── ⚙️ Configuration
    ├── requirements.txt          # Python dependencies
    └── .gitignore               # Git ignore rules
```

---

## AI Features

### 🤖 Available AI Capabilities

#### 1. Intelligent Transformation Suggestions
Get AI-powered suggestions for SQL transformations based on column names and data types.

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
```

#### 2. Natural Language to SQL Mapping
Describe your ETL mapping in plain English, and AI generates the complete mapping CSV.

```python
validator = AIEnhancedValidator()
mappings = validator.generate_from_description(
    "Map customer ID as key, combine first and last name into full_name, "
    "convert email to lowercase, extract year from order_date"
)
```

#### 3. SQL Query Optimization
Automatically optimize generated SQL queries for your specific database.

```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

result = validator.generate_with_optimization(
    source_table='orders',
    target_table='orders_fact',
    database_type='postgres',
    query_type='both'
)

optimized_sql = result['optimized_queries']['source_minus_target']
notes = result['optimization_notes']
```

#### 4. Mapping Quality Analysis
AI analyzes your mapping document and provides quality assessment with recommendations.

```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

analysis = validator.analyze_mapping_quality()

print(analysis['quality_score'])        # excellent/good/fair/poor
print(analysis['issues'])               # List of potential problems
print(analysis['recommendations'])      # Suggestions for improvement
```

#### 5. Transformation Explanations
Convert technical SQL transformations into plain English explanations.

```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

explanations = validator.explain_transformations()
# Returns: {'full_name': 'Combines first and last name...', ...}
```

#### 6. Syntax Validation
Validate transformation syntax for your specific database dialect.

```python
validator = AIEnhancedValidator('mapping.csv')
validator.load_mappings()

validation = validator.validate_transformation_syntax(database_type='postgres')

for result in validation:
    if not result['valid']:
        print(f"Issue in {result['target_column']}: {result['issues']}")
```

### 🔧 Setup & Configuration

#### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Installs:
- `openai` - OpenAI API client
- `langchain` - LangChain framework
- `python-dotenv` - Environment variable management

#### Step 2: Configure API Key

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

#### Step 3: Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### 💻 Usage

#### Web Interface
1. Start the application: `python app.py`
2. Open http://localhost:5000
3. Check "🤖 Use AI Optimization & Analysis"
4. Upload your CSV mapping
5. Select database type
6. Generate queries with AI optimization

#### Command Line
```python
from src.ai_enhanced_validator import AIEnhancedValidator

validator = AIEnhancedValidator('examples/sample_mapping.csv')
validator.load_mappings()

if validator.is_ai_available():
    analysis = validator.get_comprehensive_analysis(database_type='postgres')
    print(analysis['quality_analysis'])
else:
    print("AI not available - configure OPENAI_API_KEY")
```

---

## Desktop Application

### What is the Desktop Version?

The desktop version is a **standalone application** that:
- ✅ Runs like a native desktop app (no browser needed)
- ✅ Can be installed with a simple double-click
- ✅ Works offline (except AI features)
- ✅ No Python or technical knowledge required for users
- ✅ Cross-platform (Windows, macOS, Linux)

### Quick Start (For Developers)

#### Step 1: Install Desktop Requirements

```bash
pip install -r desktop_requirements.txt
```

#### Step 2: Run as Desktop App (Development Mode)

```bash
python desktop_app.py
```

#### Step 3: Build Standalone Executable (For Distribution)

```bash
python build_desktop_app.py
```

This creates a **distributable application** in the `dist/` folder.

### Distribution Methods

#### Method 1: Standalone Executable (Recommended)

**Build:**
```bash
python build_desktop_app.py
```

**Result:**
- Windows: `dist/ETL_Parser/ETL_Parser.exe`
- macOS: `dist/ETL_Parser.app`
- Linux: `dist/ETL_Parser/ETL_Parser`

**Share with Users:**
1. Zip the entire `dist/ETL_Parser` folder
2. Share the zip file
3. Users extract and double-click the executable
4. Done! No installation needed.

**File Size:** ~50-100 MB (includes Python runtime)

#### Method 2: Windows Installer (.msi)

Use [Inno Setup](https://jrsoftware.org/isdl.php) to create an installer.

#### Method 3: macOS Installer (.dmg)

```bash
pip install dmgbuild
dmgbuild -s dmg_settings.py "ETL Parser" dist/ETL_Parser.dmg
```

#### Method 4: Linux Package (.deb / .rpm)

```bash
# For Debian/Ubuntu
pip install stdeb
python setup.py --command-packages=stdeb.command bdist_deb
```

---

## Deployment

### Deploy to Render.com (RECOMMENDED - FREE)

**Best for:** Easy deployment, auto-deploys from GitHub

#### Quick Deploy Steps:
1. Go to: https://render.com
2. Sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select repository: `hkrishnan62/ETL_Parser`
5. Render auto-detects settings from `render.yaml`
6. Click **"Create Web Service"**

**Done!** Your app will be live at: `https://etl-parser.onrender.com`

### Other Deployment Options

- **Railway.app** - Modern UI, fast deployment
- **PythonAnywhere** - Python-specific, always on
- **Fly.io** - Global edge deployment
- **Docker** - Container deployment
- **Heroku** - Traditional hosting (paid)

### Configuration Files Included

- ✅ `Procfile` - For Heroku/Render
- ✅ `render.yaml` - One-click Render deployment
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - All dependencies

### Environment Variables

If using AI features, set these in your hosting platform:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Database Testing

### Testing Generated Queries

#### Method 1: Using Python

**PostgreSQL Example:**
```python
import psycopg2
from src.etl_validator import ETLValidator

# Generate SQL queries
validator = ETLValidator('examples/complex_mapping.csv')
validator.load_mappings()

queries = validator.generate_validation_queries(
    source_table='source_table',
    target_table='orders_fact',
    source_schema='staging',
    target_schema='production',
    query_type='both'
)

# Connect to database
conn = psycopg2.connect(
    host="your-host.com",
    port=5432,
    database="your_database",
    user="your_username",
    password="your_password"
)

cursor = conn.cursor()

# Run validation query
cursor.execute(queries['source_minus_target'])
results = cursor.fetchall()

print(f"Found {len(results)} discrepancies:")
for row in results:
    print(row)

cursor.close()
conn.close()
```

#### Method 2: Direct Database Client

1. Copy the generated SQL from web interface or CLI
2. Open your database client (SQL Developer, MySQL Workbench, pgAdmin, etc.)
3. Paste the SQL query
4. Execute and review results

---

## Troubleshooting

### Issue: "No file provided" Error
**Solution**: Ensure you've selected a CSV file before clicking Generate

### Issue: "Invalid file type" Error
**Solution**: File must be `.csv` extension

### Issue: Generated Query Syntax Error
**Cause**: Transformation contains database-specific syntax
**Solution**: Adjust transformation to match your database SQL dialect

### Issue: Port Already in Use
**Solution**: Stop existing process on port 5000, then restart the app

### Issue: Module Not Found Error
**Solution**: Reinstall dependencies with `pip install -r requirements.txt`

### Issue: Windows protected your PC
**Solution**: Click "More info" → "Run anyway" (or code sign your executable)

---

## Google Indexing Guide

### ✅ Changes Made to Enable Google Indexing

#### 1. robots.txt - CREATED ✓
The robots.txt file tells Google's crawler which pages can and cannot be crawled.

#### 2. SEO Headers - ADDED ✓
Added to Flask app middleware:
- `X-Content-Type-Options`: Prevents MIME type sniffing
- `X-Frame-Options`: Protects against clickjacking
- `X-XSS-Protection`: Enables XSS filtering
- `Referrer-Policy`: Controls referrer information

#### 3. Sitemap - VERIFIED ✓
Location: `/static/sitemap.xml`
- Already configured with main URL
- Includes lastmod and priority tags

#### 4. Meta Tags - VERIFIED ✓
Already present in `index.html`:
- Title: "ETL Mapping Validator - Free Online SQL Validation Tool"
- Meta description: Clearly describes the tool
- Meta keywords: Relevant ETL, SQL, and validation terms
- Robots meta tag: "index, follow"
- Canonical URL: https://etl-parser.onrender.com
- Mobile viewport tag

### 🚀 Next Steps to Get Indexed on Google

#### Step 1: Verify Your Domain
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Click "Add property"
3. Enter your domain: `https://etl-mapping-converter-to-sql.onrender.com/`
4. Choose verification method (DNS record, HTML file, or HTML tag)

#### Step 2: Submit Sitemap to Google
1. In Google Search Console, go to "Sitemaps"
2. Click "Add/test sitemap"
3. Enter: `https://etl-mapping-converter-to-sql.onrender.com/sitemap.xml`
4. Click "Submit"

#### Step 3: Request Indexing
1. In Google Search Console, use "URL inspection" tool
2. Enter: `https://etl-mapping-converter-to-sql.onrender.com/`
3. Click "Request indexing"
4. Google will crawl and index your pages

#### Step 4: Monitor Indexing Status
- Check "Coverage" report to see which pages are indexed
- Monitor "Performance" to see search results
- Watch for any crawl errors in "Crawl stats"

### 📋 SEO Checklist

- [x] robots.txt created and configured
- [x] Sitemap.xml present and valid
- [x] Meta tags properly set
- [x] Mobile-responsive design (already implemented)
- [x] SEO headers added to responses
- [x] Canonical URL specified
- [x] Google verification files present
- [ ] Domain verified in Google Search Console ← **DO THIS**
- [ ] Sitemap submitted to Google Search Console ← **DO THIS**
- [ ] Request URL indexing from GSC ← **DO THIS**

---

## Best Practices

### 1. Always Mark Key Columns
```csv
customer_id,customer_id,source_table.customer_id,TRUE
order_id,order_id,source_table.order_id,TRUE
```
This ensures accurate JOIN conditions in validation queries.

### 2. Use Consistent Naming
```csv
# Good
source_table.column_name

# Avoid mixing
some_table.col1
source_table.col2
```

### 3. Test Complex Transformations Separately
For complex expressions, test them in your database first:
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM test_table LIMIT 5;
```

### 4. Save Generated Queries
Always save your generated SQL queries for:
- Version control
- Documentation
- Reuse in CI/CD pipelines

### 5. Handle NULLs Explicitly
```csv
# Use COALESCE for required fields
discount,discount_amount,"COALESCE(source_table.discount, 0)",FALSE
```

### 6. Monitor Performance
For large tables (100M+ rows):
- Create indexes on join key columns
- Consider running validation during off-hours
- Use LIMIT clause for initial testing

---

## Real-World Workflow

```
1. ETL Developer creates mapping document (CSV)
   ↓
2. Upload to ETL Validator web interface
   ↓
3. Configure source/target details
   ↓
4. Generate validation SQL queries
   ↓
5. Copy queries to your ETL tool/scheduler
   ↓
6. Execute after each ETL run
   ↓
7. Monitor for discrepancies
```

---

## Use Cases

1. **ETL Pipeline Validation**: Validate data transformations in production ETL jobs
2. **Data Migration**: Verify accuracy when migrating data between systems
3. **Data Quality**: Continuous monitoring of data quality
4. **Reconciliation**: Automated source-to-target reconciliation
5. **Audit Compliance**: Generate audit trails for regulatory compliance

---

## Support & Contributing

### Getting Help

- 📖 Check the [README.md](README.md) for detailed documentation
- 🚀 Review [QUICK_START.md](QUICK_START.md) for quick setup
- 📚 Explore example mappings in the `examples/` directory
- ▶️ Run [example_usage.py](example_usage.py) to see it in action
- 🐛 Open an issue on GitHub for bugs and feature requests

### Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Technology Stack

**Frontend:**
- HTML5
- CSS3 (Modern styling with gradients)
- JavaScript (ES6+)
- Fetch API

**Backend:**
- Python 3.12
- Flask 3.0 (Web framework)
- Werkzeug 3.0 (WSGI utilities)
- Jinja2 3.1 (Template engine)

**Data Processing:**
- Pandas 2.1 (CSV parsing)
- Python standard library

**AI (Optional):**
- OpenAI GPT models
- LangChain framework
- Python-dotenv

**Development:**
- pip (Package management)
- Git (Version control)
- Docker (Container deployment)

---

## Project Status

**Status**: ✅ Fully Operational
**Last Updated**: January 2026
**Test Status**: ✅ All Tests Passing

---

**Made with ❤️ for Data Engineers and ETL Developers**

For the latest updates and documentation, visit:
[https://github.com/hkrishnan62/ETL_Parser](https://github.com/hkrishnan62/ETL_Parser)
