# 🎮 SQL Playground - Standalone Usage (No Flask Required!)

## Overview

The SQL Playground is a **pure Python module** with **zero web dependencies**. It works standalone without Flask, Django, or any web framework.

## ✨ Key Features

- ✅ **No Flask Required** - Works as a standalone Python module
- ✅ **Zero Web Dependencies** - Pure Python + SQLite
- ✅ **Embeddable** - Use in scripts, Jupyter notebooks, or applications
- ✅ **Sandboxed** - Safe SQL execution with security controls
- ✅ **Self-Contained** - All features work without a web server

## 🚀 Quick Start (No Server Needed)

### Installation
```bash
# No extra dependencies needed!
# Just Python 3.8+ with standard library
```

### Basic Usage

```python
from src.sql_playground import SQLPlayground

# Initialize (no Flask, no server!)
playground = SQLPlayground()

# Execute a query
result = playground.execute_query("SELECT * FROM customers LIMIT 5")

# Check results
if result['success']:
    print(f"Found {result['row_count']} rows")
    for row in result['rows']:
        print(row)
```

**That's it!** No `app.run()`, no `flask`, no web server. 🎉

## 📚 Complete API Reference

### 1. Initialize Playground

```python
from src.sql_playground import SQLPlayground

# Default storage location
playground = SQLPlayground()

# Custom storage location
playground = SQLPlayground(storage_dir='my_storage')
```

### 2. Execute Queries

```python
# Simple query
result = playground.execute_query("SELECT * FROM customers")

# With custom sample data
custom_data = {
    'my_table': [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
}
result = playground.execute_query(
    "SELECT * FROM my_table",
    sample_data=custom_data
)

# Response format
{
    'success': True,
    'rows': [...],           # List of dictionaries
    'columns': [...],        # Column names
    'row_count': 5,          # Number of rows
    'query': 'SELECT ...'    # Original query
}
```

### 3. Share Queries (No Web Server)

```python
# Create share link
share_id = playground.create_share_link(
    query="SELECT * FROM customers WHERE status = 'active'",
    sample_data=None,
    results={'rows': [...], 'columns': [...]}
)

print(f"Share ID: {share_id}")  # e.g., 'a1b2c3d4e5f6'

# Retrieve shared query later
shared = playground.get_shared_query(share_id)
print(shared['query'])
print(shared['view_count'])
```

### 4. Get Sample Queries

```python
samples = playground.get_sample_queries()

for sample in samples:
    print(f"Name: {sample['name']}")
    print(f"Description: {sample['description']}")
    print(f"Query: {sample['query']}")
```

### 5. Get Database Schema

```python
schema = playground.get_database_schema()

for table_name, columns in schema.items():
    print(f"Table: {table_name}")
    for col in columns:
        print(f"  - {col['name']} ({col['type']})")
```

## 💡 Use Cases

### 1. Jupyter Notebook

```python
# notebook_analysis.ipynb
from src.sql_playground import SQLPlayground

playground = SQLPlayground()

# Test ETL transformations
query = """
SELECT 
    UPPER(first_name) || ' ' || UPPER(last_name) as full_name,
    LOWER(email) as email_clean
FROM customers
"""

result = playground.execute_query(query)

# Convert to pandas DataFrame
import pandas as pd
df = pd.DataFrame(result['rows'])
df.head()
```

### 2. Automated Testing

```python
# test_etl_logic.py
import unittest
from src.sql_playground import SQLPlayground

class TestETLTransformations(unittest.TestCase):
    def setUp(self):
        self.playground = SQLPlayground()
    
    def test_email_normalization(self):
        result = self.playground.execute_query(
            "SELECT LOWER(email) as normalized FROM customers LIMIT 1"
        )
        self.assertTrue(result['success'])
        self.assertTrue(result['rows'][0]['normalized'].islower())
    
    def test_aggregation(self):
        result = self.playground.execute_query(
            "SELECT COUNT(*) as total FROM customers"
        )
        self.assertEqual(result['rows'][0]['total'], 5)
```

### 3. Command-Line Script

```python
#!/usr/bin/env python3
# analyze_data.py
import sys
from src.sql_playground import SQLPlayground

def main():
    playground = SQLPlayground()
    
    # Read query from command line
    query = sys.argv[1] if len(sys.argv) > 1 else "SELECT * FROM customers"
    
    result = playground.execute_query(query)
    
    if result['success']:
        print(f"Rows: {result['row_count']}")
        for row in result['rows']:
            print(row)
    else:
        print(f"Error: {result['error']}", file=sys.stderr)

if __name__ == '__main__':
    main()
```

**Usage:**
```bash
python analyze_data.py "SELECT status, COUNT(*) FROM orders GROUP BY status"
```

### 4. ETL Pipeline Integration

```python
# etl_pipeline.py
from src.sql_playground import SQLPlayground

class ETLValidator:
    def __init__(self):
        self.playground = SQLPlayground()
    
    def validate_transformation(self, source_data, transformation_sql):
        """Validate ETL transformation logic"""
        # Execute transformation
        result = self.playground.execute_query(
            transformation_sql,
            sample_data={'source': source_data}
        )
        
        if not result['success']:
            raise ValueError(f"Transformation failed: {result['error']}")
        
        return result['rows']
    
    def test_before_production(self):
        """Test transformations before deploying"""
        sample_data = [
            {'customer_id': 1, 'name': 'John Doe', 'email': 'JOHN@EXAMPLE.COM'},
            {'customer_id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
        ]
        
        transformation = """
        SELECT 
            customer_id,
            UPPER(name) as name_upper,
            LOWER(email) as email_lower
        FROM source
        """
        
        results = self.validate_transformation(sample_data, transformation)
        print(f"✓ Validated {len(results)} transformations")
        return results

# Use in pipeline
validator = ETLValidator()
validator.test_before_production()
```

### 5. Learning/Teaching Tool

```python
# sql_tutorial.py
from src.sql_playground import SQLPlayground

def teach_sql_basics():
    playground = SQLPlayground()
    
    lessons = [
        {
            'title': 'SELECT Basics',
            'query': 'SELECT * FROM customers LIMIT 3'
        },
        {
            'title': 'WHERE Clause',
            'query': "SELECT * FROM orders WHERE status = 'completed'"
        },
        {
            'title': 'GROUP BY',
            'query': 'SELECT status, COUNT(*) FROM orders GROUP BY status'
        }
    ]
    
    for lesson in lessons:
        print(f"\n📚 Lesson: {lesson['title']}")
        print(f"Query: {lesson['query']}")
        
        result = playground.execute_query(lesson['query'])
        print(f"Results: {result['row_count']} rows")
        for row in result['rows'][:2]:  # Show first 2 rows
            print(f"  {row}")

teach_sql_basics()
```

## 🔒 Security (Built-In, No Configuration)

```python
playground = SQLPlayground()

# These are automatically blocked:
playground.execute_query("DROP TABLE customers")     # ❌ Blocked
playground.execute_query("DELETE FROM orders")       # ❌ Blocked
playground.execute_query("UPDATE customers SET ...") # ❌ Blocked
playground.execute_query("INSERT INTO orders ...")   # ❌ Blocked

# Only SELECT queries allowed:
playground.execute_query("SELECT * FROM customers")  # ✅ Allowed
```

## 🎯 Comparison: Standalone vs Web

| Feature | Standalone | With Flask |
|---------|-----------|------------|
| SQL Execution | ✅ Yes | ✅ Yes |
| Sample Data | ✅ Yes | ✅ Yes |
| Share Links | ✅ Yes | ✅ Yes |
| Security | ✅ Yes | ✅ Yes |
| Web UI | ❌ No | ✅ Yes |
| REST API | ❌ No | ✅ Yes |
| Browser Access | ❌ No | ✅ Yes |
| Dependencies | ✅ None | Flask |
| Use Case | Scripts, Apps | Web Service |

## 📦 Zero Dependencies

The SQL Playground uses only Python standard library:

```python
import sqlite3        # Standard library
import hashlib        # Standard library
import json          # Standard library
import os            # Standard library
from datetime import datetime  # Standard library
from typing import Dict, List, Any, Optional  # Standard library
import re            # Standard library
```

**No pip install needed!** (except for the parent ETL Parser dependencies)

## 🚀 Performance

- **Fast**: In-memory SQLite database
- **Lightweight**: No web server overhead
- **Scalable**: Each instance is independent

```python
from src.sql_playground import SQLPlayground
import time

playground = SQLPlayground()

start = time.time()
result = playground.execute_query("SELECT * FROM customers")
elapsed = time.time() - start

print(f"Query executed in {elapsed*1000:.2f}ms")  # Typically < 5ms
```

## 🎓 Learning Path

1. **Start with basics** - Run simple SELECT queries
2. **Try JOINs** - Combine customers and orders
3. **Practice aggregations** - Use GROUP BY, COUNT, SUM
4. **Test transformations** - Try UPPER, LOWER, CONCAT
5. **Create custom data** - Test with your own tables
6. **Build applications** - Integrate into your tools

## 📝 Example: Complete Script

```python
#!/usr/bin/env python3
"""
SQL Playground Demo - No Flask Required
"""
from src.sql_playground import SQLPlayground

def main():
    # Initialize
    playground = SQLPlayground()
    
    # Execute query
    result = playground.execute_query("""
        SELECT 
            c.first_name,
            c.last_name,
            COUNT(o.order_id) as total_orders,
            SUM(o.total_amount) as total_spent
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
    """)
    
    # Display results
    if result['success']:
        print("Customer Purchase Summary:")
        print("-" * 60)
        for row in result['rows']:
            print(f"{row['first_name']} {row['last_name']}: "
                  f"{row['total_orders']} orders, "
                  f"${row['total_spent']:.2f} spent")
    else:
        print(f"Error: {result['error']}")

if __name__ == '__main__':
    main()
```

Run it:
```bash
python my_script.py
```

No web server. No Flask. Just Python! 🎉

## 🔗 Optional: Add Flask Endpoints Later

If you want web access, Flask endpoints are **optional add-ons**:

```python
# Optional: app.py for web access
from flask import Flask, jsonify, request
from src.sql_playground import SQLPlayground

app = Flask(__name__)
playground = SQLPlayground()

@app.route('/api/execute', methods=['POST'])
def execute():
    query = request.json.get('query')
    result = playground.execute_query(query)
    return jsonify(result)

# Only run if you want web access
if __name__ == '__main__':
    app.run()
```

**But you don't need Flask at all!** The playground works perfectly standalone.

## ✨ Summary

The SQL Playground is:
- ✅ **Standalone** - No web dependencies
- ✅ **Embeddable** - Use anywhere
- ✅ **Zero config** - Works out of the box
- ✅ **Secure** - Built-in safety
- ✅ **Fast** - In-memory execution
- ✅ **Flexible** - Custom data support

**Start using it now without any server setup!**

```python
from src.sql_playground import SQLPlayground
playground = SQLPlayground()
result = playground.execute_query("SELECT * FROM customers")
print(result['rows'])
```

That's it! 🚀
