# Quick Start Guide

## Getting Started with ETL Mapping Validator

### 1. Web Interface (Recommended for beginners)

The easiest way to use the ETL Mapping Validator is through the web interface.

**Steps:**

1. Start the application:
```bash
python app.py
```

2. Open your browser and go to: `http://localhost:5000`

3. You'll see a user-friendly interface where you can:
   - Upload your CSV mapping file
   - Configure source and target table names
   - Specify schema names (optional)
   - Choose the type of validation query you need

4. Click "Generate SQL Queries" and download your validation queries!

### 2. Command Line Usage

For automation and integration into pipelines:

```python
from src.etl_validator import ETLValidator

# Create validator instance
validator = ETLValidator('examples/sample_mapping.csv')

# Load the mapping document
validator.load_mappings()

# Generate validation queries
queries = validator.generate_validation_queries(
    source_table='customers',
    target_table='customers_dim',
    source_schema='source_db',
    target_schema='target_db',
    query_type='both'
)

# Use the generated queries
print(queries['source_minus_target'])
print(queries['target_minus_source'])
```

## Creating Your Mapping CSV

Your CSV file must have these columns:

- **source_column**: The column name in the source table
- **target_column**: The column name in the target table
- **transformation**: SQL expression to transform the data (optional)
- **is_key**: TRUE if this column is used for joining (optional)

### Example:

```csv
source_column,target_column,transformation,is_key
id,customer_id,source_table.id,TRUE
fname,full_name,"CONCAT(source_table.fname, ' ', source_table.lname)",FALSE
email,email_address,LOWER(TRIM(source_table.email)),FALSE
```

## Understanding the Output

The tool generates three types of queries:

### 1. Source MINUS Target Query
Shows records that exist in source but not in target after transformation.
- **Use case**: Find data that didn't load properly into target

### 2. Target MINUS Source Query
Shows records that exist in target but not in transformed source.
- **Use case**: Find extra or unexpected data in target

### 3. Complete Validation Query
Combines both queries for full bidirectional validation.
- **Use case**: Complete reconciliation report

## Tips and Best Practices

1. **Mark Key Columns**: Always mark join key columns with `is_key=TRUE` for accurate results

2. **Test Transformations**: Start with simple transformations and test incrementally

3. **Use Schemas**: Specify schema names for clarity and to avoid ambiguity

4. **Save Queries**: Save generated queries for reuse and version control

5. **Validate Regularly**: Run validation queries after each ETL run

## Common Transformations

Here are examples of transformations you can use:

```csv
# String Concatenation
fname,full_name,"CONCAT(source_table.fname, ' ', source_table.lname)",FALSE

# Case Statement
status,status_code,"CASE WHEN source_table.status = 'A' THEN 'ACTIVE' ELSE 'INACTIVE' END",FALSE

# Type Casting
date_str,date_value,"CAST(source_table.date_str AS DATE)",FALSE

# String Functions
email,email_clean,"LOWER(TRIM(source_table.email))",FALSE

# Mathematical Operations
price,price_rounded,"ROUND(source_table.price, 2)",FALSE

# Regular Expression
phone,phone_digits,"REGEXP_REPLACE(source_table.phone, '[^0-9]', '')",FALSE
```

## Troubleshooting

**Problem**: CSV upload fails
- **Solution**: Ensure your CSV has the required columns and is properly formatted

**Problem**: Generated query doesn't work
- **Solution**: Check that your transformation syntax matches your database SQL dialect

**Problem**: No records returned
- **Solution**: Verify that source and target tables have data and schemas are correct

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review the [sample_mapping.csv](examples/sample_mapping.csv) for examples
- Run [example_usage.py](example_usage.py) to see a working example

---

Happy ETL Testing! 🚀
