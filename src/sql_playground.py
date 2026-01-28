"""
SQL Playground - Execute and share SQL queries with sample data
"""
import sqlite3
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import re


class SQLPlayground:
    """Handles SQL query execution in a sandboxed environment"""
    
    def __init__(self, storage_dir: str = 'playground_storage'):
        """Initialize SQL playground with storage directory"""
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.shares_file = os.path.join(storage_dir, 'shares.json')
        
        # Initialize shares storage
        if not os.path.exists(self.shares_file):
            with open(self.shares_file, 'w') as f:
                json.dump({}, f)
    
    def create_sample_database(self, sample_data: Optional[Dict[str, List[Dict]]] = None) -> sqlite3.Connection:
        """
        Create an in-memory SQLite database with sample data
        
        Args:
            sample_data: Dictionary mapping table names to list of row dictionaries
        
        Returns:
            SQLite connection with sample data
        """
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        
        if sample_data:
            for table_name, rows in sample_data.items():
                if not rows:
                    continue
                
                # Sanitize table name
                table_name = self._sanitize_identifier(table_name)
                
                # Create table from first row
                first_row = rows[0]
                columns = ', '.join([f'{self._sanitize_identifier(col)} TEXT' 
                                   for col in first_row.keys()])
                
                conn.execute(f'CREATE TABLE {table_name} ({columns})')
                
                # Insert data
                for row in rows:
                    placeholders = ', '.join(['?' for _ in row])
                    cols = ', '.join([self._sanitize_identifier(col) for col in row.keys()])
                    conn.execute(
                        f'INSERT INTO {table_name} ({cols}) VALUES ({placeholders})',
                        tuple(row.values())
                    )
        else:
            # Create default sample tables
            self._create_default_sample_data(conn)
        
        conn.commit()
        return conn
    
    def _create_default_sample_data(self, conn: sqlite3.Connection):
        """Create default sample tables for demonstration"""
        # Customer table
        conn.execute('''
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone TEXT,
                created_date TEXT
            )
        ''')
        
        sample_customers = [
            (1, 'John', 'Doe', 'john.doe@email.com', '555-1234', '2024-01-15'),
            (2, 'Jane', 'Smith', 'jane.smith@email.com', '555-5678', '2024-02-20'),
            (3, 'Bob', 'Johnson', 'bob.j@email.com', '555-9012', '2024-03-10'),
            (4, 'Alice', 'Williams', 'alice.w@email.com', '555-3456', '2024-04-05'),
            (5, 'Charlie', 'Brown', 'charlie.b@email.com', '555-7890', '2024-05-12'),
        ]
        
        conn.executemany(
            'INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)',
            sample_customers
        )
        
        # Orders table
        conn.execute('''
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date TEXT,
                total_amount REAL,
                status TEXT
            )
        ''')
        
        sample_orders = [
            (101, 1, '2024-06-01', 150.00, 'completed'),
            (102, 2, '2024-06-05', 299.99, 'completed'),
            (103, 1, '2024-06-10', 75.50, 'pending'),
            (104, 3, '2024-06-15', 425.00, 'completed'),
            (105, 4, '2024-06-20', 199.99, 'shipped'),
            (106, 2, '2024-06-25', 89.99, 'completed'),
            (107, 5, '2024-06-30', 350.00, 'pending'),
        ]
        
        conn.executemany(
            'INSERT INTO orders VALUES (?, ?, ?, ?, ?)',
            sample_orders
        )
        
        conn.commit()
    
    def execute_query(self, query: str, sample_data: Optional[Dict[str, List[Dict]]] = None) -> Dict[str, Any]:
        """
        Execute SQL query in sandboxed environment
        
        Args:
            query: SQL query to execute
            sample_data: Optional custom sample data
        
        Returns:
            Dictionary with results, columns, and metadata
        """
        try:
            # Security: Block dangerous operations
            if not self._is_safe_query(query):
                return {
                    'success': False,
                    'error': 'Query contains disallowed operations. Only SELECT statements are allowed.',
                    'rows': [],
                    'columns': []
                }
            
            # Create database with sample data
            conn = self.create_sample_database(sample_data)
            
            # Execute query
            cursor = conn.execute(query)
            
            # Get results
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Convert rows to dictionaries
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            conn.close()
            
            return {
                'success': True,
                'rows': results,
                'columns': columns,
                'row_count': len(results),
                'query': query
            }
            
        except sqlite3.Error as e:
            return {
                'success': False,
                'error': f'SQL Error: {str(e)}',
                'rows': [],
                'columns': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution Error: {str(e)}',
                'rows': [],
                'columns': []
            }
    
    def _is_safe_query(self, query: str) -> bool:
        """
        Check if query is safe to execute
        Only allows SELECT statements
        """
        query_upper = query.upper().strip()
        
        # Remove comments
        query_upper = re.sub(r'--.*$', '', query_upper, flags=re.MULTILINE)
        query_upper = re.sub(r'/\*.*?\*/', '', query_upper, flags=re.DOTALL)
        
        # Check for dangerous keywords
        dangerous_keywords = [
            'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE',
            'TRUNCATE', 'REPLACE', 'ATTACH', 'DETACH', 'PRAGMA'
        ]
        
        for keyword in dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', query_upper):
                return False
        
        # Must start with SELECT (after whitespace)
        if not re.match(r'^\s*SELECT\b', query_upper):
            return False
        
        return True
    
    def _sanitize_identifier(self, identifier: str) -> str:
        """Sanitize SQL identifier (table/column name)"""
        # Remove any non-alphanumeric characters except underscore
        sanitized = re.sub(r'[^\w]', '_', identifier)
        # Ensure it doesn't start with a number
        if sanitized[0].isdigit():
            sanitized = '_' + sanitized
        return sanitized
    
    def create_share_link(self, query: str, sample_data: Optional[Dict] = None, 
                         results: Optional[Dict] = None) -> str:
        """
        Create a shareable link for a query
        
        Args:
            query: SQL query
            sample_data: Sample data used
            results: Query results
        
        Returns:
            Unique share ID
        """
        # Generate unique ID
        timestamp = datetime.now().isoformat()
        content = f"{query}_{timestamp}_{os.urandom(8).hex()}"
        share_id = hashlib.sha256(content.encode()).hexdigest()[:12]
        
        # Load existing shares
        with open(self.shares_file, 'r') as f:
            shares = json.load(f)
        
        # Store share data
        shares[share_id] = {
            'query': query,
            'sample_data': sample_data,
            'results': results,
            'created_at': timestamp,
            'view_count': 0
        }
        
        # Save shares
        with open(self.shares_file, 'w') as f:
            json.dump(shares, f, indent=2)
        
        return share_id
    
    def get_shared_query(self, share_id: str) -> Optional[Dict]:
        """
        Retrieve shared query by ID
        
        Args:
            share_id: Unique share identifier
        
        Returns:
            Share data or None if not found
        """
        try:
            with open(self.shares_file, 'r') as f:
                shares = json.load(f)
            
            if share_id in shares:
                # Increment view count
                shares[share_id]['view_count'] = shares[share_id].get('view_count', 0) + 1
                
                # Save updated view count
                with open(self.shares_file, 'w') as f:
                    json.dump(shares, f, indent=2)
                
                return shares[share_id]
            
            return None
        except Exception:
            return None
    
    def get_sample_queries(self) -> List[Dict[str, str]]:
        """Get list of sample queries for quick start"""
        return [
            {
                'name': 'ETL Row Count Validation',
                'description': 'Compare source and target row counts',
                'category': 'ETL Testing',
                'query': '''-- Source row count
SELECT 'Source' as table_name, COUNT(*) as row_count FROM customers
UNION ALL
-- Target row count (simulated)
SELECT 'Target' as table_name, COUNT(*) as row_count FROM customers;'''
            },
            {
                'name': 'Data Transformation Test',
                'description': 'Test ETL transformations with side-by-side comparison',
                'category': 'ETL Testing',
                'query': '''-- Compare original vs transformed data
SELECT 
    customer_id,
    first_name || ' ' || last_name as original_name,
    UPPER(first_name) || ' ' || UPPER(last_name) as transformed_name,
    email as original_email,
    LOWER(email) as transformed_email,
    phone as original_phone,
    REPLACE(phone, '-', '') as transformed_phone
FROM customers
LIMIT 5;'''
            },
            {
                'name': 'NULL Value Analysis',
                'description': 'Find NULL values across all columns',
                'category': 'Data Quality',
                'query': '''SELECT 
    'email' as column_name,
    COUNT(*) as null_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) as null_percentage
FROM customers 
WHERE email IS NULL
UNION ALL
SELECT 
    'phone',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2)
FROM customers 
WHERE phone IS NULL;'''
            },
            {
                'name': 'Duplicate Detection',
                'description': 'Find duplicate records in source data',
                'category': 'Data Quality',
                'query': '''SELECT 
    email,
    COUNT(*) as duplicate_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;'''
            },
            {
                'name': 'Data Profiling - Statistics',
                'description': 'Get min, max, avg for numeric columns',
                'category': 'Data Profiling',
                'query': '''SELECT 
    'orders' as table_name,
    COUNT(*) as total_rows,
    COUNT(DISTINCT customer_id) as unique_customers,
    MIN(total_amount) as min_amount,
    MAX(total_amount) as max_amount,
    ROUND(AVG(total_amount), 2) as avg_amount,
    SUM(total_amount) as total_revenue
FROM orders;'''
            },
            {
                'name': 'Referential Integrity Check',
                'description': 'Check for orphaned records',
                'category': 'Data Quality',
                'query': '''-- Find orders without matching customers (orphaned records)
SELECT 
    o.order_id,
    o.customer_id,
    o.total_amount,
    'No matching customer' as issue
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;'''
            },
            {
                'name': 'Date Range Validation',
                'description': 'Check if dates are within expected range',
                'category': 'Data Quality',
                'query': '''SELECT 
    MIN(created_date) as earliest_date,
    MAX(created_date) as latest_date,
    COUNT(*) as total_records,
    COUNT(CASE WHEN created_date < '2024-01-01' THEN 1 END) as before_2024,
    COUNT(CASE WHEN created_date > '2024-12-31' THEN 1 END) as after_2024
FROM customers;'''
            },
            {
                'name': 'String Length Validation',
                'description': 'Check if string lengths match target requirements',
                'category': 'Data Quality',
                'query': '''SELECT 
    customer_id,
    email,
    LENGTH(email) as email_length,
    CASE 
        WHEN LENGTH(email) > 100 THEN 'Too Long'
        WHEN LENGTH(email) < 5 THEN 'Too Short'
        ELSE 'Valid'
    END as validation_status
FROM customers
WHERE LENGTH(email) > 100 OR LENGTH(email) < 5;'''
            },
            {
                'name': 'CASE Statement Testing',
                'description': 'Test complex CASE transformations',
                'category': 'ETL Testing',
                'query': '''SELECT 
    order_id,
    status as original_status,
    total_amount,
    CASE 
        WHEN status = 'completed' AND total_amount >= 300 THEN 'High Value - Completed'
        WHEN status = 'completed' AND total_amount < 300 THEN 'Standard - Completed'
        WHEN status = 'pending' THEN 'Processing'
        WHEN status = 'shipped' THEN 'In Transit'
        ELSE 'Other'
    END as categorized_status
FROM orders;'''
            },
            {
                'name': 'Aggregation Validation',
                'description': 'Validate aggregated data matches source totals',
                'category': 'ETL Testing',
                'query': '''-- Compare detailed vs aggregated data
SELECT 
    'Detail Level' as level,
    COUNT(*) as record_count,
    SUM(total_amount) as total_revenue
FROM orders
UNION ALL
SELECT 
    'Aggregated by Status' as level,
    COUNT(DISTINCT status) as record_count,
    SUM(agg_revenue) as total_revenue
FROM (
    SELECT status, SUM(total_amount) as agg_revenue
    FROM orders
    GROUP BY status
);'''
            }
        ]
    
    def get_database_schema(self) -> Dict[str, List[Dict]]:
        """Get schema information for sample database"""
        conn = self.create_sample_database()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        
        schema = {}
        for table in tables:
            cursor = conn.execute(f"PRAGMA table_info({table})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    'name': row[1],
                    'type': row[2],
                    'nullable': not row[3]
                })
            schema[table] = columns
        
        conn.close()
        return schema
    
    def run_etl_validation_test(self, source_query: str, target_query: str) -> Dict[str, Any]:
        """
        Run ETL validation test comparing source and target queries
        
        Args:
            source_query: Query to get source data
            target_query: Query to get target/transformed data
        
        Returns:
            Comparison results with differences highlighted
        """
        source_result = self.execute_query(source_query)
        target_result = self.execute_query(target_query)
        
        if not source_result['success'] or not target_result['success']:
            return {
                'success': False,
                'error': 'One or both queries failed',
                'source_error': source_result.get('error'),
                'target_error': target_result.get('error')
            }
        
        return {
            'success': True,
            'source_count': source_result['row_count'],
            'target_count': target_result['row_count'],
            'count_match': source_result['row_count'] == target_result['row_count'],
            'source_data': source_result['rows'],
            'target_data': target_result['rows']
        }
    
    def get_data_profile(self, table_name: str) -> Dict[str, Any]:
        """
        Generate data profiling statistics for a table
        
        Args:
            table_name: Name of table to profile
        
        Returns:
            Statistics including row count, null counts, distinct values
        """
        table_name = self._sanitize_identifier(table_name)
        
        conn = self.create_sample_database()
        
        # Get row count
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        # Get column info
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        
        profile = {
            'table': table_name,
            'row_count': row_count,
            'columns': {}
        }
        
        # Profile each column
        for col in columns:
            cursor = conn.execute(f"""
                SELECT 
                    COUNT(*) as total,
                    COUNT(DISTINCT {col}) as distinct_count,
                    COUNT({col}) as non_null_count
                FROM {table_name}
            """)
            row = cursor.fetchone()
            
            null_count = row_count - row[2]
            
            profile['columns'][col] = {
                'distinct_values': row[1],
                'null_count': null_count,
                'null_percentage': round((null_count / row_count * 100), 2) if row_count > 0 else 0,
                'completeness': round((row[2] / row_count * 100), 2) if row_count > 0 else 0
            }
        
        conn.close()
        return profile
    
    def get_etl_test_templates(self) -> List[Dict[str, str]]:
        """Get common ETL test case templates"""
        return [
            {
                'name': 'Row Count Match',
                'description': 'Verify source and target have same row count',
                'source_query': 'SELECT COUNT(*) as count FROM customers',
                'target_query': 'SELECT COUNT(*) as count FROM customers',
                'expected': 'Counts should match'
            },
            {
                'name': 'NULL Handling',
                'description': 'Check NULL values are handled correctly',
                'source_query': 'SELECT customer_id, email FROM customers WHERE email IS NULL',
                'target_query': 'SELECT customer_id, COALESCE(email, \'no-email@domain.com\') as email FROM customers WHERE email IS NULL',
                'expected': 'NULLs replaced with default value'
            },
            {
                'name': 'String Transformation',
                'description': 'Verify string cleaning transformations',
                'source_query': 'SELECT phone FROM customers',
                'target_query': 'SELECT REPLACE(phone, \'-\', \'\') as phone_clean FROM customers',
                'expected': 'Hyphens removed from phone numbers'
            },
            {
                'name': 'Date Extraction',
                'description': 'Extract year/month from date fields',
                'source_query': 'SELECT created_date FROM customers',
                'target_query': 'SELECT SUBSTR(created_date, 1, 7) as year_month FROM customers',
                'expected': 'Extract YYYY-MM format'
            },
            {
                'name': 'Aggregation Validation',
                'description': 'Verify aggregated totals match detail level',
                'source_query': 'SELECT SUM(total_amount) as total FROM orders',
                'target_query': 'SELECT SUM(revenue) as total FROM (SELECT status, SUM(total_amount) as revenue FROM orders GROUP BY status)',
                'expected': 'Totals should match between detail and aggregate'
            }
        ]
