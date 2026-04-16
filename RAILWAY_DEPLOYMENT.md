# Deploy EcoHub to Railway 🚆

Railway is the **easiest** way to deploy your Flask app - zero configuration needed!

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Add Gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

Verify `gunicorn==*` is in requirements.txt

### Step 2: Create Railway Account
1. Go to https://railway.app
2. Click "Start a new project"
3. Sign in with GitHub
4. Authorize Railway to access your repositories

### Step 3: Deploy from GitHub
1. Click "Deploy from GitHub repo"
2. Search for: `Innovora-Ecohub`
3. Select `Der-Stif-Meister/Innovora-Ecohub`
4. Click "Deploy Now"

**Railway auto-detects Flask and builds it automatically** ✅

### Step 4: Add Environment Variables
In Railway Dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add these variables:

```
FLASK_ENV          production
SECRET_KEY         your-secret-key-here-min-32-chars
DATABASE_URL       sqlite:///ecohub.db
MAIL_USERNAME      ecohubgroup5@gmail.com
MAIL_PASSWORD      your-gmail-app-password
```

### Step 5: Deploy
1. Railway auto-deploys when you push to GitHub
2. Check "Deployments" tab for build status
3. Once green ✅, your app is live

**Your public URL:** `https://[project-name].up.railway.app`

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
https://your-railway-url/
```
Should see: EcoHub homepage ✅

### 2. Test Admin Panel
```
https://your-railway-url/admin/login
```
Log in with your admin credentials

### 3. Test Contact Form
1. Scroll to #contact section
2. Fill out contact form
3. Submit
4. Check `/admin/messages` if it saved
5. Check your email if it sent

### 4. Test Language Switcher
1. Click language dropdown
2. Select another language (e.g., Spanish)
3. Page should translate
4. Contact section text should change

---

## 🔄 Auto-Deploy on Push

Once connected to GitHub, **every push to `master` automatically deploys:**

```bash
git add .
git commit -m "my changes"
git push origin master
```

Railway detects the push → rebuilds → deploys (takes ~2-3 minutes)

Check status in Railway Dashboard → "Deployments" tab

---

## 📊 Monitoring in Railway

### View Logs
```
Dashboard → Logs tab → See real-time output
```

### View Metrics
```
Dashboard → Metrics tab → CPU, Memory, Network usage
```

### View Deployments
```
Dashboard → Deployments tab → See build history
```

---

## 🔑 Troubleshooting

### "Build failed"
Check logs for errors. Common issues:
- Missing `Procfile` (Railway can infer it, but add if needed)
- Package not in `requirements.txt`
- Python version issue

**Fix:**
```bash
pip install -r requirements.txt  # Test locally
git push origin master           # Push again
```

### "App crashes on startup"
1. Check Rails logs for error
2. Verify environment variables are set
3. Ensure `app.py` is in root directory

### "Static files not loading"
- Verify CSS/JS paths use `url_for()` ✅ (already done)
- Check `static/` folder exists and has files

### "Translations not working"
- Verify `/static/js/i18n/*.json` files exist
- Check JS console for 404 errors
- Ensure paths in `i18n.js` are `/static/js/i18n/`

### "Email not sending"
1. Verify Gmail 2FA is enabled
2. Check App Password is correct (16 chars, no spaces)
3. Verify `MAIL_USERNAME` = `ecohubgroup5@gmail.com`
4. Check MAIL_PASSWORD in environment variables (no typos)

---

## 🎯 Full Railway Setup (Detailed)

### Create `.env` Locally (for testing)
```bash
# Create .env file (don't commit to GitHub)
FLASK_ENV=production
SECRET_KEY=your-super-secret-random-key-32-chars-minimum!
DATABASE_URL=sqlite:///ecohub.db
MAIL_USERNAME=ecohubgroup5@gmail.com
MAIL_PASSWORD=your-app-password
```

### Test Locally
```bash
pip install -r requirements.txt
python -m flask run
```

Visit: `http://localhost:5000` - should work ✅

### Prepare for Deployment
```bash
# Make sure gunicorn is in requirements
pip install gunicorn
pip freeze > requirements.txt

# Commit changes
git add requirements.txt
git commit -m "add: gunicorn for production"
git push origin master
```

### Deploy on Railway
1. Go to https://railway.app/dashboard
2. Click "New Project" → "Deploy from GitHub Repo"
3. Select `Innovora-Ecohub`
4. Go to "Variables" tab
5. Add all 5 environment variables
6. Railway auto-starts building
7. Wait for "Running" status (green ✅)
8. Click on project to get public URL

### Access Your Live App
```
https://[project-id].up.railway.app
```

---

## 📱 Custom Domain (Optional)

1. In Railway Dashboard: Settings → Domain
2. Add your domain (e.g., `ecohub.yourdomain.com`)
3. Follow DNS setup (CNAME record)
4. SSL automatically generated ✅

---

## 💡 Database & Admin Setup

### First Time After Deploy
Railway provides a shell:

1. In Railway Dashboard → "Shell" tab
2. Run:
```bash
flask init-db
flask create-admin
```

### Create Admin User
Enter credentials when prompted:
```
Username: admin
Email: admin@ecohub.com
Password: your-admin-password
```

---

## 🔄 Continuous Auto-Deploy

Your workflow:
```
1. Make changes locally
2. Test: python -m flask run
3. Commit: git commit -m "..."
4. Push: git push origin master
5. Railway detects push
6. Railway auto-builds (2-3 min)
7. Your live app updates automatically ✅
```

**No manual deployment needed!**

---

## 🚀 You're Live!

After deployment, you have:
- ✅ Live website at `https://your-railway-url`
- ✅ Admin panel at `https://your-railway-url/admin/login`
- ✅ Contact form that emails you
- ✅ 8-language multilingual site
- ✅ Auto-deploys on every GitHub push
- ✅ Database persisted
- ✅ Monitoring & logs available

---

## 📚 Railway Documentation

- **Main Docs:** https://docs.railway.app
- **Flask Guide:** https://docs.railway.app/guides/flask
- **Environment Variables:** https://docs.railway.app/guides/variables
- **Custom Domains:** https://docs.railway.app/guides/custom-domains

---

## ✨ Summary

| Feature | Status |
|---------|--------|
| GitHub Integration | ✅ Connected |
| Auto-Deploy | ✅ On every push |
| Environment Variables | ✅ Set in Railway |
| Database | ✅ SQLite persisted |
| Email | ✅ Gmail SMTP ready |
| Admin Panel | ✅ Deploy & test |
| SSL Certificate | ✅ Auto-generated |
| Monitoring | ✅ Logs & metrics |
| Cost | 💰 $5/month (generous free tier) |

---

**Ready? Go to https://railway.app and deploy now!** 🚀
