"""
Example usage of ETL Validator
"""
from src.etl_validator import ETLValidator


def main():
    # Initialize validator with mapping CSV file
    validator = ETLValidator('examples/sample_mapping.csv')
    
    # Load mappings
    print("Loading mapping document...")
    validator.load_mappings()
    
    # Get mapping summary
    summary = validator.get_mapping_summary()
    print(f"\nMapping Summary:")
    print(f"  Total mappings: {summary['total_mappings']}")
    print(f"  Source columns: {', '.join(summary['source_columns'])}")
    print(f"  Target columns: {', '.join(summary['target_columns'])}")
    
    # Generate validation queries
    print("\nGenerating validation queries...")
    queries = validator.generate_validation_queries(
        source_table='customers',
        target_table='customers_dim',
        source_schema='source_db',
        target_schema='target_db',
        query_type='both'
    )
    
    # Print generated queries
    print("\n" + "="*80)
    print("SOURCE MINUS TARGET QUERY:")
    print("="*80)
    print(queries['source_minus_target'])
    
    print("\n" + "="*80)
    print("TARGET MINUS SOURCE QUERY:")
    print("="*80)
    print(queries['target_minus_source'])
    
    # Save queries to files
    print("\nSaving queries to files...")
    with open('output/source_minus_target.sql', 'w') as f:
        f.write(queries['source_minus_target'])
    
    with open('output/target_minus_source.sql', 'w') as f:
        f.write(queries['target_minus_source'])
    
    with open('output/complete_validation.sql', 'w') as f:
        f.write(queries['complete'])
    
    print("✓ Queries saved to output/ directory")


if __name__ == '__main__':
    main()
