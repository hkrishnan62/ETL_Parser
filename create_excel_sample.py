"""
Create a sample Excel file for testing
"""
import pandas as pd

# Create sample mapping data
data = {
    'source_column': ['customer_id', 'first_name', 'last_name', 'email', 'phone', 'registration_date', 'status_code', 'total_purchases'],
    'target_column': ['cust_key', 'first_name', 'last_name', 'email_address', 'phone_number', 'reg_timestamp', 'status', 'purchase_total'],
    'transformation': [
        'customers.customer_id',
        'customers.first_name',
        'customers.last_name',
        'LOWER(TRIM(customers.email))',
        "REGEXP_REPLACE(customers.phone, '[^0-9]', '')",
        "TO_TIMESTAMP(customers.registration_date, 'YYYY-MM-DD HH24:MI:SS')",
        "CASE WHEN customers.status_code = 'A' THEN 'ACTIVE' WHEN customers.status_code = 'I' THEN 'INACTIVE' ELSE 'UNKNOWN' END",
        'COALESCE(customers.total_purchases, 0)'
    ],
    'is_key': ['TRUE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE']
}

df = pd.DataFrame(data)

# Save to Excel
excel_file = 'examples/sample_mapping.xlsx'
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"✓ Created Excel file: {excel_file}")
print(f"  Rows: {len(df)}")
print(f"  Columns: {list(df.columns)}")
print("\nYou can now upload this file to test Excel support!")
