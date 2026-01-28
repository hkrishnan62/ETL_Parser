# 🎮 Interactive SQL Playground

The ETL Parser now includes a powerful **Interactive SQL Playground** that lets you test SQL queries with live syntax highlighting, sample data, and shareable results!

## ✨ Features

### 1. **Live SQL Query Execution**
- Execute SELECT queries in a sandboxed SQLite environment
- Real-time results display with formatted tables
- Sample database with customers and orders data

### 2. **Syntax Highlighting**
- Professional SQL syntax highlighting using CodeMirror
- Dark theme optimized for readability
- Auto-complete support (Ctrl+Space)
- Quick execution with Ctrl+Enter

### 3. **Sample Queries Library**
Pre-loaded examples to get you started:
- ✅ Basic customer queries
- ✅ JOIN operations
- ✅ Aggregations with GROUP BY
- ✅ ETL transformation examples with CASE, CONCAT, UPPER/LOWER
- ✅ Data quality checks

### 4. **Database Schema Browser**
- Interactive schema viewer showing:
  - Table names
  - Column names and types
  - Easy reference while writing queries

### 5. **Share Query Results**
- 🔗 Generate unique shareable links
- Share queries and results with teammates
- Track view counts
- Permanent storage of shared queries

### 6. **Security**
- ✅ Sandboxed execution - queries run in isolated SQLite environment
- ✅ Read-only queries - only SELECT statements allowed
- ✅ No dangerous operations (DROP, DELETE, UPDATE blocked)
- ✅ Safe for public use

## 🚀 Quick Start

### Access the Playground

1. **From the main ETL Validator page:**
   - Click the "🎮 SQL Playground" button in the navigation bar

2. **Direct URL:**
   ```
   http://your-domain.com/playground/
   ```

### Using the Playground

1. **Write your SQL query** in the editor (or select a sample query)
2. **Click "Run Query"** or press Ctrl+Enter
3. **View results** in the right panel
4. **Share** your query using the share button

## 📊 Sample Database Schema

The playground includes two pre-populated tables:

### `customers` table
```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    created_date TEXT
);
```

**Sample Data:** 5 customers with complete information

### `orders` table
```sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    status TEXT
);
```

**Sample Data:** 7 orders with various statuses

## 💡 Example Queries

### Basic Query
```sql
SELECT * FROM customers LIMIT 5;
```

### Join Query
```sql
SELECT 
    c.first_name,
    c.last_name,
    o.order_date,
    o.total_amount,
    o.status
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC;
```

### ETL Transformation
```sql
SELECT 
    customer_id,
    UPPER(first_name) || ' ' || UPPER(last_name) as full_name,
    LOWER(email) as email_normalized,
    REPLACE(phone, '-', '') as phone_cleaned,
    SUBSTR(created_date, 1, 7) as month
FROM customers;
```

### Aggregation
```sql
SELECT 
    status,
    COUNT(*) as order_count,
    ROUND(AVG(total_amount), 2) as avg_amount,
    SUM(total_amount) as total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC;
```

## 🔗 Sharing Queries

### Create a Share Link

1. Write and execute your query
2. Click the "🔗 Share" button
3. Copy the generated URL
4. Share with anyone!

### Share Link Example
```
https://your-domain.com/playground/a1b2c3d4e5f6
```

### What's Shared?
- ✅ SQL query text
- ✅ Query results (if available)
- ✅ Execution metadata
- ✅ View count

## 🎨 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Execute query |
| `Ctrl+Space` | Show autocomplete |
| `Ctrl+/` | Toggle comment |
| `Tab` | Indent |
| `Shift+Tab` | Outdent |

## 🔧 API Endpoints

### Execute Query
```http
POST /playground/execute
Content-Type: application/json

{
  "query": "SELECT * FROM customers;",
  "sample_data": null
}
```

**Response:**
```json
{
  "success": true,
  "rows": [...],
  "columns": ["customer_id", "first_name", ...],
  "row_count": 5,
  "query": "SELECT * FROM customers;"
}
```

### Create Share Link
```http
POST /playground/share
Content-Type: application/json

{
  "query": "SELECT * FROM customers;",
  "results": {...}
}
```

**Response:**
```json
{
  "success": true,
  "share_id": "a1b2c3d4e5f6",
  "share_url": "https://your-domain.com/playground/a1b2c3d4e5f6"
}
```

### Get Sample Queries
```http
GET /playground/samples
```

### Get Database Schema
```http
GET /playground/schema
```

## 🛠️ Custom Sample Data

You can also provide custom sample data when using the API:

```python
from src.sql_playground import SQLPlayground

playground = SQLPlayground()

# Custom sample data
sample_data = {
    'my_table': [
        {'id': 1, 'name': 'Alice', 'amount': 100},
        {'id': 2, 'name': 'Bob', 'amount': 200}
    ]
}

result = playground.execute_query(
    "SELECT * FROM my_table WHERE amount > 150",
    sample_data=sample_data
)

print(result['rows'])
```

## 🎯 Use Cases

### 1. **Learning SQL**
- Practice SQL queries with instant feedback
- Try different query patterns
- Learn from sample queries

### 2. **Testing ETL Transformations**
- Test transformation logic before production
- Validate CASE statements
- Test string manipulation functions

### 3. **Sharing Query Examples**
- Share query solutions with teammates
- Create tutorial links
- Document SQL patterns

### 4. **Data Quality Checks**
- Test validation queries
- Check for data issues
- Verify business logic

### 5. **Interview Preparation**
- Practice SQL interview questions
- Test complex queries
- Build a portfolio of queries

## 🚀 Traffic Growth Benefits

### SEO Value
- **Keywords:** SQL playground, SQL online editor, SQL test, interactive SQL
- **Rich content:** Sample queries, tutorials, documentation
- **Shareability:** Viral potential through shared queries

### User Engagement
- ⏱️ **Time on site:** Interactive features increase engagement
- 🔄 **Return visits:** Users come back to test queries
- 📤 **Social sharing:** Share query results on social media
- 💬 **Community:** Users share interesting queries

### Conversion Path
1. User searches "SQL playground online"
2. Finds your tool
3. Tests SQL queries
4. Discovers ETL Validator
5. Uses for production work
6. Shares with team

## 🔮 Future Enhancements

Potential additions:
- [ ] Support for PostgreSQL, MySQL, SQL Server dialects
- [ ] Query history per user
- [ ] Collaborative editing
- [ ] Query performance metrics
- [ ] Export results to CSV/JSON
- [ ] Save favorite queries
- [ ] Query templates library
- [ ] Syntax error highlighting
- [ ] Query optimization suggestions

## 📈 Analytics & Metrics

Track these metrics for growth:
- Query execution count
- Share link creation rate
- Share link views
- Popular sample queries
- Average session duration
- Query complexity distribution

## 🎓 Learn More

- [Main Documentation](../README.md)
- [ETL Validator Guide](../QUICK_START.md)
- [AI Features](../AI_FEATURES.md)
- [Deployment Guide](../DEPLOYMENT_GUIDE.md)

---

**Built with ❤️ for the data community**

Start testing SQL queries now: [Launch Playground](/playground/)
