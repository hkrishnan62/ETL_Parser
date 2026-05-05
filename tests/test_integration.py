"""
Integration test for test case generation feature
Tests the full workflow from mapping upload to test case generation
"""
import requests
import json
import os

# Base URL - update if needed
BASE_URL = "https://etl-mapping-converter-to-sql.onrender.com"  # Production
# BASE_URL = "http://localhost:5000"  # Local development

print("=" * 70)
print("ETL Parser - Test Case Generation Integration Test")
print("=" * 70)

# Step 1: Upload a mapping file
print("\n1. Uploading sample mapping file...")
file_path = "examples/sample_mapping.csv"

if not os.path.exists(file_path):
    print(f"   ✗ Error: File {file_path} not found")
    exit(1)

with open(file_path, 'rb') as f:
    files = {'file': ('sample_mapping.csv', f, 'text/csv')}
    data = {
        'target_table': 'target_table',
        'source_schema': '',
        'target_schema': '',
        'database_type': 'generic',
        'query_type': 'both',
        'use_ai': 'false'
    }
    
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"   ✓ Upload successful")
    print(f"   ✓ Total mappings: {result['summary']['total_mappings']}")
    print(f"   ✓ Source columns: {len(result['summary']['source_columns'])}")
    print(f"   ✓ Target columns: {len(result['summary']['target_columns'])}")
    
    # Store mapping data for test case generation
    mappings = result['summary'].get('mappings', [])
    summary = result['summary']
else:
    print(f"   ✗ Upload failed: {response.status_code}")
    print(f"   Error: {response.text}")
    exit(1)

# Step 2: Preview test cases
print("\n2. Previewing test cases...")
preview_data = {
    'mappings': mappings,
    'summary': summary,
    'test_type': 'all'
}

response = requests.post(
    f"{BASE_URL}/preview-test-cases",
    json=preview_data,
    headers={'Content-Type': 'application/json'}
)

if response.status_code == 200:
    result = response.json()
    print(f"   ✓ Preview successful")
    print(f"   ✓ Positive test cases: {result['positive_count']}")
    print(f"   ✓ Negative test cases: {result['negative_count']}")
    print(f"   ✓ Total test cases: {result['total_count']}")
    
    # Display a sample test case
    if result['test_cases']:
        sample_tc = result['test_cases'][0]
        print(f"\n   Sample Test Case:")
        print(f"   - ID: {sample_tc['test_id']}")
        print(f"   - Name: {sample_tc['name']}")
        print(f"   - Priority: {sample_tc['priority']}")
        print(f"   - Type: {sample_tc['type']}")
else:
    print(f"   ✗ Preview failed: {response.status_code}")
    print(f"   Error: {response.text}")

# Step 3: Generate test cases in different formats
print("\n3. Generating test cases in various formats...")
formats = ['qtest', 'zephyr', 'testrail', 'ado', 'json']

for fmt in formats:
    gen_data = {
        'mappings': mappings,
        'summary': summary,
        'test_type': 'all',
        'format': fmt
    }
    
    response = requests.post(
        f"{BASE_URL}/generate-test-cases",
        json=gen_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        if fmt == 'json':
            result = response.json()
            print(f"   ✓ {fmt.upper()}: Generated {result['test_case_count']} test cases")
        else:
            content = response.content
            lines = content.decode('utf-8').count('\n')
            print(f"   ✓ {fmt.upper()}: Generated CSV with {lines} lines")
    else:
        print(f"   ✗ {fmt.upper()}: Failed - {response.status_code}")

# Step 4: Test specific test types
print("\n4. Testing specific test case types...")
test_types = ['positive', 'negative']

for test_type in test_types:
    gen_data = {
        'mappings': mappings,
        'summary': summary,
        'test_type': test_type,
        'format': 'json'
    }
    
    response = requests.post(
        f"{BASE_URL}/generate-test-cases",
        json=gen_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ {test_type.upper()}: Generated {result['test_case_count']} test cases")
    else:
        print(f"   ✗ {test_type.upper()}: Failed")

print("\n" + "=" * 70)
print("✓ All integration tests completed successfully!")
print("=" * 70)
print("\nNext steps:")
print("1. Open https://etl-mapping-converter-to-sql.onrender.com in your browser")
print("2. Upload a mapping file")
print("3. Look for the '🧪 Generate Test Cases' section")
print("4. Try the Preview and Download features")
print("=" * 70)
