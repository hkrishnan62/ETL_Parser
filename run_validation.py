#!/usr/bin/env python3
"""
Complete Database Validation Script
Customize the connection details for your database
"""
import sys
import os
from src.etl_validator import ETLValidator

# Database configuration (CUSTOMIZE THESE)
DB_CONFIG = {
    'type': 'postgresql',  # postgresql, mysql, sqlserver, oracle
    'host': 'localhost',
    'port': 5432,
    'database': 'your_database',
    'user': 'your_username',
    'password': os.environ.get('DB_PASSWORD', 'your_password')  # Use env var for security
}

# ETL configuration (CUSTOMIZE THESE)
ETL_CONFIG = {
    'mapping_file': 'examples/complex_mapping.csv',
    'target_table': 'orders_fact',
    'target_schema': None,  # Set to 'production' if you use schemas
    'source_schema': None,  # Set to 'staging' if you use schemas
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
    
    try:
        conn = connect_database(DB_CONFIG)
        cursor = conn.cursor()
        print("   ✓ Connected successfully")
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nPlease check:")
        print("  - Database credentials are correct")
        print("  - Database server is running and accessible")
        print("  - Required Python package is installed (psycopg2, mysql-connector-python, etc.)")
        return
    
    # 3. Run validation queries
    print("\n3. Running validation queries...\n")
    
    results_summary = {}
    
    for query_name, query_sql in queries.items():
        print(f"\n{'='*80}")
        print(f"Query: {query_name.upper()}")
        print(f"{'='*80}")
        
        try:
            cursor.execute(query_sql)
            results = cursor.fetchall()
            results_summary[query_name] = len(results)
            
            if results:
                print(f"\n⚠️  Found {len(results)} discrepancies")
                print("\nFirst 5 records:")
                for i, row in enumerate(results[:5], 1):
                    print(f"{i}. {row}")
                
                if len(results) > 5:
                    print(f"\n... and {len(results) - 5} more")
            else:
                print("\n✅ No discrepancies found - Perfect match!")
                
        except Exception as e:
            print(f"\n❌ Error running query: {e}")
            print("\nNote: The generated SQL may need adjustments for your database version.")
            print("Save the query and review with your DBA if needed.")
    
    # 4. Summary
    print("\n" + "="*80)
    print("Validation Summary")
    print("="*80)
    
    total_issues = sum(results_summary.values())
    
    for query_name, count in results_summary.items():
        status = "✅" if count == 0 else "⚠️"
        print(f"{status} {query_name}: {count} discrepancies")
    
    if total_issues == 0:
        print("\n🎉 Perfect! No discrepancies found.")
    else:
        print(f"\n⚠️  Total discrepancies: {total_issues}")
        print("\nRecommendations:")
        print("  - Review the specific records listed above")
        print("  - Check ETL transformation logic")
        print("  - Verify data loading completed successfully")
    
    # 5. Cleanup
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
