# EcoHub Website - GitHub Deployment Guide

Your repository is live at: **https://github.com/Der-Stif-Meister/Innovora-Ecohub**

---

## 🚀 Deployment Options (Pick One)

### **OPTION 1: Render (RECOMMENDED - Easiest)**
✅ Free tier available | ✅ Direct GitHub integration | ✅ Auto-deploys on push

#### Steps:
1. Go to https://render.com
2. Sign up with GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repo: `Der-Stif-Meister/Innovora-Ecohub`
5. Fill in these settings:
   - **Name:** `innovora-ecohub`
   - **Environment:** `Python 3.12`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Add environment variables (Settings tab):
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here-min-32-chars
   DATABASE_URL=sqlite:///ecohub.db
   MAIL_USERNAME=ecohubgroup5@gmail.com
   MAIL_PASSWORD=your-app-password
   ```
7. Select free tier and deploy
8. Your app will be at: `https://innovora-ecohub.onrender.com`

**Auto-deploy on every push to GitHub** ✅

---

### **OPTION 2: Railway (FREE - Very Simple)**
✅ Zero configuration | ✅ GitHub auto-deploy | ✅ Generous free tier

#### Steps:
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Create Project" → "Deploy from GitHub Repo"
4. Select `Der-Stif-Meister/Innovora-Ecohub`
5. Railway auto-detects this is a Flask app
6. Add these environment variables in dashboard:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///ecohub.db
   MAIL_USERNAME=ecohubgroup5@gmail.com
   MAIL_PASSWORD=your-app-password
   ```
7. Deploy button automatically deploys
8. Get your public URL from the Railway dashboard

**Auto-deploy on every push** ✅

---

### **OPTION 3: Heroku (Legacy but Works)**
⚠️ Free tier removed (2022), but paid options available

If you want to use Heroku, you'll need to add a Procfile:

```bash
# Create Procfile in root directory
web: gunicorn app:app
```

Then:
```bash
heroku login
heroku create innovora-ecohub
git push heroku master
```

---

### **OPTION 4: GitHub Actions + Azure/AWS (Advanced)**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to [Your-Hosting]
        run: |
          # Your deployment script here
```

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] `.env` file created with all required variables
- [ ] `gunicorn` installed (already in requirements.txt? Add if not)
- [ ] Database migrations ready (SQLite auto-creates)
- [ ] Admin user created
- [ ] Email credentials configured (Gmail SMTP)

### Install gunicorn if missing:
```bash
pip install gunicorn
```

### Update requirements.txt:
```bash
pip freeze > requirements.txt
```

Then add if not present:
```
gunicorn==21.2.0
```

---

## 🔑 Environment Variables Needed

Create a `.env` file with these (DO NOT commit to GitHub):

```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-min-32-chars-change-this!
DATABASE_URL=sqlite:///ecohub.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=ecohubgroup5@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=ecohubgroup5@gmail.com
```

### Get Gmail App Password:
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Go to "App Passwords" section
4. Generate password for "Mail" on "Windows Computer"
5. Use that 16-character password (remove spaces)

---

## 📧 Gmail SMTP Setup

### Create Gmail App Password:
1. Enable 2FA on your Gmail account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer"
4. Copy the 16-character password
5. Paste into `MAIL_PASSWORD` in `.env`

**Example:**
```
MAIL_USERNAME=ecohubgroup5@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop  (remove spaces: abcdefghijklmnop)
```

---

## 🎯 Recommended: Render Deployment (Step-by-Step)

### Step 1: Ensure code is on GitHub
```bash
cd "c:\Users\samue\Documents\EcoHub-Website"
git status
git push origin master
```

### Step 2: Add gunicorn to requirements.txt
```bash
echo "gunicorn==21.2.0" >> requirements.txt
git add requirements.txt
git commit -m "add: gunicorn for production deployment"
git push origin master
```

### Step 3: Create Render account
- Visit https://render.com
- Sign up with GitHub (click "GitHub" button)
- Authorize repository access

### Step 4: Create Web Service
- Click "New +" → "Web Service"
- Search for repo: `Der-Stif-Meister/Innovora-Ecohub`
- Click "Connect"

### Step 5: Configure
- **Name:** `innovora-ecohub`
- **Environment:** `Python 3.12`
- **Region:** Choose closest to your users
- **Branch:** `master`
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  gunicorn app:app
  ```

### Step 6: Environment Variables
Click "Environment" tab, add:

```
FLASK_ENV            production
SECRET_KEY           your-secret-key-min-32-chars
DATABASE_URL         sqlite:///ecohub.db
MAIL_USERNAME        ecohubgroup5@gmail.com
MAIL_PASSWORD        your-app-password
```

### Step 7: Deploy
- Select Free tier (if applicable)
- Click "Create Web Service"
- Render auto-deploys from GitHub
- Get your URL: `https://innovora-ecohub.onrender.com`

### Step 8: Auto-Deploy on Push
- Every time you push to `master` branch
- Render automatically redeploys
- Check "Deployments" tab for status

---

## 🔄 After Deployment

### Initialize Database
```bash
# SSH into deployed app and run:
flask init-db
flask create-admin
```

Or run via Render dashboard:
- Click "Shell" tab
- Run: `flask init-db && flask create-admin`

### Access Admin Panel
```
https://your-deployed-url/admin/login
```

### Monitor Logs
- Render Dashboard → "Logs" tab
- See real-time application output

---

## 🐛 Troubleshooting

### app.py module not found
- Ensure `app.py` is in root directory
- Render should auto-detect it

### Database errors
```bash
# Reinitialize database
flask init-db
```

### Email not sending
- Verify Gmail App Password (16 chars, no spaces)
- Check 2FA is enabled on Gmail
- Verify MAIL_USERNAME matches email

### Static files not loading
- Check paths use `url_for()` in templates ✅ (Already done)
- Ensure `static/` folder is in root

### Translation files not loading
- Verify paths in `static/js/i18n.js`: `/static/js/i18n/`
- Check JSON files are in correct location

---

## 📊 Post-Deployment Monitoring

### Check Admin Dashboard
1. Visit `/admin/login`
2. Log in with admin credentials
3. Upload test images
4. Send test contact form

### Monitor Email
- Check if contact form emails arrive at admin email
- Verify messages appear in `/admin/messages`

### Performance Monitoring
- Render provides basic metrics
- Check for errors in Logs tab

---

## 💡 Next Steps

1. **Choose platform** (Render recommended)
2. **Add gunicorn** to requirements.txt
3. **Create account** on chosen platform
4. **Connect GitHub repo**
5. **Set environment variables**
6. **Deploy** with one click
7. **Test** admin panel and forms
8. **Enable auto-deploy** (happens automatically)

---

## 📱 Custom Domain (Optional)

Once deployed, you can add custom domain:

### Render:
1. Dashboard → Custom Domain
2. Add: `ecohub.yourdomain.com`
3. Follow DNS setup instructions
4. SSL certificate auto-generates

### Railway:
1. Settings → Custom Domain
2. Similar setup as Render

---

## 🔐 Security Notes

- **Never commit `.env`** to GitHub
- **Use strong SECRET_KEY** (min 32 random characters)
- **Enable 2FA** on Gmail account
- **Use App Password**, not main Gmail password
- **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`

---

## ✅ Deployment Complete!

Your EcoHub website will be:
- ✅ Live on the internet
- ✅ Auto-deploys on every GitHub push
- ✅ Database persisted
- ✅ Email notifications working
- ✅ Admin panel accessible
- ✅ Full multilingual support

Your public URL will be: **`https://innovora-ecohub.onrender.com`** (or your chosen platform)

---

## Support Links

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://railway.app/docs
- **Flask Deployment:** https://flask.palletsprojects.com/deployment/
- **Gunicorn Docs:** https://gunicorn.org/

Good luck! 🚀
