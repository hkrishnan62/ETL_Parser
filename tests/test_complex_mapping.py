"""
Test script to validate complex mapping CSV parsing and SQL generation
"""
from src.etl_validator import ETLValidator

def test_complex_mapping():
    print("=" * 80)
    print("Testing Complex Mapping CSV")
    print("=" * 80)
    
    # Initialize validator with complex mapping
    validator = ETLValidator('examples/complex_mapping.csv')
    
    # Load mappings
    print("\n1. Loading mappings...")
    validator.load_mappings()
    print("✓ Mappings loaded successfully")
    
    # Get summary
    print("\n2. Getting mapping summary...")
    summary = validator.get_mapping_summary()
    
    print(f"\n📊 Mapping Summary:")
    print(f"   Total mappings: {summary['total_mappings']}")
    print(f"   Detected source tables: {summary.get('detected_source_tables', [])}")
    print(f"   Source columns ({len(summary['source_columns'])}): {', '.join(summary['source_columns'][:5])}...")
    print(f"   Target columns ({len(summary['target_columns'])}): {', '.join(summary['target_columns'][:5])}...")
    
    # Use detected source table
    source_tables = summary.get('detected_source_tables', [])
    source_table = source_tables[0] if source_tables else 'source_table'
    target_table = 'orders_fact'
    
    print(f"\n3. Generating SQL queries...")
    print(f"   Source Table: {source_table}")
    print(f"   Target Table: {target_table}")
    
    # Generate queries
    queries = validator.generate_validation_queries(
        source_table=source_table,
        target_table=target_table,
        query_type='both'
    )
    
    print(f"\n✓ Generated {len(queries)} queries")
    
    # Display queries
    print("\n" + "=" * 80)
    print("Generated SQL Queries:")
    print("=" * 80)
    
    for query_name, query_sql in queries.items():
        print(f"\n{'=' * 40}")
        print(f"{query_name.upper()}")
        print(f"{'=' * 40}")
        print(query_sql)
        print()
    
    print("\n✅ Test completed successfully!")
    print("\nKey Transformations Found:")
    transformations = summary['transformations']
    for i, (target, transform) in enumerate(list(transformations.items())[:5], 1):
        print(f"{i}. {target}: {transform[:80]}...")

if __name__ == '__main__':
    test_complex_mapping()
