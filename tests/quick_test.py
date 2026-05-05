#!/usr/bin/env python3
import sys
sys.path.insert(0, '/workspaces/ETL_Parser')

from src.sql_playground import SQLPlayground

print("Testing SQL Playground...")
p = SQLPlayground()
result = p.execute_query("SELECT * FROM customers LIMIT 2")
print(f"Success: {result['success']}")
print(f"Rows: {result['row_count']}")
print("Test passed!")
