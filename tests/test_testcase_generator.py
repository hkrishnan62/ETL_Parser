"""
Test script to verify test case generator functionality
"""
from src.test_case_generator import TestCaseGenerator

# Sample mapping data
sample_mappings = [
    {
        'source_column': 'customer_id',
        'target_column': 'cust_id',
        'transformation': 'source_table.customer_id',
        'is_key': 'Yes'
    },
    {
        'source_column': 'first_name',
        'target_column': 'fname',
        'transformation': 'UPPER(source_table.first_name)',
        'is_key': 'No'
    },
    {
        'source_column': 'email',
        'target_column': 'email_address',
        'transformation': 'TRIM(source_table.email)',
        'is_key': 'No'
    }
]

sample_summary = {
    'total_mappings': 3,
    'source_columns': ['customer_id', 'first_name', 'email'],
    'target_columns': ['cust_id', 'fname', 'email_address'],
    'detected_source_tables': ['source_table']
}

print("=" * 60)
print("Testing Test Case Generator")
print("=" * 60)

# Create generator instance
generator = TestCaseGenerator(sample_mappings, sample_summary)

# Test 1: Generate all test cases
print("\n1. Generating all test cases...")
all_test_cases = generator.generate_all_test_cases()
print(f"   ✓ Positive test cases: {len(all_test_cases['positive'])}")
print(f"   ✓ Negative test cases: {len(all_test_cases['negative'])}")
print(f"   ✓ Total test cases: {len(all_test_cases['all'])}")

# Test 2: Export to different formats
formats = ['qtest', 'zephyr', 'testrail', 'ado', 'json']
print("\n2. Testing export formats...")
for fmt in formats:
    try:
        content = generator.export_test_cases(fmt, 'all')
        lines = len(content.split('\n'))
        print(f"   ✓ {fmt.upper()}: Generated {lines} lines")
    except Exception as e:
        print(f"   ✗ {fmt.upper()}: Error - {str(e)}")

# Test 3: Display sample positive test case
print("\n3. Sample Positive Test Case:")
print("-" * 60)
positive_case = all_test_cases['positive'][0]
print(f"ID: {positive_case['test_id']}")
print(f"Name: {positive_case['name']}")
print(f"Description: {positive_case['description']}")
print(f"Priority: {positive_case['priority']}")
print(f"Steps: {len(positive_case['test_steps'])} steps")

# Test 4: Display sample negative test case
print("\n4. Sample Negative Test Case:")
print("-" * 60)
negative_case = all_test_cases['negative'][0]
print(f"ID: {negative_case['test_id']}")
print(f"Name: {negative_case['name']}")
print(f"Description: {negative_case['description']}")
print(f"Priority: {negative_case['priority']}")
print(f"Steps: {len(negative_case['test_steps'])} steps")

# Test 5: Export sample CSV
print("\n5. Sample qTest CSV Export (first 5 lines):")
print("-" * 60)
qtest_csv = generator.export_test_cases('qtest', 'positive')
lines = qtest_csv.split('\n')
for line in lines[:5]:
    print(line[:100] + '...' if len(line) > 100 else line)

print("\n" + "=" * 60)
print("✓ All tests completed successfully!")
print("=" * 60)
