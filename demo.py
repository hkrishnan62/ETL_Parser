"""
Demo script showing different use cases of the ETL Validator
"""
from src.etl_validator import ETLValidator
import os


def demo_basic_usage():
    """Demo 1: Basic usage with simple mapping"""
    print("="*80)
    print("DEMO 1: Basic Usage")
    print("="*80)
    
    validator = ETLValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    summary = validator.get_mapping_summary()
    print(f"\n📊 Mapping Summary:")
    print(f"   Total Mappings: {summary['total_mappings']}")
    print(f"   Source Columns: {len(summary['source_columns'])}")
    print(f"   Target Columns: {len(summary['target_columns'])}")
    
    print("\n✓ Basic mapping loaded successfully!")


def demo_source_minus_target():
    """Demo 2: Generate Source MINUS Target query only"""
    print("\n" + "="*80)
    print("DEMO 2: Source MINUS Target Query")
    print("="*80)
    
    validator = ETLValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    queries = validator.generate_validation_queries(
        source_table='customer_source',
        target_table='customer_target',
        query_type='source_minus_target'
    )
    
    print("\n📝 Generated Query Preview (first 500 chars):")
    print(queries['source_minus_target'][:500] + "...")
    
    print("\n✓ Source MINUS Target query generated!")


def demo_complex_transformations():
    """Demo 3: Complex transformations"""
    print("\n" + "="*80)
    print("DEMO 3: Complex Transformations")
    print("="*80)
    
    validator = ETLValidator('examples/complex_mapping.csv')
    validator.load_mappings()
    
    summary = validator.get_mapping_summary()
    
    print(f"\n🔧 Complex Transformation Examples:")
    transformations = summary['transformations']
    
    for target_col, transform in list(transformations.items())[:5]:
        print(f"\n   {target_col}:")
        print(f"      {transform[:80]}...")
    
    print("\n✓ Complex transformations parsed successfully!")


def demo_with_schemas():
    """Demo 4: Using schema names"""
    print("\n" + "="*80)
    print("DEMO 4: With Schema Names")
    print("="*80)
    
    validator = ETLValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    queries = validator.generate_validation_queries(
        source_table='customers',
        target_table='customers_dim',
        source_schema='sales_db',
        target_schema='analytics_dw',
        query_type='both'
    )
    
    # Check if schemas are in the queries
    has_schema = 'sales_db' in queries['complete'] and 'analytics_dw' in queries['complete']
    
    print(f"\n✓ Generated queries with schema names")
    print(f"   Source Schema: sales_db")
    print(f"   Target Schema: analytics_dw")
    print(f"   Schema References: {'✓ Present' if has_schema else '✗ Missing'}")


def demo_save_queries():
    """Demo 5: Save queries to files"""
    print("\n" + "="*80)
    print("DEMO 5: Save Queries to Files")
    print("="*80)
    
    validator = ETLValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    queries = validator.generate_validation_queries(
        source_table='orders',
        target_table='orders_fact',
        source_schema='oltp',
        target_schema='olap',
        query_type='both'
    )
    
    # Create output directory if needed
    os.makedirs('output/demo', exist_ok=True)
    
    # Save queries
    files_saved = []
    for query_type, query_sql in queries.items():
        filename = f'output/demo/{query_type}.sql'
        with open(filename, 'w') as f:
            f.write(query_sql)
        files_saved.append(filename)
    
    print(f"\n💾 Saved {len(files_saved)} query files:")
    for filename in files_saved:
        print(f"   ✓ {filename}")


def run_all_demos():
    """Run all demonstrations"""
    print("\n" + "🎬 ETL VALIDATOR - DEMONSTRATION SUITE")
    print("="*80)
    
    demos = [
        demo_basic_usage,
        demo_source_minus_target,
        demo_complex_transformations,
        demo_with_schemas,
        demo_save_queries
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n✗ Demo failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("🎉 All demonstrations completed!")
    print("="*80)
    print("\n💡 Try the web interface by running: python app.py")
    print("   Then open: http://localhost:5000")


if __name__ == '__main__':
    run_all_demos()
