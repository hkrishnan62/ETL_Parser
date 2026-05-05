"""
Standalone SQL Playground Demo
No Flask or web server required - pure Python usage
"""
from src.sql_playground import SQLPlayground


def main():
    """Demonstrate standalone SQL Playground usage"""
    
    print("🎮 SQL Playground - Standalone Demo")
    print("=" * 60)
    
    # Initialize playground (no Flask needed!)
    playground = SQLPlayground()
    
    # Example 1: Basic query
    print("\n📊 Example 1: Basic Customer Query")
    print("-" * 60)
    result = playground.execute_query("SELECT * FROM customers LIMIT 3")
    
    if result['success']:
        print(f"✓ Query executed successfully")
        print(f"✓ Returned {result['row_count']} rows")
        print(f"✓ Columns: {', '.join(result['columns'])}")
        print("\nResults:")
        for i, row in enumerate(result['rows'], 1):
            print(f"  {i}. {row}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Example 2: JOIN query
    print("\n📊 Example 2: JOIN Query")
    print("-" * 60)
    join_query = """
    SELECT 
        c.first_name,
        c.last_name,
        o.order_date,
        o.total_amount,
        o.status
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    ORDER BY o.order_date DESC
    LIMIT 5
    """
    
    result = playground.execute_query(join_query)
    if result['success']:
        print(f"✓ Found {result['row_count']} orders")
        for row in result['rows']:
            print(f"  • {row['first_name']} {row['last_name']}: ${row['total_amount']} ({row['status']})")
    
    # Example 3: Aggregation
    print("\n📊 Example 3: Aggregation Query")
    print("-" * 60)
    agg_query = """
    SELECT 
        status,
        COUNT(*) as order_count,
        ROUND(AVG(total_amount), 2) as avg_amount,
        SUM(total_amount) as total_revenue
    FROM orders
    GROUP BY status
    ORDER BY total_revenue DESC
    """
    
    result = playground.execute_query(agg_query)
    if result['success']:
        print(f"✓ Order statistics by status:")
        for row in result['rows']:
            print(f"  • {row['status']}: {row['order_count']} orders, "
                  f"avg ${row['avg_amount']}, total ${row['total_revenue']}")
    
    # Example 4: ETL Transformation
    print("\n📊 Example 4: ETL Transformation")
    print("-" * 60)
    etl_query = """
    SELECT 
        customer_id,
        UPPER(first_name) || ' ' || UPPER(last_name) as full_name_upper,
        LOWER(email) as email_normalized,
        REPLACE(phone, '-', '') as phone_clean
    FROM customers
    LIMIT 3
    """
    
    result = playground.execute_query(etl_query)
    if result['success']:
        print(f"✓ Transformed {result['row_count']} customers:")
        for row in result['rows']:
            print(f"  • {row['full_name_upper']}: {row['email_normalized']}")
    
    # Example 5: Security - blocked operations
    print("\n🔒 Example 5: Security Test")
    print("-" * 60)
    dangerous_queries = [
        "DROP TABLE customers",
        "DELETE FROM orders",
        "UPDATE customers SET email = 'hacked@bad.com'"
    ]
    
    for query in dangerous_queries:
        result = playground.execute_query(query)
        status = "✓ BLOCKED" if not result['success'] else "✗ ALLOWED"
        print(f"  {status}: {query}")
    
    # Example 6: Create shareable link (works without Flask)
    print("\n🔗 Example 6: Share Functionality")
    print("-" * 60)
    share_id = playground.create_share_link(
        query="SELECT * FROM customers WHERE created_date >= '2024-01-01'",
        results={'rows': [], 'columns': [], 'row_count': 5}
    )
    print(f"✓ Share link created: {share_id}")
    
    # Retrieve shared query
    shared = playground.get_shared_query(share_id)
    print(f"✓ Retrieved shared query")
    print(f"  • Query: {shared['query'][:50]}...")
    print(f"  • View count: {shared['view_count']}")
    print(f"  • Created: {shared['created_at']}")
    
    # Example 7: Custom sample data
    print("\n📊 Example 7: Custom Sample Data")
    print("-" * 60)
    custom_data = {
        'products': [
            {'id': 1, 'name': 'Widget', 'price': 9.99, 'category': 'Tools'},
            {'id': 2, 'name': 'Gadget', 'price': 19.99, 'category': 'Electronics'},
            {'id': 3, 'name': 'Doohickey', 'price': 14.99, 'category': 'Tools'},
        ]
    }
    
    result = playground.execute_query(
        "SELECT category, COUNT(*) as count, AVG(price) as avg_price FROM products GROUP BY category",
        sample_data=custom_data
    )
    
    if result['success']:
        print(f"✓ Custom data query executed:")
        for row in result['rows']:
            print(f"  • {row['category']}: {row['count']} items, avg ${row['avg_price']:.2f}")
    
    # Example 8: Get available samples
    print("\n📚 Example 8: Sample Query Library")
    print("-" * 60)
    samples = playground.get_sample_queries()
    print(f"✓ Available samples: {len(samples)}")
    for i, sample in enumerate(samples[:3], 1):
        print(f"  {i}. {sample['name']}: {sample['description']}")
    
    # Example 9: Database schema
    print("\n🗄️ Example 9: Database Schema")
    print("-" * 60)
    schema = playground.get_database_schema()
    print(f"✓ Available tables: {', '.join(schema.keys())}")
    for table, columns in schema.items():
        print(f"  • {table}:")
        for col in columns[:3]:  # Show first 3 columns
            print(f"    - {col['name']} ({col['type']})")
    
    print("\n" + "=" * 60)
    print("✨ All examples completed successfully!")
    print("\n💡 Key Points:")
    print("   • No Flask or web server required")
    print("   • Pure Python API")
    print("   • Sandboxed SQL execution")
    print("   • Built-in security")
    print("   • Custom data support")
    print("   • Share functionality included")
    print("\n🚀 Use it in your scripts, notebooks, or applications!")


if __name__ == '__main__':
    main()
