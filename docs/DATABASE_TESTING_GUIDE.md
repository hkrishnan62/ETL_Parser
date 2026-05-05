# Database Testing Guide

This guide explains how to test the generated SQL queries against your live database.

## Overview

The ETL Validator generates SQL queries that can be run against your database to validate data transformations. This guide shows you how to:
1. Connect to your database
2. Run the generated queries
3. Interpret the results

## Prerequisites

- Database credentials (host, port, username, password, database name)
- Database client or Python connection library installed

## Supported Databases

The tool generates SQL for:
- PostgreSQL
- MySQL
- Oracle
- SQL Server
- Snowflake
- Generic SQL

## Method 1: Using Python (Recommended)

### Installation

```bash
# For PostgreSQL
pip install psycopg2-binary

# For MySQL
pip install mysql-connector-python

# For SQL Server
pip install pyodbc

# For Oracle
pip install cx_Oracle

# For Snowflake
pip install snowflake-connector-python
```

### PostgreSQL Example

```python
import psycopg2
from src.etl_validator import ETLValidator

# 1. Generate SQL queries
validator = ETLValidator('examples/complex_mapping.csv')
validator.load_mappings()

summary = validator.get_mapping_summary()
source_table = summary['detected_source_tables'][0] if summary.get('detected_source_tables') else 'source_table'

queries = validator.generate_validation_queries(
    source_table=source_table,
    target_table='orders_fact',
    source_schema='staging',
    target_schema='production',
    query_type='both'
)

# 2. Connect to database
conn = psycopg2.connect(
    host="your-host.com",
    port=5432,
    database="your_database",
    user="your_username",
    password="your_password"
)

cursor = conn.cursor()

# 3. Run validation queries
print("Running Source MINUS Target query...")
cursor.execute(queries['source_minus_target'])
results = cursor.fetchall()

print(f"\nFound {len(results)} discrepancies:")
for row in results:
    print(row)

cursor.close()
conn.close()
```

### MySQL Example

```python
import mysql.connector

conn = mysql.connector.connect(
    host="your-host.com",
    port=3306,
    database="your_database",
    user="your_username",
    password="your_password"
)

cursor = conn.cursor()
cursor.execute(queries['source_minus_target'])
results = cursor.fetchall()
print(f"Found {len(results)} discrepancies")
```

### SQL Server Example

```python
import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=your-server.com;'
    'DATABASE=your_database;'
    'UID=your_username;'
    'PWD=your_password'
)

cursor = conn.cursor()
cursor.execute(queries['source_minus_target'])
results = cursor.fetchall()
print(f"Found {len(results)} discrepancies")
```

## Method 2: Using Database Client Tools

### Using DBeaver, pgAdmin, SQL Developer, etc.

1. **Generate Queries**
   - Upload your mapping CSV to the web interface (http://localhost:5000)
   - Select your database type
   - Click "Generate SQL Queries"
   - Copy the generated SQL

2. **Run in Database Client**
   - Open your database client
   - Connect to your database
   - Paste the SQL query
   - Execute the query

3. **Interpret Results**
   - If the query returns rows, those are the discrepancies
   - Empty result = perfect match between source and target
   - Review the specific records that don't match

### Using psql (PostgreSQL Command Line)

```bash
# Generate queries first and save to file
python3 -c "
from src.etl_validator import ETLValidator
v = ETLValidator('examples/complex_mapping.csv')
v.load_mappings()
s = v.get_mapping_summary()
st = s.get('detected_source_tables', ['source_table'])[0]
q = v.generate_validation_queries(st, 'target_table')
print(q['source_minus_target'])
" > validation_query.sql

# Run against database
psql -h your-host.com -U your_user -d your_db -f validation_query.sql
```

## Method 3: Complete Python Script Template

Save this as `run_validation.py`:

```python
#!/usr/bin/env python3
"""
Complete Database Validation Script
Customize the connection details for your database
"""
import sys
from src.etl_validator import ETLValidator

# Database configuration (CUSTOMIZE THESE)
DB_CONFIG = {
    'type': 'postgresql',  # postgresql, mysql, sqlserver, oracle
    'host': 'localhost',
    'port': 5432,
    'database': 'your_database',
    'user': 'your_username',
    'password': 'your_password'
}

# ETL configuration (CUSTOMIZE THESE)
ETL_CONFIG = {
    'mapping_file': 'examples/complex_mapping.csv',
    'target_table': 'orders_fact',
    'target_schema': 'production',
    'source_schema': 'staging',
}

def connect_database(config):
    """Create database connection based on type"""
    db_type = config['type'].lower()
    
    if db_type == 'postgresql':
        import psycopg2
        return psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
    elif db_type == 'mysql':
        import mysql.connector
        return mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
    elif db_type == 'sqlserver':
        import pyodbc
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={config['host']};"
            f"DATABASE={config['database']};"
            f"UID={config['user']};"
            f"PWD={config['password']}"
        )
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

def main():
    print("="*80)
    print("ETL Validation Runner")
    print("="*80)
    
    # 1. Generate SQL
    print("\n1. Generating validation queries...")
    validator = ETLValidator(ETL_CONFIG['mapping_file'])
    validator.load_mappings()
    
    summary = validator.get_mapping_summary()
    source_tables = summary.get('detected_source_tables', [])
    source_table = source_tables[0] if source_tables else 'source_table'
    
    print(f"   Source table: {source_table}")
    print(f"   Target table: {ETL_CONFIG['target_table']}")
    print(f"   Total mappings: {summary['total_mappings']}")
    
    queries = validator.generate_validation_queries(
        source_table=source_table,
        target_table=ETL_CONFIG['target_table'],
        source_schema=ETL_CONFIG.get('source_schema'),
        target_schema=ETL_CONFIG.get('target_schema'),
        query_type='both'
    )
    
    # 2. Connect to database
    print("\n2. Connecting to database...")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Database: {DB_CONFIG['database']}")
    
    conn = connect_database(DB_CONFIG)
    cursor = conn.cursor()
    print("   ✓ Connected successfully")
    
    # 3. Run validation queries
    print("\n3. Running validation queries...\n")
    
    for query_name, query_sql in queries.items():
        print(f"\n{'='*80}")
        print(f"Query: {query_name.upper()}")
        print(f"{'='*80}")
        
        try:
            cursor.execute(query_sql)
            results = cursor.fetchall()
            
            if results:
                print(f"\n⚠️  Found {len(results)} discrepancies")
                print("\nFirst 10 records:")
                for i, row in enumerate(results[:10], 1):
                    print(f"{i}. {row}")
                
                if len(results) > 10:
                    print(f"\n... and {len(results) - 10} more")
            else:
                print("\n✅ No discrepancies found - Perfect match!")
                
        except Exception as e:
            print(f"\n❌ Error running query: {e}")
            print("\nQuery SQL:")
            print(query_sql[:500] + "...")
    
    # 4. Cleanup
    cursor.close()
    conn.close()
    
    print("\n" + "="*80)
    print("Validation Complete")
    print("="*80)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

## Running the Validation

```bash
# Edit run_validation.py with your database details
nano run_validation.py

# Run the validation
python3 run_validation.py
```

## Understanding the Results

### Source MINUS Target Query
- **Returns rows**: These records exist in source but are missing or different in target
- **Empty result**: All source records are correctly transformed in target

### Target MINUS Source Query
- **Returns rows**: These records exist in target but don't match source transformations
- **Empty result**: No extra or mismatched records in target

### Common Issues Found

1. **Missing Records**: Some source records didn't load to target
2. **Transformation Errors**: Data was transformed incorrectly
3. **Data Type Mismatches**: Casting or conversion issues
4. **NULL Handling**: COALESCE or default value problems

## Best Practices

1. **Start Small**: Test with a small date range first
2. **Use WHERE Clauses**: Add date filters to limit data volume
3. **Save Results**: Export discrepancies to CSV for analysis
4. **Schedule Regular Checks**: Run validation after each ETL job
5. **Monitor Performance**: Add query timeouts for large datasets

## Troubleshooting

### Query Takes Too Long
Add a filter to limit records:
```sql
-- Add to the source_transformed CTE
WHERE order_date >= '2024-01-01'
```

### Syntax Errors
- Check your database type selection
- Some functions may need adjustment for your specific database version
- Consult your DBA for database-specific syntax

### Connection Issues
- Verify credentials
- Check firewall rules
- Ensure database is accessible from your network
- Test with a simple query first

## Security Notes

- Never commit database passwords to version control
- Use environment variables for credentials:
  ```python
  import os
  DB_CONFIG = {
      'password': os.environ.get('DB_PASSWORD')
  }
  ```
- Use read-only database accounts for validation
- Consider using connection pools for production

## Next Steps

1. Review the generated queries
2. Test against a development database first
3. Adjust transformation logic if discrepancies are expected
4. Schedule automated validation runs
5. Set up alerts for validation failures
