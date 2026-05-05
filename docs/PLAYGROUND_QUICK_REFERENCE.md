# 🎮 SQL Playground - Quick Reference Card

## 🚀 Access
- **Main Page**: http://localhost:5000/playground/
- **From ETL Validator**: Click "🎮 SQL Playground" in navbar

## ⌨️ Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Execute query |
| `Ctrl+Space` | Auto-complete |
| `Ctrl+/` | Toggle comment |
| `Tab` | Indent selection |

## 📊 Sample Tables

### customers (5 rows)
```
customer_id | first_name | last_name | email | phone | created_date
```

### orders (7 rows)
```
order_id | customer_id | order_date | total_amount | status
```

## 💡 Quick Queries

### See all customers
```sql
SELECT * FROM customers;
```

### Join with orders
```sql
SELECT c.first_name, c.last_name, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

### Aggregation
```sql
SELECT status, COUNT(*) as count, SUM(total_amount) as revenue
FROM orders
GROUP BY status;
```

### Transformation
```sql
SELECT 
    UPPER(first_name) || ' ' || UPPER(last_name) as full_name,
    LOWER(email) as email_clean
FROM customers;
```

## 🔗 API Endpoints

### Execute Query
```bash
curl -X POST http://localhost:5000/playground/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM customers"}'
```

### Create Share Link
```bash
curl -X POST http://localhost:5000/playground/share \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM customers", "results": {...}}'
```

### Get Samples
```bash
curl http://localhost:5000/playground/samples
```

### Get Schema
```bash
curl http://localhost:5000/playground/schema
```

## 🔒 Security
- ✅ Only SELECT queries allowed
- ❌ DROP, DELETE, UPDATE, INSERT blocked
- 🔐 Sandboxed SQLite environment
- 💾 In-memory database (no persistence)

## 📤 Sharing
1. Write your query
2. Run it to test
3. Click "🔗 Share" button
4. Copy the generated URL
5. Share with anyone!

**Share URL format**: `http://localhost:5000/playground/abc123def456`

## 🎯 Use Cases
- ✅ Test SQL transformations
- ✅ Learn SQL syntax
- ✅ Validate ETL logic
- ✅ Share query examples
- ✅ Interview preparation
- ✅ Teaching SQL

## 🐛 Troubleshooting

### Query won't run
- Check for syntax errors
- Ensure it's a SELECT query
- Verify table names (customers, orders)

### Share link not working
- Server must be running
- Check share_id is correct
- Verify shares.json exists in playground_storage/

### No results shown
- Query may return 0 rows
- Check WHERE conditions
- Verify table has data

## 📚 Learn More
- [Full Documentation](SQL_PLAYGROUND.md)
- [API Reference](SQL_PLAYGROUND.md#-api-endpoints)
- [Security Details](SQL_PLAYGROUND.md#-security)

---
**Happy querying! 🎉**
