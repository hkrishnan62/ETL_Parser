# Keep Your App Awake 24/7 (Free Solutions)

Your app on Render's free tier sleeps after 15 minutes of inactivity. Here are free solutions to keep it awake:

---

## ✅ Option 1: UptimeRobot (Recommended)

**Best for:** Set it and forget it, completely free

### Setup Steps:
1. Go to: https://uptimerobot.com
2. Sign up for free (no credit card needed)
3. Click **"Add New Monitor"**
4. Configure:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** ETL Parser
   - **URL:** `https://etl-parser.onrender.com/health`
   - **Monitoring Interval:** 5 minutes (free tier)
5. Click **"Create Monitor"**

**Done!** Your app will be pinged every 5 minutes and never sleep.

**Free Tier:**
- ✅ 50 monitors
- ✅ 5-minute intervals
- ✅ Email alerts if down
- ✅ No credit card required

---

## Option 2: Cron-job.org

**Best for:** More frequent pings

### Setup Steps:
1. Go to: https://cron-job.org
2. Sign up for free
3. Create new cronjob:
   - **URL:** `https://etl-parser.onrender.com/health`
   - **Schedule:** Every 5 minutes (`*/5 * * * *`)
4. Save and enable

**Free Tier:**
- ✅ 1-minute intervals possible
- ✅ Unlimited jobs
- ✅ Execution history

---

## Option 3: GitHub Actions (Developer's Choice)

**Best for:** Keep everything in your repository

### Setup:
Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep App Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
  workflow_dispatch:  # Manual trigger

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Health Endpoint
        run: |
          curl -f https://etl-parser.onrender.com/health || exit 0
          echo "App is awake!"
```

**Note:** GitHub Actions may not run exactly every 10 minutes during peak times.

---

## Option 4: Easycron

**Best for:** Flexible scheduling

### Setup:
1. Go to: https://www.easycron.com
2. Sign up for free
3. Create cron job:
   - **URL:** `https://etl-parser.onrender.com/health`
   - **Interval:** Every 5 minutes
4. Enable job

**Free Tier:**
- ✅ Up to 100 executions/day
- ✅ 15-minute minimum interval (free)
- ✅ Execution logs

---

## ⚡ Quick Comparison

| Service | Interval | Setup Time | Reliability | Best For |
|---------|----------|------------|-------------|----------|
| **UptimeRobot** | 5 min | 2 min | ⭐⭐⭐⭐⭐ | Most users |
| **Cron-job.org** | 1 min | 3 min | ⭐⭐⭐⭐ | Developers |
| **GitHub Actions** | 10 min | 5 min | ⭐⭐⭐ | Keep in repo |
| **Easycron** | 15 min | 3 min | ⭐⭐⭐⭐ | Simple setup |

---

## 🎯 Recommended Setup

**For most users:**
1. Use **UptimeRobot** (easiest, most reliable)
2. Set monitor interval to 5 minutes
3. Enable email alerts
4. Done! Your app stays awake 24/7

**Why 5 minutes?**
- Render free tier sleeps after 15 minutes
- Pinging every 5 minutes ensures at most 10 minutes of inactivity
- Well within the free tier limits of all services

---

## ✅ Health Check Endpoint

Your app already has a health check endpoint configured:
- **URL:** `/health`
- **Response:** `{"status": "healthy", "timestamp": "..."}`

This endpoint is lightweight and perfect for keep-alive pings.

---

## 💡 Pro Tips

1. **Multiple Monitors:** Use 2 services (e.g., UptimeRobot + Cron-job.org) for redundancy
2. **Monitoring:** Enable email alerts to know if your app goes down
3. **Logs:** Check execution logs to verify pings are working
4. **Test First:** Manually visit your `/health` endpoint to confirm it works

---

## 🚫 What Won't Work

- Render's free tier has a 750-hour/month limit (31.25 days)
- If you exceed this, app will stop serving requests
- Solution: Upgrade to paid plan ($7/month) for unlimited hours

---

## Need Help?

If your app is still sleeping:
1. Check if health endpoint works: `curl https://your-app.onrender.com/health`
2. Verify monitor is enabled in UptimeRobot/Cron-job.org
3. Check Render logs for errors
4. Ensure you're not hitting the 750-hour limit

---

## 🎉 All Done!

Once you set up any of these services, your app will stay awake 24/7 within free tier limits!
