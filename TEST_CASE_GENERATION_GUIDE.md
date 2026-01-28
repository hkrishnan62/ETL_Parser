# Test Case Generation Feature

## Overview

The ETL Parser now includes an automated test case generation feature that creates comprehensive test cases for your ETL mapping documents. This feature helps QA teams and data engineers quickly generate test scenarios in multiple industry-standard formats.

## Features

### 🎯 Test Case Types

1. **Positive Test Cases**
   - Validate all columns are mapped correctly
   - Individual column transformation validation
   - Data type preservation/conversion tests
   - Large volume data processing tests
   - End-to-end ETL validation

2. **Negative Test Cases**
   - NULL value handling
   - Invalid data type rejection
   - Missing mandatory columns
   - Duplicate record handling
   - Data length/size constraint validation
   - Special character handling

### 📋 Supported Export Formats

The test cases can be exported in the following formats:

1. **qTest** (CSV) - Compatible with qTest test management platform
2. **Zephyr** (CSV) - Compatible with Zephyr for Jira
3. **TestRail** (CSV) - Compatible with TestRail test management
4. **Azure DevOps / ADO** (CSV) - Compatible with Azure DevOps Test Plans
5. **JSON** - Universal format for custom integrations

## How to Use

### Step 1: Upload Your Mapping Document

1. Navigate to the ETL Parser website
2. Upload your CSV or Excel mapping file
3. Configure the source and target settings
4. Click "Generate SQL Queries"

### Step 2: Generate Test Cases

Once your mapping is processed, you'll see a new section: **🧪 Generate Test Cases**

1. **Select Test Type:**
   - All Test Cases (both positive and negative)
   - Positive Test Cases Only
   - Negative Test Cases Only

2. **Select Export Format:**
   - Choose from qTest, Zephyr, TestRail, ADO, or JSON

### Step 3: Preview or Download

- **Preview Test Cases**: Click to see all generated test cases in a readable format
- **Download Test Cases**: Download the test cases in your selected format

## Test Case Structure

Each generated test case includes:

- **Test Case ID**: Unique identifier (e.g., TC_POSITIVE_001, TC_NEGATIVE_001)
- **Name**: Descriptive test case title
- **Description**: Detailed description of what is being tested
- **Preconditions**: Requirements before test execution
- **Test Steps**: Step-by-step instructions
- **Expected Result**: What should happen when test passes
- **Priority**: High, Medium, or Low
- **Type**: Functional, Performance, or Negative
- **Category**: Positive or Negative

## Example Test Cases

### Positive Test Case Example

```
Test ID: TC_POSITIVE_001
Name: Verify all columns are mapped from source_table to target_table
Description: Validate that all columns are correctly mapped with specified transformations
Priority: High
Type: Functional

Preconditions:
- Source table contains valid data
- ETL process is configured and ready
- Target table structure is created

Test Steps:
1. Load sample data into source_table
2. Execute ETL process
3. Query target table
4. Compare source and target data

Expected Result: All columns are mapped correctly with transformations applied
```

### Negative Test Case Example

```
Test ID: TC_NEGATIVE_001
Name: Verify handling of NULL values in source columns
Description: Validate ETL behavior when source columns contain NULL values
Priority: High
Type: Negative

Preconditions:
- Source table accepts NULL values
- NULL handling rules are defined

Test Steps:
1. Insert records with NULL values in various columns
2. Execute ETL process
3. Verify error handling or default value assignment
4. Check target table for NULL or default values

Expected Result: NULL values are handled according to business rules
```

## Import Instructions

### qTest Import

1. Log in to qTest
2. Navigate to Test Design
3. Click Import
4. Select CSV format
5. Upload the downloaded CSV file
6. Map the columns if prompted
7. Complete the import

### Zephyr Import

1. Open Jira with Zephyr
2. Go to Tests section
3. Click Import
4. Select CSV/Excel format
5. Upload the file
6. Follow the mapping wizard
7. Complete the import

### TestRail Import

1. Log in to TestRail
2. Go to your test project
3. Navigate to Test Cases
4. Click on Import
5. Select CSV format
6. Upload the file
7. Complete the import process

### Azure DevOps (ADO) Import

1. Open Azure DevOps
2. Navigate to Test Plans
3. Select your test plan
4. Click on Import
5. Choose CSV format
6. Upload the file
7. Map fields and complete import

### JSON Format

The JSON format provides maximum flexibility:

```json
{
  "metadata": {
    "generated_at": "2026-01-28T...",
    "source_table": "source_table",
    "target_table": "target_table",
    "total_mappings": 3,
    "total_test_cases": 14
  },
  "test_cases": [
    {
      "test_id": "TC_POSITIVE_001",
      "name": "...",
      "description": "...",
      "preconditions": [...],
      "test_steps": [...],
      "expected_result": "...",
      "priority": "High",
      "type": "Functional",
      "category": "Positive"
    }
  ]
}
```

## Benefits

✅ **Save Time**: Generate dozens of test cases in seconds instead of hours
✅ **Comprehensive Coverage**: Both positive and negative scenarios automatically created
✅ **Consistent Quality**: Standardized test case structure and naming
✅ **Multiple Formats**: Export to your preferred test management tool
✅ **Easy Maintenance**: Regenerate test cases when mappings change
✅ **Best Practices**: Built-in testing best practices and patterns

## API Endpoints

For programmatic access:

### Preview Test Cases
```
POST /preview-test-cases
Content-Type: application/json

{
  "mappings": [...],
  "summary": {...},
  "test_type": "all"
}
```

### Generate/Download Test Cases
```
POST /generate-test-cases
Content-Type: application/json

{
  "mappings": [...],
  "summary": {...},
  "test_type": "all",
  "format": "qtest"
}
```

## Tips

1. **Start with Preview**: Always preview test cases before downloading to verify they meet your needs
2. **Customize After Export**: The generated test cases provide a solid foundation - customize them based on your specific requirements
3. **Combine Test Types**: Export both positive and negative test cases separately for better organization
4. **Update Test Data**: Add specific test data values based on your actual data
5. **Review Priorities**: Adjust test case priorities based on your project needs

## Support

For questions or issues with the test case generation feature:
- Email: hkrishnan62@gmail.com
- GitHub: https://github.com/hkrishnan62/ETL_Parser/issues

## Version

Feature added: January 2026
Current version: 1.0
