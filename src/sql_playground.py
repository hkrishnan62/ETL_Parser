"""
SQL Playground - Execute and share SQL queries with sample data
"""
import sqlite3
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import re


class SQLPlayground:
    """Handles SQL query execution in a sandboxed environment"""
    
    def __init__(self, storage_dir: str = 'playground_storage'):
        """Initialize SQL playground with storage directory"""
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.shares_file = os.path.join(storage_dir, 'shares.json')
        
        # Initialize shares storage
        if not os.path.exists(self.shares_file):
            with open(self.shares_file, 'w') as f:
                json.dump({}, f)
    
    def create_sample_database(self, sample_data: Optional[Dict[str, List[Dict]]] = None) -> sqlite3.Connection:
        """
        Create an in-memory SQLite database with sample data
        
        Args:
            sample_data: Dictionary mapping table names to list of row dictionaries
        
        Returns:
            SQLite connection with sample data
        """
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        
        if sample_data:
            for table_name, rows in sample_data.items():
                if not rows:
                    continue
                
                # Sanitize table name
                table_name = self._sanitize_identifier(table_name)
                
                # Create table from first row
                first_row = rows[0]
                columns = ', '.join([f'{self._sanitize_identifier(col)} TEXT' 
                                   for col in first_row.keys()])
                
                conn.execute(f'CREATE TABLE {table_name} ({columns})')
                
                # Insert data
                for row in rows:
                    placeholders = ', '.join(['?' for _ in row])
                    cols = ', '.join([self._sanitize_identifier(col) for col in row.keys()])
                    conn.execute(
                        f'INSERT INTO {table_name} ({cols}) VALUES ({placeholders})',
                        tuple(row.values())
                    )
        else:
            # Create default sample tables
            self._create_default_sample_data(conn)
        
        conn.commit()
        return conn
    
    def _create_default_sample_data(self, conn: sqlite3.Connection):
        """Create default sample tables for demonstration"""
        # Customer table
import random
        from datetime import datetime, timedelta
        
        # 1. Customers table
        conn.execute('''
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone TEXT,
                date_of_birth TEXT,
                ssn TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                customer_since TEXT,
                customer_type TEXT,
                risk_score INTEGER
            )
        ''')
        
        first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth', 
                      'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Christopher', 'Karen']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
        states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']
        customer_types = ['Individual', 'Business', 'Premium', 'Corporate']
        
        customers = []
        for i in range(1, 1001):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            city_idx = random.randint(0, len(cities)-1)
            dob = (datetime(1950, 1, 1) + timedelta(days=random.randint(0, 25000))).strftime('%Y-%m-%d')
            since = (datetime(2010, 1, 1) + timedelta(days=random.randint(0, 5000))).strftime('%Y-%m-%d')
            customers.append((
                i, fname, lname, f'{fname.lower()}.{lname.lower()}{i}@email.com',
                f'555-{random.randint(1000,9999)}', dob, f'***-**-{random.randint(1000,9999)}',
                f'{random.randint(100,9999)} Main St', cities[city_idx], states[city_idx],
                f'{random.randint(10000,99999)}', since, random.choice(customer_types), random.randint(300,850)
            ))
        
        conn.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', customers)
        
        # 2. Accounts table
        conn.execute('''
            CREATE TABLE accounts (
                account_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                account_number TEXT,
                account_type TEXT,
                balance REAL,
                currency TEXT,
                status TEXT,
                open_date TEXT,
                interest_rate REAL,
                branch_id INTEGER
            )
        ''')
        
        account_types = ['Checking', 'Savings', 'Money Market', 'CD', 'Investment']
        statuses = ['Active', 'Dormant', 'Closed', 'Frozen']
        accounts = []
        for i in range(1, 1001):
            accounts.append((
                i, random.randint(1, 1000), f'ACC{str(i).zfill(10)}',
                random.choice(account_types), round(random.uniform(100, 500000), 2),
                'USD', random.choice(statuses),
                (datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000))).strftime('%Y-%m-%d'),
                round(random.uniform(0.5, 5.5), 2), random.randint(1, 50)
            ))
        
        conn.executemany('INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?,?,?)', accounts)
        
        # 3. Transactions table
        conn.execute('''
            CREATE TABLE transactions (
                transaction_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                transaction_date TEXT,
                transaction_type TEXT,
                amount REAL,
                balance_after REAL,
                description TEXT,
                merchant_name TEXT,
                category TEXT,
                status TEXT
            )
        ''')
        
        trans_types = ['Debit', 'Credit', 'Transfer', 'ATM Withdrawal', 'Check', 'Wire']
        categories = ['Groceries', 'Gas', 'Restaurants', 'Shopping', 'Utilities', 'Healthcare', 'Entertainment', 'Travel', 'Other']
        merchants = ['Walmart', 'Target', 'Amazon', 'Shell', 'Starbucks', 'McDonalds', 'CVS', 'Home Depot', 'Best Buy', 'Costco']
        
        transactions = []
        for i in range(1, 1001):
            trans_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S')
            amount = round(random.uniform(5, 5000), 2)
            transactions.append((
                i, random.randint(1, 1000), trans_date, random.choice(trans_types),
                amount, round(random.uniform(100, 50000), 2),
                f'Transaction {i}', random.choice(merchants), random.choice(categories), 'Completed'
            ))
        
        conn.executemany('INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?)', transactions)
        
        # 4. Loans table
        conn.execute('''
            CREATE TABLE loans (
                loan_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                loan_type TEXT,
                principal_amount REAL,
                interest_rate REAL,
                term_months INTEGER,
                monthly_payment REAL,
                outstanding_balance REAL,
                origination_date TEXT,
                maturity_date TEXT,
                status TEXT
            )
        ''')
        
        loan_types = ['Mortgage', 'Auto', 'Personal', 'Student', 'Business', 'Home Equity']
        loan_statuses = ['Active', 'Paid Off', 'Defaulted', 'In Collections']
        
        loans = []
        for i in range(1, 1001):
            principal = round(random.uniform(5000, 500000), 2)
            rate = round(random.uniform(3.0, 18.0), 2)
            term = random.choice([12, 24, 36, 60, 84, 120, 180, 240, 360])
            orig_date = (datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000))).strftime('%Y-%m-%d')
            mat_date = (datetime.strptime(orig_date, '%Y-%m-%d') + timedelta(days=term*30)).strftime('%Y-%m-%d')
            monthly_pmt = round(principal * (rate/1200) / (1 - (1 + rate/1200)**(-term)), 2)
            
            loans.append((
                i, random.randint(1, 1000), random.choice(loan_types), principal, rate, term,
                monthly_pmt, round(principal * random.uniform(0, 0.95), 2), orig_date, mat_date,
                random.choice(loan_statuses)
            ))
        
        conn.executemany('INSERT INTO loans VALUES (?,?,?,?,?,?,?,?,?,?,?)', loans)
        
        # 5. Credit Cards table
        conn.execute('''
            CREATE TABLE credit_cards (
                card_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                card_number TEXT,
                card_type TEXT,
                credit_limit REAL,
                current_balance REAL,
                available_credit REAL,
                apr REAL,
                issue_date TEXT,
                expiry_date TEXT,
                status TEXT
            )
        ''')
        
        card_types = ['Visa', 'Mastercard', 'American Express', 'Discover']
        
        cards = []
        for i in range(1, 1001):
            limit = round(random.uniform(1000, 50000), 2)
            balance = round(random.uniform(0, limit), 2)
            issue = (datetime(2018, 1, 1) + timedelta(days=random.randint(0, 2000))).strftime('%Y-%m-%d')
            expiry = (datetime.strptime(issue, '%Y-%m-%d') + timedelta(days=1460)).strftime('%Y-%m-%d')
            
            cards.append((
                i, random.randint(1, 1000), f'****-****-****-{random.randint(1000,9999)}',
                random.choice(card_types), limit, balance, limit - balance,
                round(random.uniform(12.99, 29.99), 2), issue, expiry,
                random.choice(['Active', 'Closed', 'Suspended'])
            ))
        
        conn.executemany('INSERT INTO credit_cards VALUES (?,?,?,?,?,?,?,?,?,?,?)', cards)
        
        # 6. Branches table
        conn.execute('''
            CREATE TABLE branches (
                branch_id INTEGER PRIMARY KEY,
                branch_name TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                phone TEXT,
                manager_name TEXT,
                open_date TEXT,
                branch_type TEXT
            )
        ''')
        
        branches = []
        for i in range(1, 1001):
            city_idx = random.randint(0, len(cities)-1)
            branches.append((
                i, f'Branch {i}', f'{random.randint(100,9999)} Financial Ave',
                cities[city_idx], states[city_idx], f'{random.randint(10000,99999)}',
                f'555-{random.randint(1000,9999)}', f'{random.choice(first_names)} {random.choice(last_names)}',
                (datetime(2000, 1, 1) + timedelta(days=random.randint(0, 8000))).strftime('%Y-%m-%d'),
                random.choice(['Full Service', 'ATM Only', 'Commercial', 'Retail'])
            ))
        
        conn.executemany('INSERT INTO branches VALUES (?,?,?,?,?,?,?,?,?,?)', branches)
        
        # 7. Employees table
        conn.execute('''
            CREATE TABLE employees (
                employee_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone TEXT,
                position TEXT,
                department TEXT,
                salary REAL,
                hire_date TEXT,
                branch_id INTEGER,
                manager_id INTEGER
            )
        ''')
        
        positions = ['Teller', 'Personal Banker', 'Loan Officer', 'Branch Manager', 'Financial Advisor', 'Operations Manager']
        departments = ['Retail Banking', 'Commercial Banking', 'Wealth Management', 'Operations', 'Compliance', 'IT']
        
        employees = []
        for i in range(1, 1001):
            employees.append((
                i, random.choice(first_names), random.choice(last_names),
                f'employee{i}@bank.com', f'555-{random.randint(1000,9999)}',
                random.choice(positions), random.choice(departments),
                round(random.uniform(35000, 150000), 2),
                (datetime(2010, 1, 1) + timedelta(days=random.randint(0, 5000))).strftime('%Y-%m-%d'),
                random.randint(1, 50), random.randint(1, 100) if i > 100 else None
            ))
        
        conn.executemany('INSERT INTO employees VALUES (?,?,?,?,?,?,?,?,?,?,?)', employees)
        
        # 8. Investments table
        conn.execute('''
            CREATE TABLE investments (
                investment_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                account_id INTEGER,
                investment_type TEXT,
                symbol TEXT,
                quantity REAL,
                purchase_price REAL,
                current_price REAL,
                purchase_date TEXT,
                portfolio_value REAL
            )
        ''')
        
        inv_types = ['Stock', 'Bond', 'Mutual Fund', 'ETF', 'Options', 'Commodity']
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'JPM', 'BAC', 'WFC', 'GS', 'MS', 'SPY', 'QQQ', 'VTI']
        
        investments = []
        for i in range(1, 1001):
            qty = round(random.uniform(1, 1000), 2)
            purchase = round(random.uniform(10, 500), 2)
            current = purchase * random.uniform(0.5, 2.0)
            
            investments.append((
                i, random.randint(1, 1000), random.randint(1, 1000), random.choice(inv_types),
                random.choice(symbols), qty, purchase, round(current, 2),
                (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))).strftime('%Y-%m-%d'),
                round(qty * current, 2)
            ))
        
        conn.executemany('INSERT INTO investments VALUES (?,?,?,?,?,?,?,?,?,?)', investments)
        
        # 9. Insurance Policies table
        conn.execute('''
            CREATE TABLE insurance_policies (
                policy_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                policy_type TEXT,
                policy_number TEXT,
                premium_amount REAL,
                coverage_amount REAL,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                beneficiary TEXT
            )
        ''')
        
        policy_types = ['Life', 'Health', 'Auto', 'Home', 'Disability', 'Umbrella']
        
        policies = []
        for i in range(1, 1001):
            start = (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))).strftime('%Y-%m-%d')
            end = (datetime.strptime(start, '%Y-%m-%d') + timedelta(days=365)).strftime('%Y-%m-%d')
            
            policies.append((
                i, random.randint(1, 1000), random.choice(policy_types), f'POL{str(i).zfill(8)}',
                round(random.uniform(50, 500), 2), round(random.uniform(10000, 1000000), 2),
                start, end, random.choice(['Active', 'Expired', 'Cancelled']),
                f'{random.choice(first_names)} {random.choice(last_names)}'
            ))
        
        conn.executemany('INSERT INTO insurance_policies VALUES (?,?,?,?,?,?,?,?,?,?)', policies)
        
        # 10. Fraud Alerts table
        conn.execute('''
            CREATE TABLE fraud_alerts (
                alert_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                transaction_id INTEGER,
                alert_date TEXT,
                alert_type TEXT,
                risk_level TEXT,
                description TEXT,
                status TEXT,
                assigned_to INTEGER,
                resolution_date TEXT
            )
        ''')
        
        alert_types = ['Unusual Transaction', 'Multiple Logins', 'Card Skimming', 'Identity Theft', 'Phishing', 'Account Takeover']
        risk_levels = ['Low', 'Medium', 'High', 'Critical']
        
        alerts = []
        for i in range(1, 1001):
            alert_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S')
            resolution = None if random.random() < 0.3 else (datetime.strptime(alert_date, '%Y-%m-%d %H:%M:%S') + timedelta(hours=random.randint(1, 72))).strftime('%Y-%m-%d %H:%M:%S')
            
            alerts.append((
                i, random.randint(1, 1000), random.randint(1, 1000), alert_date,
                random.choice(alert_types), random.choice(risk_levels),
                f'Potential fraud detected on transaction', 
                random.choice(['Open', 'Investigating', 'Resolved', 'False Positive']),
                random.randint(1, 100), resolution
            ))
        
        conn.executemany('INSERT INTO fraud_alerts VALUES (?,?,?,?,?,?,?,?,?,?)', alerts)
        
        # 11. ATM Transactions table
        conn.execute('''
            CREATE TABLE atm_transactions (
                atm_transaction_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                card_id INTEGER,
                atm_id TEXT,
                transaction_date TEXT,
                transaction_type TEXT,
                amount REAL,
                fee REAL,
                location TEXT,
                status TEXT
            )
        ''')
        
        atm_types = ['Withdrawal', 'Deposit', 'Balance Inquiry', 'Transfer']
        
        atm_trans = []
        for i in range(1, 1001):
            atm_trans.append((
                i, random.randint(1, 1000), random.randint(1, 1000), f'ATM{random.randint(1000,9999)}',
                (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'),
                random.choice(atm_types), round(random.uniform(20, 500), 2),
                random.choice([0, 2.5, 3.0]), f'{random.choice(cities)}, {random.choice(states)}',
                'Completed'
            ))
        
        conn.executemany('INSERT INTO atm_transactions VALUES (?,?,?,?,?,?,?,?,?,?)', atm_trans)
        
        # 12. Wire Transfers table
        conn.execute('''
            CREATE TABLE wire_transfers (
                transfer_id INTEGER PRIMARY KEY,
                from_account_id INTEGER,
                to_account_id INTEGER,
                amount REAL,
                currency TEXT,
                transfer_date TEXT,
                purpose TEXT,
                status TEXT,
                fee REAL,
                reference_number TEXT
            )
        ''')
        
        purposes = ['Payment', 'Investment', 'Personal Transfer', 'Business Transaction', 'Loan Payment', 'Property Purchase']
        
        wires = []
        for i in range(1, 1001):
            wires.append((
                i, random.randint(1, 1000), random.randint(1, 1000),
                round(random.uniform(1000, 100000), 2), 'USD',
                (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
                random.choice(purposes), random.choice(['Completed', 'Pending', 'Failed']),
                round(random.uniform(15, 50), 2), f'WIRE{str(i).zfill(10)}'
            ))
        
        conn.executemany('INSERT INTO wire_transfers VALUES (?,?,?,?,?,?,?,?,?,?)', wires)
        
        # 13. Merchant Transactions table
        conn.execute('''
            CREATE TABLE merchant_transactions (
                merchant_trans_id INTEGER PRIMARY KEY,
                card_id INTEGER,
                merchant_id TEXT,
                merchant_name TEXT,
                merchant_category TEXT,
                transaction_date TEXT,
                amount REAL,
                authorization_code TEXT,
                status TEXT,
                points_earned INTEGER
            )
        ''')
        
        merchant_cats = ['Retail', 'Dining', 'Travel', 'Gas', 'Grocery', 'Online', 'Entertainment', 'Healthcare', 'Utilities']
        
        merch_trans = []
        for i in range(1, 1001):
            amount = round(random.uniform(5, 2000), 2)
            merch_trans.append((
                i, random.randint(1, 1000), f'MER{random.randint(10000,99999)}',
                random.choice(merchants), random.choice(merchant_cats),
                (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'),
                amount, f'AUTH{random.randint(100000,999999)}',
                random.choice(['Approved', 'Declined', 'Pending']),
                int(amount * random.uniform(1, 3))
            ))
        
        conn.executemany('INSERT INTO merchant_transactions VALUES (?,?,?,?,?,?,?,?,?,?)', merch_trans)
        
        # 14. Credit Reports table
        conn.execute('''
            CREATE TABLE credit_reports (
                report_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                report_date TEXT,
                credit_score INTEGER,
                credit_bureau TEXT,
                total_accounts INTEGER,
                total_debt REAL,
                payment_history TEXT,
                credit_utilization REAL,
                derogatory_marks INTEGER
            )
        ''')
        
        bureaus = ['Experian', 'Equifax', 'TransUnion']
        payment_hist = ['Excellent', 'Good', 'Fair', 'Poor']
        
        reports = []
        for i in range(1, 1001):
            score = random.randint(300, 850)
            reports.append((
                i, random.randint(1, 1000),
                (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
                score, random.choice(bureaus), random.randint(1, 30),
                round(random.uniform(1000, 200000), 2),
                payment_hist[min(3, (850-score)//150)],
                round(random.uniform(0, 100), 1),
                random.randint(0, 5)
            ))
        
        conn.executemany('INSERT INTO credit_reports VALUES (?,?,?,?,?,?,?,?,?,?)', reports)
        
        # 15. Compliance Audit Logs table
        conn.execute('''
            CREATE TABLE compliance_audit_logs (
                audit_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                audit_date TEXT,
                audit_type TEXT,
                regulation TEXT,
                finding TEXT,
                severity TEXT,
                auditor_id INTEGER,
                status TEXT,
                resolution_date TEXT
            )
        ''')
        
        audit_types = ['KYC Review', 'AML Check', 'Transaction Review', 'Account Verification', 'Risk Assessment']
        regulations = ['BSA', 'OFAC', 'GDPR', 'SOX', 'FCRA', 'Reg E', 'Reg Z']
        findings = ['Compliant', 'Minor Issue', 'Major Issue', 'Critical Issue', 'Under Review']
        severities = ['Low', 'Medium', 'High', 'Critical']
        
        audits = []
        for i in range(1, 1001):
            audit_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
            resolution = None if random.random() < 0.2 else (datetime.strptime(audit_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            
            audits.append((
                i, random.randint(1, 1000), audit_date, random.choice(audit_types),
                random.choice(regulations), random.choice(findings), random.choice(severities),
                random.randint(1, 50), random.choice(['Open', 'Closed', 'In Progress']),
                resolution
            ))
        
        conn.executemany('INSERT INTO compliance_audit_logs VALUES (?,?,?,?,?,?,?,?,?,?)', audits)
        
        conn.commit()
    
    def execute_query(self, query: str, sample_data: Optional[Dict[str, List[Dict]]] = None) -> Dict[str, Any]:
        """
        Execute SQL query in sandboxed environment
        
        Args:
            query: SQL query to execute
            sample_data: Optional custom sample data
        
        Returns:
            Dictionary with results, columns, and metadata
        """
        try:
            # Security: Block dangerous operations
            if not self._is_safe_query(query):
                return {
                    'success': False,
                    'error': 'Query contains disallowed operations. Only SELECT statements are allowed.',
                    'rows': [],
                    'columns': []
                }
            
            # Create database with sample data
            conn = self.create_sample_database(sample_data)
            
            # Execute query
            cursor = conn.execute(query)
            
            # Get results
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Convert rows to dictionaries
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            conn.close()
            
            return {
                'success': True,
                'rows': results,
                'columns': columns,
                'row_count': len(results),
                'query': query
            }
            
        except sqlite3.Error as e:
            return {
                'success': False,
                'error': f'SQL Error: {str(e)}',
                'rows': [],
                'columns': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution Error: {str(e)}',
                'rows': [],
                'columns': []
            }
    
    def _is_safe_query(self, query: str) -> bool:
        """
        Check if query is safe to execute
        Only allows SELECT statements
        """
        query_upper = query.upper().strip()
        
        # Remove comments
        query_upper = re.sub(r'--.*$', '', query_upper, flags=re.MULTILINE)
        query_upper = re.sub(r'/\*.*?\*/', '', query_upper, flags=re.DOTALL)
        
        # Check for dangerous keywords
        dangerous_keywords = [
            'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE',
            'TRUNCATE', 'REPLACE', 'ATTACH', 'DETACH', 'PRAGMA'
        ]
        
        for keyword in dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', query_upper):
                return False
        
        # Must start with SELECT (after whitespace)
        if not re.match(r'^\s*SELECT\b', query_upper):
            return False
        
        return True
    
    def _sanitize_identifier(self, identifier: str) -> str:
        """Sanitize SQL identifier (table/column name)"""
        # Remove any non-alphanumeric characters except underscore
        sanitized = re.sub(r'[^\w]', '_', identifier)
        # Ensure it doesn't start with a number
        if sanitized[0].isdigit():
            sanitized = '_' + sanitized
        return sanitized
    
    def create_share_link(self, query: str, sample_data: Optional[Dict] = None, 
                         results: Optional[Dict] = None) -> str:
        """
        Create a shareable link for a query
        
        Args:
            query: SQL query
            sample_data: Sample data used
            results: Query results
        
        Returns:
            Unique share ID
        """
        # Generate unique ID
        timestamp = datetime.now().isoformat()
        content = f"{query}_{timestamp}_{os.urandom(8).hex()}"
        share_id = hashlib.sha256(content.encode()).hexdigest()[:12]
        
        # Load existing shares
        with open(self.shares_file, 'r') as f:
            shares = json.load(f)
        
        # Store share data
        shares[share_id] = {
            'query': query,
            'sample_data': sample_data,
            'results': results,
            'created_at': timestamp,
            'view_count': 0
        }
        
        # Save shares
        with open(self.shares_file, 'w') as f:
            json.dump(shares, f, indent=2)
        
        return share_id
    
    def get_shared_query(self, share_id: str) -> Optional[Dict]:
        """
        Retrieve shared query by ID
        
        Args:
            share_id: Unique share identifier
        
        Returns:
            Share data or None if not found
        """
        try:
            with open(self.shares_file, 'r') as f:
                shares = json.load(f)
            
            if share_id in shares:
                # Increment view count
                shares[share_id]['view_count'] = shares[share_id].get('view_count', 0) + 1
                
                # Save updated view count
                with open(self.shares_file, 'w') as f:
                    json.dump(shares, f, indent=2)
                
                return shares[share_id]
            
            return None
        except Exception:
            return None
    
    def get_sample_queries(self) -> List[Dict[str, str]]:
        """Get list of sample queries for Financial Services database"""
        return [
            {
                'name': 'Account Balance Overview',
                'description': 'View customer accounts with balances',
                'category': 'Basic Queries',
                'query': '''SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    a.account_number,
    a.account_type,
    a.balance,
    a.status
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
WHERE a.status = 'Active'
LIMIT 10;'''
            },
            {
                'name': 'High-Value Transactions',
                'description': 'Find transactions over $1000',
                'category': 'Basic Queries',
                'query': '''SELECT 
    t.transaction_id,
    t.transaction_date,
    t.transaction_type,
    t.amount,
    t.merchant_name,
    t.category,
    a.account_number
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
WHERE t.amount > 1000
ORDER BY t.amount DESC
LIMIT 10;'''
            },
            {
                'name': 'Loan Portfolio Analysis',
                'description': 'Analyze loan distribution by type',
                'category': 'Analytics',
                'query': '''SELECT 
    loan_type,
    COUNT(*) as loan_count,
    ROUND(AVG(principal_amount), 2) as avg_principal,
    ROUND(AVG(interest_rate), 2) as avg_interest_rate,
    ROUND(SUM(outstanding_balance), 2) as total_outstanding
FROM loans
WHERE status = 'Active'
GROUP BY loan_type
ORDER BY total_outstanding DESC;'''
            },
            {
                'name': 'Credit Card Utilization',
                'description': 'Calculate credit utilization ratios',
                'category': 'Risk Analysis',
                'query': '''SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    cc.card_type,
    cc.credit_limit,
    cc.current_balance,
    ROUND((cc.current_balance * 100.0 / cc.credit_limit), 2) as utilization_pct
FROM customers c
JOIN credit_cards cc ON c.customer_id = cc.customer_id
WHERE cc.status = 'Active'
  AND (cc.current_balance * 100.0 / cc.credit_limit) > 70
ORDER BY utilization_pct DESC
LIMIT 10;'''
            },
            {
                'name': 'Fraud Alert Dashboard',
                'description': 'Review high-risk fraud alerts',
                'category': 'Risk Analysis',
                'query': '''SELECT 
    f.alert_id,
    f.alert_date,
    f.alert_type,
    f.risk_level,
    f.status,
    a.account_number,
    c.first_name || ' ' || c.last_name as customer_name
FROM fraud_alerts f
JOIN accounts a ON f.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
WHERE f.risk_level IN ('High', 'Critical')
  AND f.status IN ('Open', 'Investigating')
ORDER BY f.alert_date DESC
LIMIT 10;'''
            },
            {
                'name': 'Investment Portfolio Summary',
                'description': 'Analyze customer investment holdings',
                'category': 'Wealth Management',
                'query': '''SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    i.investment_type,
    COUNT(*) as position_count,
    ROUND(SUM(i.portfolio_value), 2) as total_value,
    ROUND(SUM(i.quantity * (i.current_price - i.purchase_price)), 2) as unrealized_gain_loss
FROM customers c
JOIN investments i ON c.customer_id = i.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, i.investment_type
HAVING SUM(i.portfolio_value) > 10000
ORDER BY total_value DESC
LIMIT 10;'''
            },
            {
                'name': 'Branch Performance Metrics',
                'description': 'Compare branch account and transaction volumes',
                'category': 'Analytics',
                'query': '''SELECT 
    b.branch_name,
    b.city,
    b.state,
    COUNT(DISTINCT a.account_id) as total_accounts,
    ROUND(SUM(a.balance), 2) as total_deposits,
    COUNT(DISTINCT e.employee_id) as employee_count
FROM branches b
LEFT JOIN accounts a ON b.branch_id = a.branch_id
LEFT JOIN employees e ON b.branch_id = e.branch_id
GROUP BY b.branch_id, b.branch_name, b.city, b.state
ORDER BY total_deposits DESC
LIMIT 10;'''
            },
            {
                'name': 'Customer Risk Segmentation',
                'description': 'Segment customers by risk score',
                'category': 'Risk Analysis',
                'query': '''SELECT 
    CASE 
        WHEN risk_score >= 750 THEN 'Low Risk'
        WHEN risk_score >= 650 THEN 'Medium Risk'
        WHEN risk_score >= 550 THEN 'High Risk'
        ELSE 'Very High Risk'
    END as risk_category,
    COUNT(*) as customer_count,
    ROUND(AVG(risk_score), 0) as avg_risk_score,
    customer_type
FROM customers
GROUP BY risk_category, customer_type
ORDER BY 
    CASE risk_category
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
        ELSE 4
    END;'''
            },
            {
                'name': 'Monthly Transaction Trends',
                'description': 'Analyze transaction volume and value by month',
                'category': 'Analytics',
                'query': '''SELECT 
    strftime('%Y-%m', transaction_date) as month,
    transaction_type,
    COUNT(*) as transaction_count,
    ROUND(SUM(amount), 2) as total_amount,
    ROUND(AVG(amount), 2) as avg_amount
FROM transactions
WHERE transaction_date >= date('now', '-6 months')
GROUP BY month, transaction_type
ORDER BY month DESC, total_amount DESC
LIMIT 20;'''
            },
            {
                'name': 'Compliance Audit Summary',
                'description': 'Review compliance audit findings',
                'category': 'Compliance',
                'query': '''SELECT 
    audit_type,
    regulation,
    finding,
    COUNT(*) as audit_count,
    COUNT(CASE WHEN status = 'Open' THEN 1 END) as open_count,
    COUNT(CASE WHEN status = 'Closed' THEN 1 END) as closed_count
FROM compliance_audit_logs
WHERE audit_date >= date('now', '-3 months')
GROUP BY audit_type, regulation, finding
HAVING audit_count > 2
ORDER BY open_count DESC, audit_count DESC
LIMIT 15;'''
            }
        ]
    
    def get_database_schema(self) -> Dict[str, List[Dict]]:
        """Get schema information for sample database"""
        conn = self.create_sample_database()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        
        schema = {}
        for table in tables:
            cursor = conn.execute(f"PRAGMA table_info({table})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    'name': row[1],
                    'type': row[2],
                    'nullable': not row[3]
                })
            schema[table] = columns
        
        conn.close()
        return schema
    
    def run_etl_validation_test(self, source_query: str, target_query: str) -> Dict[str, Any]:
        """
        Run ETL validation test comparing source and target queries
        
        Args:
            source_query: Query to get source data
            target_query: Query to get target/transformed data
        
        Returns:
            Comparison results with differences highlighted
        """
        source_result = self.execute_query(source_query)
        target_result = self.execute_query(target_query)
        
        if not source_result['success'] or not target_result['success']:
            return {
                'success': False,
                'error': 'One or both queries failed',
                'source_error': source_result.get('error'),
                'target_error': target_result.get('error')
            }
        
        return {
            'success': True,
            'source_count': source_result['row_count'],
            'target_count': target_result['row_count'],
            'count_match': source_result['row_count'] == target_result['row_count'],
            'source_data': source_result['rows'],
            'target_data': target_result['rows']
        }
    
    def get_data_profile(self, table_name: str) -> Dict[str, Any]:
        """
        Generate data profiling statistics for a table
        
        Args:
            table_name: Name of table to profile
        
        Returns:
            Statistics including row count, null counts, distinct values
        """
        table_name = self._sanitize_identifier(table_name)
        
        conn = self.create_sample_database()
        
        # Get row count
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        # Get column info
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        
        profile = {
            'table': table_name,
            'row_count': row_count,
            'columns': {}
        }
        
        # Profile each column
        for col in columns:
            cursor = conn.execute(f"""
                SELECT 
                    COUNT(*) as total,
                    COUNT(DISTINCT {col}) as distinct_count,
                    COUNT({col}) as non_null_count
                FROM {table_name}
            """)
            row = cursor.fetchone()
            
            null_count = row_count - row[2]
            
            profile['columns'][col] = {
                'distinct_values': row[1],
                'null_count': null_count,
                'null_percentage': round((null_count / row_count * 100), 2) if row_count > 0 else 0,
                'completeness': round((row[2] / row_count * 100), 2) if row_count > 0 else 0
            }
        
        conn.close()
        return profile
    
    def get_etl_test_templates(self) -> List[Dict[str, str]]:
        """Get common ETL test case templates"""
        return [
            {
                'name': 'Row Count Match',
                'description': 'Verify source and target have same row count',
                'source_query': 'SELECT COUNT(*) as count FROM customers',
                'target_query': 'SELECT COUNT(*) as count FROM customers',
                'expected': 'Counts should match'
            },
            {
                'name': 'NULL Handling',
                'description': 'Check NULL values are handled correctly',
                'source_query': 'SELECT customer_id, email FROM customers WHERE email IS NULL',
                'target_query': 'SELECT customer_id, COALESCE(email, \'no-email@domain.com\') as email FROM customers WHERE email IS NULL',
                'expected': 'NULLs replaced with default value'
            },
            {
                'name': 'String Transformation',
                'description': 'Verify string cleaning transformations',
                'source_query': 'SELECT phone FROM customers',
                'target_query': 'SELECT REPLACE(phone, \'-\', \'\') as phone_clean FROM customers',
                'expected': 'Hyphens removed from phone numbers'
            },
            {
                'name': 'Date Extraction',
                'description': 'Extract year/month from date fields',
                'source_query': 'SELECT created_date FROM customers',
                'target_query': 'SELECT SUBSTR(created_date, 1, 7) as year_month FROM customers',
                'expected': 'Extract YYYY-MM format'
            },
            {
                'name': 'Aggregation Validation',
                'description': 'Verify aggregated totals match detail level',
                'source_query': 'SELECT SUM(total_amount) as total FROM orders',
                'target_query': 'SELECT SUM(revenue) as total FROM (SELECT status, SUM(total_amount) as revenue FROM orders GROUP BY status)',
                'expected': 'Totals should match between detail and aggregate'
            }
        ]
