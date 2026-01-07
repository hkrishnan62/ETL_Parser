# 🚀 Deploy ETL Parser to Free Web Hosting

Your ETL Parser is ready to deploy! Choose any of these **FREE** hosting options:

---

## ⭐ Option 1: Render.com (RECOMMENDED)

**Best for:** Easy deployment, auto-deploys from GitHub

### Quick Deploy Steps:
1. Go to: https://render.com
2. Sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select repository: `hkrishnan62/ETL_Parser`
5. Render auto-detects settings from `render.yaml`
6. Click **"Create Web Service"**

**Done!** Your app will be live at: `https://etl-parser.onrender.com`

### Settings (Auto-detected):
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app`
- **Python Version:** 3.12.1

**Free Tier Limits:**
- ✅ 750 hours/month
- ⚠️ Spins down after 15 min inactivity (wakes in ~30 sec)
- ✅ 512 MB RAM
- ✅ Custom domain support

---

## Option 2: Railway.app

**Best for:** Modern UI, fast deployment

### Quick Deploy Steps:
1. Go to: https://railway.app
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose `hkrishnan62/ETL_Parser`
5. Railway auto-deploys!

**Your app:** `https://etl-parser.up.railway.app`

**Free Tier Limits:**
- ✅ $5 credit/month (~500 hours)
- ✅ Always on (no sleep)
- ✅ 512 MB RAM

---

## Option 3: PythonAnywhere

**Best for:** Python-specific hosting, always on

### Setup Steps:
1. Go to: https://www.pythonanywhere.com
2. Sign up for free account
3. Open **Bash console** and run:
   ```bash
   git clone https://github.com/hkrishnan62/ETL_Parser.git
   cd ETL_Parser
   pip install --user -r requirements.txt
   ```
4. Go to **"Web" tab** → **"Add a new web app"**
5. Choose **"Flask"** → **Python 3.10**
6. Set working directory to `/home/yourusername/ETL_Parser`
7. Edit WSGI file to point to `app:app`

**Your app:** `https://yourusername.pythonanywhere.com`

**Free Tier Limits:**
- ✅ Always on (no sleep!)
- ⚠️ 1 web app only
- ✅ 512 MB storage

---

## Option 4: Fly.io

**Best for:** Global edge deployment

### Quick Deploy:
1. Install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Run in your project folder:
   ```bash
   fly launch
   fly deploy
   ```

**Free Tier:**
- ✅ 3 shared-cpu VMs
- ✅ 3GB storage
- ✅ 160GB outbound data

---

## 🔧 Configuration Files Included

Your repository already has these deployment files:

- ✅ `Procfile` - For Heroku/Render
- ✅ `render.yaml` - One-click Render deployment
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - All dependencies

---

## 🔐 Environment Variables

If using AI features, set these in your hosting platform:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### How to set on Render:
- Dashboard → Your Service → Environment → Add `OPENAI_API_KEY`

### How to set on Railway:
- Dashboard → Variables → Add `OPENAI_API_KEY`

### How to set on PythonAnywhere:
- Web tab → "Environment variables" section

---

## ✅ Verify Deployment

After deployment, test your app:

1. **Visit your URL** (e.g., `https://etl-parser.onrender.com`)
2. **Upload a CSV mapping file**
3. **Generate SQL validation queries**

---

## 🎯 Recommended: Render.com

For most users, **Render.com** is the easiest:
- ✅ No credit card required
- ✅ Deploys directly from GitHub
- ✅ Auto-updates when you push changes
- ✅ Free SSL certificate
- ✅ Easy environment variable management

**Deploy Now:** https://render.com/deploy

---

## 📱 Access Your App

Once deployed, you can access your ETL Parser from:
- 🖥️ Any computer's web browser
- 📱 Mobile phones/tablets
- 👥 Share the URL with your team

No installation needed for users - just visit the URL!

---

## 🆘 Troubleshooting

### App won't start:
- Check logs in your hosting dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version matches `runtime.txt`

### Upload not working:
- Some hosts have file size limits (usually 10-50 MB)
- Check your hosting plan's limits

### Need help?
- Check your host's documentation
- Review deployment logs for error messages

---

## 🚀 What's Next?

1. **Deploy** using Option 1 (Render)
2. **Test** your live application
3. **Share** the URL with users
4. **Monitor** usage from hosting dashboard

Your ETL Parser is now accessible worldwide! 🌍
