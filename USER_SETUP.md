# 📦 Quick Setup for Third-Party Users

## 🚀 3 Simple Steps to Run

### Step 1: Get the Code
```bash
git clone https://github.com/hkrishnan62/ETL_Parser.git
cd ETL_Parser
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

**That's it!** Open your browser to: **http://localhost:5000**

---

## 🎯 What You Can Do

1. **Upload CSV Mapping** - Your ETL mapping document
2. **Configure** - Set source/target tables
3. **Generate** - Get SQL validation queries instantly
4. **Download** - Copy queries to use in your database

---

## 🤖 Optional: Enable AI Features

AI features are **optional** but provide smart suggestions and optimization.

**To Enable:**
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Get OpenAI API key from: https://platform.openai.com

# 3. Edit .env file and add your key:
# OPENAI_API_KEY=sk-your-key-here

# 4. Restart application
python app.py
```

**AI Features Include:**
- 🧠 Intelligent transformation suggestions
- 💬 Natural language to SQL mapping
- ⚡ Query optimization for your database
- 📊 Mapping quality analysis

---

## 📖 CSV Format

Your CSV file should have these columns:

```csv
source_column,target_column,transformation,is_key
customer_id,customer_id,source_table.customer_id,TRUE
first_name,full_name,"CONCAT(source_table.first_name, ' ', source_table.last_name)",FALSE
email,email_address,LOWER(TRIM(source_table.email)),FALSE
```

See `examples/sample_mapping.csv` for more examples.

---

## 🐳 Alternative: Docker

If you prefer Docker:

```bash
# Clone repository
git clone https://github.com/hkrishnan62/ETL_Parser.git
cd ETL_Parser

# (Optional) Configure AI
cp .env.example .env
# Edit .env with your API key

# Run with Docker
docker-compose up -d

# Access at: http://localhost:5000
```

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Stop existing process on port 5000
# Then restart the app
python app.py
```

### Module Not Found Error
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Errors
```bash
# Use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## 📚 Documentation

- **[README.md](README.md)** - Complete documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** - Comprehensive guide
- **[AI_FEATURES.md](AI_FEATURES.md)** - AI features documentation

---

## 💡 Need Help?

- Check examples in `examples/` folder
- Read the documentation files
- Run demo: `python demo.py`
- Open an issue on GitHub

---

## ⚡ Quick Test

Test the application with sample data:

```bash
# Run example script
python example_usage.py

# Output will be in output/ directory
```

---

**You're ready to use the ETL Parser!** 🎉

Open **http://localhost:5000** and start generating validation queries!
