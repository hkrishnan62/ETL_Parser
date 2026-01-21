# ETL Mapping File Format Guide

## 📋 Required Format

Your ETL mapping file must be a CSV or Excel file with exactly **3 required columns**:

### Required Columns

| Column Name | Description | Example |
|------------|-------------|---------|
| `source_column` | The column name from your source table | `customer_id` |
| `target_column` | The column name in your target table | `cust_id` |
| `transformation` | The SQL transformation logic or direct mapping | `source.customer_id` or `LOWER(source.email)` |

## ✅ Valid Mapping File Example

```csv
source_column,target_column,transformation
customer_id,cust_id,source.customer_id
first_name,fname,source.first_name
last_name,lname,source.last_name
email,email_addr,LOWER(source.email)
created_date,created_at,CAST(source.created_date AS DATE)
status,order_status,CASE WHEN source.status = 'ACTIVE' THEN 'A' ELSE 'I' END
```

## ❌ Common Validation Errors

### 1. Missing Required Columns
**Error:** `Missing required columns: transformation`

**Cause:** Your file is missing one or more required columns.

**Solution:** Ensure your file has all three columns:
- `source_column`
- `target_column`
- `transformation`

### 2. Empty Cells in Required Fields
**Error:** `Found 3 row(s) with missing required data`

**Cause:** Some rows have empty cells in the required columns.

**Solution:** Fill in all required columns for every row. Delete rows that don't have complete data.

### 3. Empty File
**Error:** `File is empty. Please provide a mapping file with data.`

**Cause:** Your uploaded file contains no data.

**Solution:** Add at least one row of mapping data to your file.

## 📁 Supported File Formats

- **CSV** (.csv)
- **Excel** (.xlsx, .xls)

## 💡 Tips

1. **Column Names Are Case-Insensitive**: You can use `Source_Column`, `SOURCE_COLUMN`, or `source_column` - they all work!

2. **Whitespace Is Trimmed**: Leading and trailing spaces in column names are automatically cleaned.

3. **Extra Columns Are Allowed**: You can add additional columns like `data_type` or `notes` - they won't interfere with processing.

4. **Avoid Empty Rows**: Don't leave blank rows in your mapping file.

5. **Use Direct References**: For simple direct mappings, use `source.column_name` or `target_table.column_name`.

## 🔍 Example Transformations

### Direct Mapping
```
source_column,target_column,transformation
id,id,source.id
name,name,source.name
```

### Type Conversion
```
source_column,target_column,transformation
birth_date,dob,CAST(source.birth_date AS DATE)
salary,salary_amt,CAST(source.salary AS DECIMAL(10,2))
```

### String Manipulation
```
source_column,target_column,transformation
email,email_addr,LOWER(source.email)
phone,phone_number,CONCAT('1-', source.phone)
```

### Conditional Logic
```
source_column,target_column,transformation
status,is_active,CASE WHEN source.status = 'ACTIVE' THEN true ELSE false END
```

## 🚀 Getting Started

1. Prepare your mapping file with the required 3 columns
2. Ensure all rows have complete data (no empty cells)
3. Upload the file to ETL Parser
4. Select your target table and database type
5. Generate SQL queries!

---

**Need Help?** Click the "View example →" link in the sidebar to see the format guide.
