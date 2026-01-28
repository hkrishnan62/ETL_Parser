# 🧪 ETL Testing with SQL Playground

## Enhanced Features for ETL Testers

The SQL Playground now includes **specialized features for ETL testing**, making it the perfect tool for data engineers and ETL developers.

## 🎯 New ETL-Focused Features

### 1. **Organized Test Library**
Queries are now categorized by purpose:
- **ETL Testing** - Transformation validation, row count checks
- **Data Quality** - NULL detection, duplicate finding, integrity checks
- **Data Profiling** - Statistics, completeness analysis

### 2. **10 Pre-Built ETL Test Queries**
1. ✅ **ETL Row Count Validation** - Compare source vs target counts
2. ✅ **Data Transformation Test** - Side-by-side before/after comparison
3. ✅ **NULL Value Analysis** - Find missing data across columns
4. ✅ **Duplicate Detection** - Identify duplicate records
5. ✅ **Data Profiling Statistics** - Min/max/avg analysis
6. ✅ **Referential Integrity Check** - Find orphaned records
7. ✅ **Date Range Validation** - Check date boundaries
8. ✅ **String Length Validation** - Verify field lengths
9. ✅ **CASE Statement Testing** - Test complex transformations
10. ✅ **Aggregation Validation** - Verify totals match

### 3. **One-Click Data Profiling**
- Click "📊 Profile Table" button
- Enter table name (customers or orders)
- Get instant report with:
  - Row count
  - Distinct values per column
  - NULL counts and percentages
  - Data completeness metrics

### 4. **ETL Validation API**
Compare source and target data programmatically:
```python
from src.sql_playground import SQLPlayground

playground = SQLPlayground()

# Run ETL validation test
result = playground.run_etl_validation_test(
    source_query="SELECT * FROM source_table",
    target_query="SELECT * FROM target_table"
)

print(f"Source count: {result['source_count']}")
print(f"Target count: {result['target_count']}")
print(f"Match: {result['count_match']}")
```

### 5. **ETL Test Templates**
Pre-configured test cases for common scenarios:
- Row count matching
- NULL handling verification
- String transformation validation
- Date extraction testing
- Aggregation validation

## 📋 Common ETL Testing Scenarios

### Scenario 1: Validate Row Counts Match
```sql
-- Ensure no rows lost during ETL
SELECT 'Source' as table_name, COUNT(*) as row_count FROM customers
UNION ALL
SELECT 'Target' as table_name, COUNT(*) as row_count FROM customers;
```
**Expected**: Both counts should be identical

### Scenario 2: Test Data Transformations
```sql
-- Verify transformations are applied correctly
SELECT 
    customer_id,
    first_name || ' ' || last_name as original,
    UPPER(first_name) || ' ' || UPPER(last_name) as transformed,
    CASE 
        WHEN UPPER(first_name) || ' ' || UPPER(last_name) = 
             UPPER(first_name || ' ' || last_name) THEN 'PASS'
        ELSE 'FAIL'
    END as test_result
FROM customers;
```
**Expected**: All rows should show 'PASS'

### Scenario 3: Check for NULL Values
```sql
-- Identify incomplete records
SELECT 
    customer_id,
    CASE WHEN email IS NULL THEN 'Missing Email' ELSE 'OK' END as email_check,
    CASE WHEN phone IS NULL THEN 'Missing Phone' ELSE 'OK' END as phone_check
FROM customers
WHERE email IS NULL OR phone IS NULL;
```
**Expected**: Zero rows if data is complete

### Scenario 4: Detect Duplicates
```sql
-- Find duplicate customer emails
SELECT 
    email,
    COUNT(*) as occurrence_count,
    GROUP_CONCAT(customer_id) as customer_ids
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```
**Expected**: Zero rows if no duplicates

### Scenario 5: Validate Referential Integrity
```sql
-- Find orphaned orders (orders without customers)
SELECT 
    o.order_id,
    o.customer_id,
    'Orphaned - No Customer' as issue
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```
**Expected**: Zero rows if all foreign keys valid

### Scenario 6: Check Aggregations
```sql
-- Verify detail-level sums match aggregated totals
WITH detail_total AS (
    SELECT SUM(total_amount) as amount FROM orders
),
agg_total AS (
    SELECT SUM(status_total) as amount
    FROM (
        SELECT status, SUM(total_amount) as status_total
        FROM orders
        GROUP BY status
    )
)
SELECT 
    d.amount as detail_sum,
    a.amount as aggregated_sum,
    CASE 
        WHEN d.amount = a.amount THEN 'PASS'
        ELSE 'FAIL'
    END as validation_result
FROM detail_total d, agg_total a;
```
**Expected**: Validation result = 'PASS'

## 🔬 Data Profiling Example

Profile the customers table to understand data quality:

```python
from src.sql_playground import SQLPlayground

playground = SQLPlayground()
profile = playground.get_data_profile('customers')

print(f"Table: {profile['table']}")
print(f"Total Rows: {profile['row_count']}")
print("\nColumn Analysis:")

for column, stats in profile['columns'].items():
    print(f"\n  {column}:")
    print(f"    Distinct Values: {stats['distinct_values']}")
    print(f"    NULL Count: {stats['null_count']}")
    print(f"    Completeness: {stats['completeness']}%")
```

**Output:**
```
Table: customers
Total Rows: 5

Column Analysis:
  customer_id:
    Distinct Values: 5
    NULL Count: 0
    Completeness: 100.0%
    
  email:
    Distinct Values: 5
    NULL Count: 0
    Completeness: 100.0%
```

## 🎨 User Interface Enhancements

### Tabbed Sidebar
- **ETL Tests Tab**: Transformation and validation queries
- **Data Quality Tab**: NULL checks, duplicates, integrity
- **Profiling Tab**: Statistical analysis queries
- **Schema Tab**: Database structure reference

### Quick Actions
- **Run Query** (Ctrl+Enter): Execute current SQL
- **Profile Table**: Generate data profile report
- **Share**: Create shareable link
- **Clear**: Reset editor

## 📊 ETL Test Checklist

Use this checklist for comprehensive ETL testing:

- [ ] **Row Count Validation**
  ```sql
  SELECT COUNT(*) FROM source vs SELECT COUNT(*) FROM target
  ```

- [ ] **Data Type Validation**
  ```sql
  Check data types match target schema
  ```

- [ ] **NULL Value Check**
  ```sql
  Identify columns with missing values
  ```

- [ ] **Duplicate Detection**
  ```sql
  Find duplicate primary keys or unique columns
  ```

- [ ] **Referential Integrity**
  ```sql
  Verify all foreign keys have matching records
  ```

- [ ] **Transformation Logic**
  ```sql
  Test CASE statements, CONCAT, UPPER/LOWER, etc.
  ```

- [ ] **Date Range Validation**
  ```sql
  Ensure dates fall within expected boundaries
  ```

- [ ] **String Length Check**
  ```sql
  Verify VARCHAR fields don't exceed limits
  ```

- [ ] **Aggregation Validation**
  ```sql
  Confirm SUMs, AVGs match between detail and summary
  ```

- [ ] **Business Rule Validation**
  ```sql
  Test domain-specific rules (e.g., age > 0, amount >= 0)
  ```

## 🚀 Best Practices for ETL Testing

### 1. **Test Early and Often**
- Run tests on sample data first
- Test transformations in isolation
- Validate incrementally

### 2. **Document Test Cases**
- Use SQL comments to explain tests
- Share queries with team using share button
- Maintain library of standard tests

### 3. **Automate Where Possible**
- Use Python API for repetitive tests
- Integrate with CI/CD pipelines
- Schedule regular data quality checks

### 4. **Compare Source vs Target**
- Always validate row counts match
- Check aggregated totals align
- Verify no data loss during transformation

### 5. **Profile Your Data**
- Run profiling before and after ETL
- Track data quality metrics over time
- Identify anomalies early

## 🔗 API Endpoints for ETL Testing

### Execute Query
```bash
curl -X POST http://localhost:5000/playground/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT COUNT(*) FROM customers"}'
```

### Run ETL Validation Test
```bash
curl -X POST http://localhost:5000/playground/etl-test \
  -H "Content-Type: application/json" \
  -d '{
    "source_query": "SELECT * FROM source",
    "target_query": "SELECT * FROM target"
  }'
```

### Get Data Profile
```bash
curl http://localhost:5000/playground/profile/customers
```

### Get Test Templates
```bash
curl http://localhost:5000/playground/test-templates
```

## 💡 Tips for ETL Testers

1. **Use the Profile Button**: Quick data quality overview
2. **Organize by Tabs**: Keep tests categorized
3. **Share Results**: Use share button for documentation
4. **Test Transformations Side-by-Side**: Compare before/after in same query
5. **Validate Early**: Catch issues before production

## 🎯 Real-World ETL Testing Example

Complete ETL validation workflow:

```sql
-- Step 1: Check row counts
SELECT 'Source Count' as check, COUNT(*) as value FROM customers
UNION ALL
SELECT 'Target Count', COUNT(*) FROM customers;

-- Step 2: Validate transformations
SELECT 
    customer_id,
    first_name || ' ' || last_name as source_name,
    UPPER(first_name) || ' ' || UPPER(last_name) as target_name,
    CASE 
        WHEN UPPER(first_name || ' ' || last_name) = 
             UPPER(first_name) || ' ' || UPPER(last_name)
        THEN '✓ PASS' 
        ELSE '✗ FAIL' 
    END as validation
FROM customers;

-- Step 3: Check data quality
SELECT 
    COUNT(*) as total_records,
    COUNT(CASE WHEN email IS NULL THEN 1 END) as null_emails,
    COUNT(CASE WHEN phone IS NULL THEN 1 END) as null_phones,
    COUNT(DISTINCT email) as unique_emails
FROM customers;

-- Step 4: Verify aggregations
SELECT 
    status,
    COUNT(*) as order_count,
    SUM(total_amount) as revenue
FROM orders
GROUP BY status
ORDER BY revenue DESC;
```

## 📚 Learn More

- [SQL Playground Documentation](SQL_PLAYGROUND.md)
- [Quick Reference](PLAYGROUND_QUICK_REFERENCE.md)
- [Main README](README.md)

---

**Happy ETL Testing! 🚀**

Access the playground: http://localhost:5000/playground/
