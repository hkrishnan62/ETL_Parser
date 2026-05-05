# Quick Start Guide: Test Case Generation

## 3-Step Process to Generate Test Cases

### Step 1: Upload Your Mapping File
```
┌─────────────────────────────────────────────────┐
│  📁 Upload Mapping Document                     │
│                                                 │
│  [Click to upload or drag and drop]            │
│  CSV or Excel files (XLS, XLSX)                │
│                                                 │
│  ✓ Selected: sample_mapping.csv (2.3 KB)       │
└─────────────────────────────────────────────────┘

[Generate SQL Queries]
```

### Step 2: View Generated Test Case Section
```
After successful upload, you'll see:

┌─────────────────────────────────────────────────┐
│  📊 Mapping Summary                             │
│  Total Mappings: 9                              │
│  Source Columns: 9 (customer_id, first_name...) │
│  Target Columns: 9 (customer_id, full_name...)  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  🧪 Generate Test Cases                         │
│                                                 │
│  Create comprehensive test cases covering       │
│  positive and negative scenarios for your       │
│  ETL mapping.                                   │
│                                                 │
│  Test Type:     [All Test Cases         ▼]     │
│  Export Format: [qTest (CSV)            ▼]     │
│                                                 │
│  [👁️ Preview Test Cases] [📥 Download]         │
└─────────────────────────────────────────────────┘
```

### Step 3: Preview or Download
```
┌─────────────────────────────────────────────────┐
│  Test Case Preview                          [✕] │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  Positive: 12  │  Negative: 8  │  Total: 20│ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ✅ TC_POSITIVE_001                    High     │
│  Verify all columns are mapped from source to   │
│  target table                                   │
│  Validate that all 9 columns are correctly...   │
│  [📋 Test Steps (4)]                            │
│  Expected: All columns mapped correctly         │
│                                                 │
│  ❌ TC_NEGATIVE_001                    High     │
│  Verify handling of NULL values in source...    │
│  Validate ETL behavior when source columns...   │
│  [📋 Test Steps (4)]                            │
│  Expected: NULL values handled per rules        │
│                                                 │
│  ... (18 more test cases)                       │
└─────────────────────────────────────────────────┘
```

## Supported Formats

### 1. qTest (CSV)
```csv
Test Case ID,Name,Description,Precondition,Test Step Description,Expected Result...
TC_POSITIVE_001,"Verify all columns mapped","Validate mappings",...
```

### 2. Zephyr (CSV)
```csv
ID,Name,Objective,Precondition,Test Script,Priority,Component,Labels,Status
TC_POSITIVE_001,"Verify mappings","Validate columns",...
```

### 3. TestRail (CSV)
```csv
ID,Title,Section,Template,Type,Priority,Estimate,References,Automation Type...
TC_POSITIVE_001,"Verify all columns","ETL Mapping Tests",...
```

### 4. Azure DevOps / ADO (CSV)
```csv
Work Item Type,ID,Title,State,Priority,Area Path,Iteration Path,Description...
Test Case,TC_POSITIVE_001,"Verify mappings","Design",2,"ETL",...
```

### 5. JSON
```json
{
  "metadata": {
    "generated_at": "2026-01-28T...",
    "total_test_cases": 20
  },
  "test_cases": [
    {
      "test_id": "TC_POSITIVE_001",
      "name": "Verify all columns mapped",
      "description": "Validate mappings",
      "test_steps": [...],
      "expected_result": "All columns mapped correctly",
      "priority": "High"
    }
  ]
}
```

## Test Case Types

### Positive Test Cases (✅)
- All columns mapping validation
- Individual transformation tests
- Data type validation
- Large volume testing
- End-to-end validation

### Negative Test Cases (❌)
- NULL value handling
- Invalid data types
- Missing mandatory fields
- Duplicate records
- Data length constraints
- Special characters

## Import to Test Management Tools

### qTest
1. Login → Test Design → Import → CSV
2. Upload file → Map columns → Complete

### Zephyr
1. Jira → Tests → Import → CSV/Excel
2. Upload → Follow wizard → Complete

### TestRail
1. TestRail → Test Cases → Import → CSV
2. Upload → Complete import

### Azure DevOps
1. Azure DevOps → Test Plans → Import → CSV
2. Upload → Map fields → Complete

## Example Output

For a mapping with 9 columns, you'll get approximately:
- **12 Positive Test Cases**
  - 1 overall mapping validation
  - 9 individual column transformations
  - 1 data type validation
  - 1 large volume test

- **8 Negative Test Cases**
  - 1 NULL handling
  - 1 invalid data types
  - 3 missing column tests
  - 1 duplicate handling
  - 1 data length validation
  - 1 special characters

**Total: ~20 comprehensive test cases** ready to import!

## Tips

💡 Always preview before downloading
💡 Export positive and negative separately for better organization
💡 Customize test cases after import based on your needs
💡 Add specific test data values for your environment
💡 Regenerate when mappings change

## Support

Questions? Email: hkrishnan62@gmail.com
Issues? GitHub: https://github.com/hkrishnan62/ETL_Parser/issues

---
**Ready to try it?** Visit https://etl-mapping-converter-to-sql.onrender.com and upload your first mapping file!
