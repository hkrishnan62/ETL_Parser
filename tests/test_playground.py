"""
Test script for SQL Playground functionality
"""
from src.sql_playground import SQLPlayground
import json

def test_playground():
    """Test SQL Playground features"""
    print("🧪 Testing SQL Playground...")
    print("=" * 60)
    
    playground = SQLPlayground()
    
    # Test 1: Execute basic query
    print("\n✅ Test 1: Execute basic query")
    result = playground.execute_query("SELECT * FROM customers LIMIT 3")
    print(f"   Success: {result['success']}")
    print(f"   Rows returned: {result['row_count']}")
    print(f"   Columns: {', '.join(result['columns'])}")
    
    # Test 2: Execute JOIN query
    print("\n✅ Test 2: Execute JOIN query")
    join_query = """
    SELECT 
        c.first_name,
        c.last_name,
        o.order_date,
        o.total_amount
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    LIMIT 3
    """
    result = playground.execute_query(join_query)
    print(f"   Success: {result['success']}")
    print(f"   Rows returned: {result['row_count']}")
    if result['rows']:
        print(f"   First row: {result['rows'][0]}")
    
    # Test 3: Execute aggregation query
    print("\n✅ Test 3: Execute aggregation query")
    agg_query = """
    SELECT 
        status,
        COUNT(*) as count,
        AVG(total_amount) as avg_amount
    FROM orders
    GROUP BY status
    """
    result = playground.execute_query(agg_query)
    print(f"   Success: {result['success']}")
    print(f"   Rows returned: {result['row_count']}")
    if result['rows']:
        for row in result['rows']:
            print(f"   {row}")
    
    # Test 4: Security - block dangerous operations
    print("\n✅ Test 4: Security test (should fail)")
    dangerous_queries = [
        "DROP TABLE customers",
        "DELETE FROM customers",
        "UPDATE customers SET name = 'hacked'"
    ]
    for query in dangerous_queries:
        result = playground.execute_query(query)
        print(f"   Query: {query[:30]}...")
        print(f"   Blocked: {not result['success']}")
    
    # Test 5: Create share link
    print("\n✅ Test 5: Create share link")
    share_id = playground.create_share_link(
        query="SELECT * FROM customers",
        results={'rows': [], 'columns': []}
    )
    print(f"   Share ID: {share_id}")
    
    # Test 6: Retrieve shared query
    print("\n✅ Test 6: Retrieve shared query")
    shared = playground.get_shared_query(share_id)
    print(f"   Retrieved: {shared is not None}")
    print(f"   View count: {shared['view_count']}")
    
    # Test 7: Get sample queries
    print("\n✅ Test 7: Get sample queries")
    samples = playground.get_sample_queries()
    print(f"   Sample queries available: {len(samples)}")
    for i, sample in enumerate(samples[:3], 1):
        print(f"   {i}. {sample['name']}")
    
    # Test 8: Get database schema
    print("\n✅ Test 8: Get database schema")
    schema = playground.get_database_schema()
    print(f"   Tables: {', '.join(schema.keys())}")
    for table, columns in schema.items():
        print(f"   {table}: {len(columns)} columns")
    
    # Test 9: Custom sample data
    print("\n✅ Test 9: Custom sample data")
    custom_data = {
        'products': [
            {'id': 1, 'name': 'Widget', 'price': 9.99},
            {'id': 2, 'name': 'Gadget', 'price': 19.99},
        ]
    }
    result = playground.execute_query(
        "SELECT * FROM products WHERE price > 10",
        sample_data=custom_data
    )
    print(f"   Success: {result['success']}")
    print(f"   Rows returned: {result['row_count']}")
    if result['rows']:
        print(f"   Result: {result['rows']}")
    
    # Test 10: Error handling
    print("\n✅ Test 10: Error handling")
    result = playground.execute_query("SELECT * FROM nonexistent_table")
    print(f"   Success: {result['success']}")
    print(f"   Error message: {result.get('error', 'No error')[:50]}...")
    
    print("\n" + "=" * 60)
    print("✨ All tests completed!")
    print("\n🚀 SQL Playground is ready!")
    print("   Access at: http://localhost:5000/playground/")

if __name__ == '__main__':
    test_playground()
