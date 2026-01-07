"""
Test Suite for ETL Validator
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.etl_validator import ETLValidator
from src.mapping_parser import MappingParser
from src.sql_generator import SQLGenerator


def test_mapping_parser():
    """Test CSV parsing functionality"""
    print("Testing Mapping Parser...")
    
    parser = MappingParser('examples/sample_mapping.csv')
    mappings = parser.parse()
    
    assert len(mappings) > 0, "No mappings loaded"
    assert 'source_column' in mappings[0], "Missing source_column"
    assert 'target_column' in mappings[0], "Missing target_column"
    
    source_cols = parser.get_source_columns()
    target_cols = parser.get_target_columns()
    
    assert len(source_cols) > 0, "No source columns found"
    assert len(target_cols) > 0, "No target columns found"
    
    print("✓ Mapping Parser tests passed")


def test_sql_generator():
    """Test SQL generation functionality"""
    print("\nTesting SQL Generator...")
    
    parser = MappingParser('examples/sample_mapping.csv')
    mappings = parser.parse()
    
    generator = SQLGenerator(mappings)
    
    # Test source minus target query
    query1 = generator.generate_source_minus_target('src_table', 'tgt_table')
    assert 'source_transformed' in query1, "Missing CTE"
    assert 'EXCEPT' in query1, "Missing EXCEPT clause"
    
    # Test target minus source query
    query2 = generator.generate_target_minus_source('src_table', 'tgt_table')
    assert 'target_data' in query2, "Missing target CTE"
    
    # Test complete validation
    query3 = generator.generate_complete_validation('src_table', 'tgt_table')
    assert 'Source MINUS Target' in query3, "Missing source minus target"
    assert 'Target MINUS Source' in query3, "Missing target minus source"
    
    print("✓ SQL Generator tests passed")


def test_etl_validator():
    """Test complete ETL validation workflow"""
    print("\nTesting ETL Validator...")
    
    validator = ETLValidator('examples/sample_mapping.csv')
    validator.load_mappings()
    
    summary = validator.get_mapping_summary()
    assert summary['total_mappings'] > 0, "No mappings loaded"
    
    queries = validator.generate_validation_queries(
        source_table='test_source',
        target_table='test_target',
        query_type='both'
    )
    
    assert 'source_minus_target' in queries, "Missing source minus target query"
    assert 'target_minus_source' in queries, "Missing target minus source query"
    assert 'complete' in queries, "Missing complete query"
    
    print("✓ ETL Validator tests passed")


def test_transformations():
    """Test various transformation types"""
    print("\nTesting Transformations...")
    
    test_mappings = [
        {
            'source_column': 'col1',
            'target_column': 'col1_out',
            'transformation': 'source_table.col1',
            'is_key': True
        },
        {
            'source_column': 'col2',
            'target_column': 'col2_concat',
            'transformation': "CONCAT(source_table.col2, ' - ', source_table.col3)",
            'is_key': False
        },
        {
            'source_column': 'col3',
            'target_column': 'col3_case',
            'transformation': "CASE WHEN source_table.col3 > 100 THEN 'HIGH' ELSE 'LOW' END",
            'is_key': False
        }
    ]
    
    generator = SQLGenerator(test_mappings)
    query = generator.generate_source_minus_target('test', 'test')
    
    assert 'CONCAT' in query, "CONCAT transformation not found"
    assert 'CASE WHEN' in query, "CASE transformation not found"
    
    print("✓ Transformation tests passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running ETL Validator Test Suite")
    print("=" * 60)
    
    try:
        test_mapping_parser()
        test_sql_generator()
        test_etl_validator()
        test_transformations()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {str(e)}")
        return False
    except Exception as e:
        print(f"\n✗ Error running tests: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
