# Deploy EcoHub to Render 🎨

Render is the **easiest** way to deploy your Flask app with one-click GitHub integration!

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Ensure Gunicorn is Installed
```bash
pip install gunicorn
pip freeze > requirements.txt
```

Verify `gunicorn==21.2.0` is in requirements.txt ✅

### Step 2: Create Render Account
1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub
4. Authorize Render to access your repositories

### Step 3: Create Web Service
1. In Render Dashboard, click "New +" button
2. Select "Web Service"
3. Search for repo: `Innovora-Ecohub`
4. Select `Der-Stif-Meister/Innovora-Ecohub`
5. Click "Connect"

### Step 4: Configure
Fill in these settings:

**Basic Info:**
- **Name:** `innovora-ecohub`
- **Environment:** `Python 3`
- **Region:** Choose closest to your users (e.g., `us-east`)
- **Branch:** `master`

**Build Settings:**
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  gunicorn app:app
  ```

Click "Create Web Service"

### Step 5: Add Environment Variables
1. In Render Dashboard, go to your service
2. Click "Environment" tab
3. Add these variables:

```
FLASK_ENV               production
SECRET_KEY              your-secret-key-here-min-32-chars
DATABASE_URL            sqlite:///ecohub.db
MAIL_USERNAME           ecohubgroup5@gmail.com
MAIL_PASSWORD           your-gmail-app-password
```

### Step 6: Deploy
1. Render auto-starts deploying
2. Watch logs in "Logs" tab
3. Wait for "Your service is live" message
4. Your app is live at: `https://innovora-ecohub.onrender.com`

---

## 📧 Gmail App Password Setup

### Get Gmail Password:
1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification" (if not already)
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" → "Windows Computer"
5. Google generates 16-character password
6. **Remove spaces** and use as `MAIL_PASSWORD`

**Example:**
```
Given:  abcd efgh ijkl mnop
Use:    abcdefghijklmnop
```

---

## ✅ Testing After Deployment

### 1. Check if Live
```
https://innovora-ecohub.onrender.com/
```
Should see: EcoHub homepage ✅

### 2. Test Admin Panel
```
https://innovora-ecohub.onrender.com/admin/login
```
Log in with your admin credentials

### 3. Test Contact Form
1. Scroll to #contact section
2. Fill out contact form
3. Submit
4. Check `/admin/messages` if it saved

### 4. Test Language Switcher
1. Click language dropdown
2. Select another language (e.g., Spanish)
3. Entire page should translate ✅

### 5. Test Email
1. Go to contact form
2. Fill and submit
3. Check your email inbox (may take 30 seconds)

---

## 🔄 Auto-Deploy on Push

Once connected to GitHub, **every push to `master` automatically deploys:**

```bash
git add .
git commit -m "my changes"
git push origin master
```

Render detects the push → rebuilds → deploys (takes ~2-3 minutes)

Check status in Render Dashboard → "Events" tab

---

## 📊 Monitoring in Render

### View Logs
```
Dashboard → Service Page → Logs tab → See real-time output
```

### View Events
```
Dashboard → Service Page → Events tab → Deployment history
```

### View Metrics
```
Dashboard → Service Page → Metrics tab → CPU, Memory, Network
```

---

## 🔑 Troubleshooting

### "Build failed: ModuleNotFoundError"
Check logs for missing package:
```bash
# Locally verify all packages
pip install -r requirements.txt
python -m flask run  # test locally
```

Then:
```bash
pip freeze > requirements.txt
git push origin master
```

### "App crashes on startup"
1. Check Render logs for error message
2. Verify all environment variables are set (typos?)
3. Ensure `app.py` is in root directory

### "Static files 404 (not loading)"
- Verify CSS/JS paths use `url_for()` ✅ (already done)
- Check paths in templates: `{{ url_for('static', filename='css/styles.css') }}`
- Ensure `static/` folder exists in repository

### "Translations not working"
- Check browser console (F12) for 404 errors
- Verify JSON files at: `/static/js/i18n/*.json`
- Ensure `i18n.js` paths: `/static/js/i18n/{lang}.json`

### "Email not sending"
1. Verify Gmail 2FA is enabled
2. Check App Password is correct (16 chars, no spaces)
3. Verify `MAIL_USERNAME` = `ecohubgroup5@gmail.com`
4. Check `MAIL_PASSWORD` in Render env vars (no typos)
5. In Render logs, look for email send errors

### "Database doesn't persist"
- SQLite works on Render (file-based)
- Data persists between redeployments ✅
- For production, consider PostgreSQL (Render provides)

### Redeploy is failing
1. Check all environment variables are correct
2. Verify `requirements.txt` is up-to-date
3. Reset deployment:
   - Go to service settings
   - Click "Settings" → scroll down
   - Click "Delete Service"
   - Recreate following steps above

---

## 🎯 Full Render Setup (Detailed)

### Prepare Code
```bash
cd c:\Users\samue\Documents\EcoHub-Website

# Verify gunicorn is installed
pip install gunicorn

# Update requirements
pip freeze > requirements.txt

# Test locally
python -m flask run
# Should be live at http://localhost:5000
```

### Commit & Push
```bash
git add requirements.txt
git commit -m "add: gunicorn for production"
git push origin master
```

### Deploy on Render
1. Go to https://render.com/dashboard
2. Click "New Web Service"
3. Select GitHub, then `Innovora-Ecohub`
4. Fill settings (see Step 4 above)
5. Add environment variables (see Step 5 above)
6. Render auto-deploys

### Get Your Domain
```
https://innovora-ecohub.onrender.com
```

---

## 📱 Custom Domain (Optional)

1. In Render Dashboard: Settings → Custom Domain
2. Add your domain (e.g., `ecohub.yourdomain.com`)
3. Update DNS: Add CNAME record pointing to Render
4. SSL automatically generated ✅

---

## 💡 Database & Admin Setup

### First Time After Deploy
Render provides a shell. To initialize:

1. In Render Dashboard → Service Page
2. Click "Shell" tab at top
3. Run:
```bash
flask init-db
flask create-admin
```

4. Enter admin credentials:
```
Username: admin
Email: admin@ecohub.com
Password: your-admin-password
```

Or create in local Flask first, then the database file will persist.

---

## 🔄 Continuous Auto-Deploy

Your workflow:
```
1. Make changes locally
2. Test: python -m flask run
3. Commit: git commit -m "..."
4. Push: git push origin master
5. Render detects push
6. Render auto-builds (60-90 seconds)
7. Your live app updates automatically ✅
```

**No manual deployment needed!**

---

## ⚡ Free Tier Features

| Feature | Free Tier |
|---------|-----------|
| Web Services | ✅ 1 free |
| Build Minutes | ✅ 500/month |
| Auto-deploy from Git | ✅ Yes |
| SSL Certificate | ✅ Auto |
| Database (SQLite) | ✅ Yes |
| Environment Variables | ✅ Unlimited |
| Logs & Monitoring | ✅ Yes |
| Cost | 💰 Free (with limits) |

---

## 🚀 You're Live!

After deployment, you have:
- ✅ Live website: `https://innovora-ecohub.onrender.com`
- ✅ Admin panel: `https://innovora-ecohub.onrender.com/admin/login`
- ✅ Contact form that emails you
- ✅ 8-language multilingual site
- ✅ Auto-deploys on every GitHub push
- ✅ Database persisted
- ✅ Monitoring & logs available
- ✅ SSL certificate included
- ✅ No configuration needed

---

## 📚 Render Documentation

- **Main Docs:** https://render.com/docs
- **Flask Guide:** https://render.com/docs/deploy-flask
- **Environment Variables:** https://render.com/docs/environment-variables
- **Custom Domains:** https://render.com/docs/custom-domains

---

## ✨ Summary

| Step | Description | Time |
|------|-------------|------|
| 1 | Install gunicorn | 1 min |
| 2 | Create Render account | 1 min |
| 3 | Connect GitHub repo | 1 min |
| 4 | Configure web service | 2 min |
| 5 | Add environment variables | 1 min |
| 6 | Deploy & test | 3 min |
| **Total** | **Full deployment** | **~9 min** |

---

## 🎉 Deployment Complete!

Your EcoHub website is now live with:
- ✅ Production-grade hosting
- ✅ Zero infrastructure management
- ✅ Automatic scaling
- ✅ Global CDN
- ✅ Real-time logs
- ✅ One-click rollback

**Domain:** `https://innovora-ecohub.onrender.com`

**Ready? Go to https://render.com/dashboard and deploy now!** 🚀
