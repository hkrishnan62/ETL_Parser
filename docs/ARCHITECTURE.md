# ETL Mapping Validator - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐          ┌──────────────────────┐        │
│  │   Web Interface      │          │  Command Line        │        │
│  │   (Flask + HTML)     │          │  Interface (CLI)     │        │
│  │                      │          │                      │        │
│  │  • Upload CSV        │          │  • Python Script     │        │
│  │  • Configure         │          │  • Automation        │        │
│  │  • Display Results   │          │  • CI/CD Integration │        │
│  └──────────┬───────────┘          └──────────┬───────────┘        │
│             │                                  │                     │
└─────────────┼──────────────────────────────────┼─────────────────────┘
              │                                  │
              └──────────────┬───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │              ETL Validator (etl_validator.py)           │       │
│  │                    [Main Orchestrator]                  │       │
│  │                                                         │       │
│  │  • Coordinates workflow                                │       │
│  │  • Manages pipeline                                    │       │
│  │  • Generates summary reports                           │       │
│  └──────────────┬────────────────────────┬─────────────────┘       │
│                 │                        │                          │
│                 ▼                        ▼                          │
│  ┌──────────────────────┐    ┌──────────────────────┐             │
│  │  Mapping Parser      │    │  SQL Generator       │             │
│  │  (mapping_parser.py) │    │  (sql_generator.py)  │             │
│  │                      │    │                      │             │
│  │  • Read CSV          │    │  • Build SELECT      │             │
│  │  • Parse mappings    │    │  • Generate CTEs     │             │
│  │  • Extract columns   │    │  • Create EXCEPT     │             │
│  │  • Identify keys     │    │  • Format SQL        │             │
│  └──────────────────────┘    └──────────────────────┘             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           OUTPUT                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐    ┌──────────────────────┐             │
│  │  Source MINUS Target │    │  Target MINUS Source │             │
│  │  Validation Query    │    │  Validation Query    │             │
│  │                      │    │                      │             │
│  │  • Find missing      │    │  • Find extra        │             │
│  │    target records    │    │    target records    │             │
│  └──────────────────────┘    └──────────────────────┘             │
│                                                                      │
│  ┌─────────────────────────────────────────────────────┐           │
│  │         Complete Bidirectional Validation           │           │
│  │                                                     │           │
│  │  • Both queries combined                           │           │
│  │  • Full reconciliation report                      │           │
│  └─────────────────────────────────────────────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
CSV Mapping Document
        │
        │ (Upload/Read)
        ▼
┌───────────────────┐
│  Mapping Parser   │
│                   │
│  Extracts:        │
│  • Source cols    │
│  • Target cols    │
│  • Transforms     │
│  • Key columns    │
└────────┬──────────┘
         │
         │ (Parsed Mappings List)
         ▼
┌───────────────────┐
│  SQL Generator    │
│                   │
│  Creates:         │
│  • CTEs           │
│  • SELECT clause  │
│  • EXCEPT logic   │
│  • JOIN fallback  │
└────────┬──────────┘
         │
         │ (Generated SQL Queries)
         ▼
┌───────────────────┐
│  ETL Validator    │
│                   │
│  Returns:         │
│  • Query dict     │
│  • Summary stats  │
│  • Mappings info  │
└────────┬──────────┘
         │
         │ (JSON Response / File Output)
         ▼
    User Output
```

## Component Responsibilities

### 1. Mapping Parser (`mapping_parser.py`)
```
Input:  CSV file path
Output: List of mapping dictionaries

Responsibilities:
  • Read and parse CSV file
  • Validate required columns
  • Extract source/target columns
  • Identify transformation rules
  • Flag join key columns
  • Handle NULL values
```

### 2. SQL Generator (`sql_generator.py`)
```
Input:  Mapping list, table names, schema names
Output: SQL query strings

Responsibilities:
  • Build SELECT clauses with transformations
  • Create CTEs for source and target
  • Generate EXCEPT queries
  • Provide LEFT JOIN alternatives
  • Format and comment SQL
  • Handle schema prefixes
```

### 3. ETL Validator (`etl_validator.py`)
```
Input:  CSV path, configuration parameters
Output: Query dictionary, summary statistics

Responsibilities:
  • Orchestrate parsing and generation
  • Coordinate workflow between components
  • Generate mapping summaries
  • Provide unified API
  • Handle errors gracefully
```

### 4. Web Application (`app.py`)
```
Input:  HTTP requests with file uploads
Output: JSON responses with queries

Responsibilities:
  • Handle file uploads
  • Validate input files
  • Process form parameters
  • Call ETL Validator
  • Return formatted responses
  • Serve HTML interface
```

## Technology Stack

```
Frontend:
  ├── HTML5
  ├── CSS3 (Modern styling with gradients)
  ├── JavaScript (ES6+)
  └── Fetch API

Backend:
  ├── Python 3.12
  ├── Flask 3.0 (Web framework)
  ├── Werkzeug 3.0 (WSGI utilities)
  └── Jinja2 3.1 (Template engine)

Data Processing:
  ├── Pandas 2.1 (CSV parsing)
  └── Python standard library

Development:
  ├── pip (Package management)
  └── Git (Version control)
```

## File Structure

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
│       └── etl_validator.py      # Orchestrator
│
├── 📝 Examples & Documentation
│   ├── README.md                 # Full documentation
│   ├── QUICK_START.md            # Quick start guide
│   ├── COMPLETE_GUIDE.md         # Comprehensive guide
│   ├── PROJECT_SUMMARY.md        # Project summary
│   └── ARCHITECTURE.md           # This file
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

## Sequence Diagram

```
User          Web UI        Flask App      ETL Validator    Mapping Parser    SQL Generator
 │              │               │                │                 │                │
 │─Upload CSV──>│               │                │                 │                │
 │              │               │                │                 │                │
 │              │─POST /upload─>│                │                 │                │
 │              │               │                │                 │                │
 │              │               │─Initialize────>│                 │                │
 │              │               │                │                 │                │
 │              │               │                │─load_mappings()>│                │
 │              │               │                │                 │                │
 │              │               │                │<──mappings list─│                │
 │              │               │                │                 │                │
 │              │               │──generate_queries()─────────────────────────────>│
 │              │               │                │                 │                │
 │              │               │<─────────────────────generated SQL queries───────│
 │              │               │                │                 │                │
 │              │<──JSON response with queries───│                 │                │
 │              │               │                │                 │                │
 │<─Display───> │               │                │                 │                │
 │   Results    │               │                │                 │                │
 │              │               │                │                 │                │
```

## Query Generation Process

```
Step 1: Parse CSV
┌──────────────────────────────────┐
│ CSV Row:                         │
│ customer_id, customer_id,        │
│ source_table.customer_id, TRUE   │
└──────────────────────────────────┘
                │
                ▼
Step 2: Create Mapping Object
┌──────────────────────────────────┐
│ {                                │
│   source_column: "customer_id",  │
│   target_column: "customer_id",  │
│   transformation: "source...",   │
│   is_key: True                   │
│ }                                │
└──────────────────────────────────┘
                │
                ▼
Step 3: Build SELECT Clause
┌──────────────────────────────────┐
│ SELECT                           │
│   source_table.customer_id       │
│     AS customer_id               │
└──────────────────────────────────┘
                │
                ▼
Step 4: Create CTE
┌──────────────────────────────────┐
│ WITH source_transformed AS (     │
│   SELECT ... FROM source         │
│ )                                │
└──────────────────────────────────┘
                │
                ▼
Step 5: Add EXCEPT Logic
┌──────────────────────────────────┐
│ SELECT * FROM source_transformed │
│ EXCEPT                           │
│ SELECT * FROM target_data        │
└──────────────────────────────────┘
                │
                ▼
Step 6: Format & Return
┌──────────────────────────────────┐
│ Complete SQL with:               │
│ • Comments                       │
│ • Formatting                     │
│ • Alternative queries            │
└──────────────────────────────────┘
```

## Design Patterns Used

### 1. **Separation of Concerns**
- Parsing logic separated from SQL generation
- Web layer separated from business logic
- Each component has single responsibility

### 2. **Factory Pattern**
- SQL Generator creates different query types
- Validator creates appropriate parsers/generators

### 3. **Template Method**
- SQL generation follows template structure
- CTE → SELECT → EXCEPT pattern

### 4. **Strategy Pattern**
- Different query types (source-minus-target, target-minus-source)
- User selects strategy via configuration

## Extension Points

Want to extend the application? Here are the key extension points:

### 1. Add New Transformation Types
Location: `sql_generator.py`
Method: `_clean_transformation()`

### 2. Support Different SQL Dialects
Location: `sql_generator.py`
Add: Dialect-specific generation methods

### 3. Add New Output Formats
Location: `etl_validator.py`
Add: New format generation methods

### 4. Custom Validation Rules
Location: `etl_validator.py`
Add: New validation query types

### 5. Additional Input Formats
Location: `mapping_parser.py`
Add: Support for Excel, JSON, etc.

---

## Performance Considerations

- **CSV Parsing**: Pandas is efficient for files up to 100MB
- **In-Memory Processing**: All mappings loaded into memory
- **Query Generation**: Fast, < 1 second for typical mappings
- **Web Upload**: 16MB max file size limit

## Security Considerations

- File upload validation (CSV only)
- Secure filename handling with Werkzeug
- No SQL execution (only generation)
- Input sanitization for form fields

---

**Architecture Version**: 1.0
**Last Updated**: January 2026
