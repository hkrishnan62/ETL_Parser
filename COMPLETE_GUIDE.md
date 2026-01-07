# 🎯 ETL Mapping Validator - Complete Guide

## What This Application Does

This application **automatically converts ETL mapping documents (CSV files) into SQL validation queries** that can be used to verify data transformations between source and target systems.

### The Problem It Solves

In ETL processes, you need to validate that:
1. All data from source made it to target (with transformations applied)
2. No extra data exists in target that shouldn't be there
3. Transformations were applied correctly

Traditionally, writing these validation queries manually is:
- ⏰ Time-consuming
- 🐛 Error-prone
- 🔄 Repetitive for each mapping change

### The Solution

Upload a CSV mapping document → Get production-ready SQL validation queries instantly!

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Application
```bash
python app.py
```

### Step 2: Open Your Browser
Navigate to: **http://localhost:5000**

### Step 3: Upload and Generate
1. Upload your CSV mapping file
2. Configure table/schema names
3. Click "Generate SQL Queries"
4. Copy and use the generated SQL!

---

## 📋 CSV Mapping Format

Your CSV file should have these columns:

```csv
source_column,target_column,transformation,is_key
customer_id,customer_id,source_table.customer_id,TRUE
first_name,full_name,"CONCAT(source_table.first_name, ' ', source_table.last_name)",FALSE
email,email_address,LOWER(TRIM(source_table.email)),FALSE
```

### Column Descriptions

| Column | Purpose | Required | Example |
|--------|---------|----------|---------|
| **source_column** | Column in source table | Yes* | `customer_id`, `first_name` |
| **target_column** | Column in target table | Yes | `customer_id`, `full_name` |
| **transformation** | SQL expression to transform data | No | `CONCAT(source_table.first_name, ' ', source_table.last_name)` |
| **is_key** | Used for joining tables | No | `TRUE`, `FALSE` |

*Can be empty for calculated/derived fields

---

## 🔧 Supported Transformations

### String Operations
```csv
# Concatenation
first_name,full_name,"CONCAT(source_table.first_name, ' ', source_table.last_name)"

# Case conversion
email,email_lower,LOWER(source_table.email)
region,region_upper,UPPER(source_table.region)

# Trimming
name,name_trimmed,TRIM(source_table.name)

# Combining multiple
email,email_clean,"LOWER(TRIM(source_table.email))"

# Advanced concatenation
address,full_address,"CONCAT_WS(', ', source_table.street, source_table.city, source_table.state)"
```

### Conditional Logic
```csv
# Simple case
status,status_desc,"CASE WHEN source_table.status = 'A' THEN 'ACTIVE' ELSE 'INACTIVE' END"

# Multiple conditions
priority,priority_level,"CASE WHEN source_table.amount > 1000 THEN 'HIGH' WHEN source_table.amount > 500 THEN 'MEDIUM' ELSE 'LOW' END"
```

### Date & Time
```csv
# Type conversion
date_string,date_value,"CAST(source_table.date_string AS DATE)"

# Timestamp conversion
date_str,timestamp_value,"TO_TIMESTAMP(source_table.date_str, 'YYYY-MM-DD')"

# Extract parts
order_date,order_year,"EXTRACT(YEAR FROM source_table.order_date)"
order_date,order_month,"EXTRACT(MONTH FROM source_table.order_date)"
```

### Numeric Operations
```csv
# Rounding
price,price_rounded,"ROUND(source_table.price, 2)"

# Type casting
amount,amount_decimal,"CAST(source_table.amount AS DECIMAL(10,2))"

# Calculations
,total_amount,"(source_table.quantity * source_table.unit_price) - COALESCE(source_table.discount, 0)"

# Percentage conversion
discount_decimal,discount_pct,"source_table.discount_decimal * 100"
```

### NULL Handling
```csv
# Default values
discount,discount_value,"COALESCE(source_table.discount, 0)"

# NULL replacement
middle_name,middle_initial,"COALESCE(source_table.middle_name, 'N/A')"
```

### Regular Expressions
```csv
# Remove non-numeric characters
phone,phone_digits,"REGEXP_REPLACE(source_table.phone, '[^0-9]', '')"

# Clean special characters
product,product_clean,"REGEXP_REPLACE(source_table.product, '[^a-zA-Z0-9 ]', '')"
```

### Calculated Fields
```csv
# No source column needed - leave empty
,total_sales,"(source_table.quantity * source_table.price)"
,profit_margin,"((source_table.revenue - source_table.cost) / source_table.revenue) * 100"
```

---

## 📊 Generated Query Types

### 1. Source MINUS Target
**Purpose**: Find records that exist in source but are missing in target after transformation

**Use When**:
- Checking if all source records were loaded
- Identifying failed transformations
- Detecting incomplete ETL runs

**Example Output**:
```sql
WITH source_transformed AS (
  SELECT
    source_table.customer_id AS customer_id,
    CONCAT(source_table.first_name, ' ', source_table.last_name) AS full_name
  FROM source_db.customers source_table
),
target_data AS (
  SELECT * FROM target_db.customers_dim
)
SELECT * FROM source_transformed
EXCEPT
SELECT * FROM target_data;
```

### 2. Target MINUS Source
**Purpose**: Find records in target that don't exist in transformed source

**Use When**:
- Detecting duplicate loads
- Identifying unexpected data in target
- Finding orphaned records

### 3. Complete Validation
**Purpose**: Both queries combined for comprehensive bidirectional validation

**Use When**:
- Full reconciliation required
- Audit purposes
- Production validation

---

## 💡 Usage Examples

### Example 1: Basic Customer Mapping

**Input CSV**: `customer_mapping.csv`
```csv
source_column,target_column,transformation,is_key
id,customer_id,source_table.id,TRUE
fname,first_name,TRIM(source_table.fname),FALSE
lname,last_name,TRIM(source_table.lname),FALSE
email,email,LOWER(source_table.email),FALSE
```

**Web Interface Configuration**:
- Source Table: `customers`
- Target Table: `dim_customer`
- Source Schema: `source_db`
- Target Schema: `target_dw`
- Query Type: `Both`

**Result**: Three SQL queries ready to execute!

### Example 2: Order Fact Table

**Input CSV**: `order_mapping.csv`
```csv
source_column,target_column,transformation,is_key
order_id,order_key,source_table.order_id,TRUE
customer_id,customer_key,source_table.customer_id,FALSE
order_date,order_date_key,"TO_CHAR(source_table.order_date, 'YYYYMMDD')",FALSE
quantity,quantity,source_table.quantity,FALSE
unit_price,unit_price,source_table.unit_price,FALSE
,total_amount,"source_table.quantity * source_table.unit_price",FALSE
```

### Example 3: Complex Product Transformation

**Input CSV**: `product_mapping.csv`
```csv
source_column,target_column,transformation,is_key
product_id,product_key,source_table.product_id,TRUE
product_name,product_name_clean,"UPPER(TRIM(REGEXP_REPLACE(source_table.product_name, '[^a-zA-Z0-9 ]', '')))",FALSE
category_code,category_name,"CASE WHEN source_table.category_code = 'E' THEN 'ELECTRONICS' WHEN source_table.category_code = 'C' THEN 'CLOTHING' ELSE 'OTHER' END",FALSE
price_usd,price_local,"source_table.price_usd * source_table.exchange_rate",FALSE
is_active,active_flag,"CASE WHEN source_table.is_active = 1 THEN TRUE ELSE FALSE END",FALSE
```

---

## 🎓 Best Practices

### 1. Always Mark Key Columns
```csv
customer_id,customer_id,source_table.customer_id,TRUE
order_id,order_id,source_table.order_id,TRUE
```
This ensures accurate JOIN conditions in validation queries.

### 2. Use Consistent Naming
```csv
# Good
source_table.column_name

# Avoid mixing
some_table.col1
source_table.col2
```

### 3. Test Complex Transformations Separately
For complex expressions, test them in your database first:
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM test_table LIMIT 5;
```

### 4. Document Your Transformations
Add comments in your mapping CSV:
```csv
# Customer demographic transformations
source_column,target_column,transformation,is_key
customer_id,customer_key,source_table.customer_id,TRUE
```

### 5. Handle NULLs Explicitly
```csv
# Use COALESCE for required fields
discount,discount_amount,"COALESCE(source_table.discount, 0)",FALSE
```

### 6. Save Generated Queries
Always save your generated SQL queries for:
- Version control
- Documentation
- Reuse in CI/CD pipelines

---

## 🔍 Troubleshooting

### Issue: "No file provided" Error
**Solution**: Ensure you've selected a CSV file before clicking Generate

### Issue: "Invalid file type" Error
**Solution**: File must be `.csv` extension

### Issue: Generated Query Syntax Error
**Cause**: Transformation contains database-specific syntax
**Solution**: Adjust transformation to match your database SQL dialect

### Issue: No Records in JOIN Key Column
**Cause**: No columns marked as `is_key=TRUE`
**Solution**: Mark at least one column as a join key

### Issue: Query Returns Too Many Rows
**Solution**: The generated query includes `LIMIT 100`. Adjust as needed.

---

## 🛠️ Command Line Usage

For automation and scripting:

```python
from src.etl_validator import ETLValidator

# Initialize
validator = ETLValidator('path/to/mapping.csv')

# Load mappings
validator.load_mappings()

# Generate queries
queries = validator.generate_validation_queries(
    source_table='source_tbl',
    target_table='target_tbl',
    source_schema='src_schema',
    target_schema='tgt_schema',
    query_type='both'  # or 'source_minus_target' or 'target_minus_source'
)

# Save to files
with open('source_minus_target.sql', 'w') as f:
    f.write(queries['source_minus_target'])

# Or use directly
print(queries['complete'])
```

---

## 📁 File Locations

After generation, files are saved to:
- **Web uploads**: `uploads/` directory
- **Generated queries** (via CLI): `output/` directory
- **Example mappings**: `examples/` directory

---

## 🔗 Additional Resources

- **Full Documentation**: See [README.md](README.md)
- **Quick Start**: See [QUICK_START.md](QUICK_START.md)
- **Project Summary**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Sample Mappings**: Check `examples/` directory
- **Demo Script**: Run `python demo.py`

---

## 🎯 Real-World Workflow

```
1. ETL Developer creates mapping document (CSV)
   ↓
2. Upload to ETL Validator web interface
   ↓
3. Configure source/target details
   ↓
4. Generate validation SQL queries
   ↓
5. Copy queries to your ETL tool/scheduler
   ↓
6. Execute after each ETL run
   ↓
7. Monitor for discrepancies
```

---

## ✅ Success Checklist

Before generating queries, ensure:
- [ ] CSV file has required columns (source_column, target_column)
- [ ] At least one column marked as join key (is_key=TRUE)
- [ ] Transformations use correct SQL syntax for your database
- [ ] Source and target table names are correct
- [ ] Schema names are specified (if required)

---

## 🎉 You're All Set!

You now have a complete understanding of how to use the ETL Mapping Validator. Start by exploring the example mappings or upload your own!

**Need help?** Open an issue on GitHub or check the documentation files.

---

Made with ❤️ for Data Engineers and ETL Developers
