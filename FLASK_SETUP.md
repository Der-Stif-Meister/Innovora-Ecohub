# Flask Backend Setup - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings:
# - Set your Google email and app password
# - Change SECRET_KEY to something secure
```

### Step 3: Initialize Database
```bash
python app.py
```
This will create the database on first run.

### Step 4: Create Admin User
```bash
flask create-admin
```
Follow the prompts to create your first admin account.

### Step 5: Run the Server
```bash
python app.py
```
Server runs at `http://localhost:5000`

---

## 📍 Admin Access

### Login Page
```
http://localhost:5000/admin/login
```

### Dashboard
```
http://localhost:5000/admin/dashboard
```

### Features
- 📤 Upload Files (`/admin/upload`)
- 🖼️ Manage Files (`/admin/files`)
- 💬 View Messages (`/admin/messages`)

---

## 🔧 Gmail Setup for Emails

### 1. Enable 2-Factor Authentication
- Go to: https://myaccount.google.com/security
- Click "2-Step Verification"
- Follow setup steps

### 2. Create App Password
- Go to: https://myaccount.google.com/apppasswords
- Select "Mail" and "Windows Computer"
- Click "Generate"
- Copy the 16-character password

### 3. Add to .env
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

---

## 📂 Directory Structure

```
templates/
├── admin/
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── files.html
│   └── messages.html
└── errors/
    ├── 404.html
    ├── 403.html
    └── 500.html

static/
└── uploads/          # Files go here

app.py               # Main application
requirements.txt     # Dependencies
.env                 # Configuration (keep secret!)
ecohub.db           # Database (auto-created)
```

---

## 🔐 Security Checklist

Before going public:

- [ ] Change `SECRET_KEY` in .env to a random secure value
- [ ] Create a strong admin password
- [ ] Set `FLASK_ENV=production`
- [ ] Use SSL/HTTPS
- [ ] Set up regular backups
- [ ] Enable logging monitoring
- [ ] Use PostgreSQL (not SQLite) for production
- [ ] Use Gunicorn/uWSGI instead of Flask dev server

---

## 📧 Contact Form Integration

The contact form in `index.html` needs this code:

```html
<form method="POST" action="/contact">
    <input type="text" name="name" required>
    <input type="email" name="email" required>
    <input type="text" name="subject" required>
    <textarea name="message" required></textarea>
    <button type="submit">Send</button>
</form>
```

---

## 🐛 Troubleshooting

### Flask not found
```bash
pip install Flask
```

### Database errors
```bash
# Delete old database and create new one
rm ecohub.db
python app.py
flask create-admin
```

### Emails not sending
- Check .env has correct MAIL_USERNAME and MAIL_PASSWORD
- Verify Gmail App Password (not regular password)
- Check 2FA is enabled on Gmail

### Permission denied on uploads
```bash
# Create uploads folder with permissions
mkdir -p static/uploads
chmod 755 static/uploads
```

---

## 📞 API Endpoints

### Public
- `GET /` - Homepage
- `POST /contact` - Submit contact form (rate limited 5/hour)

### Admin (Login Required)
- `GET/POST /admin/login` - Login
- `GET /admin/logout` - Logout
- `GET /admin/dashboard` - Dashboard
- `GET/POST /admin/upload` - Upload files
- `GET /admin/files` - View files
- `POST /admin/file/delete/<id>` - Delete file
- `GET /admin/messages` - View messages
- `POST /admin/message/<id>/read` - Mark read

---

## 🎯 Next Steps

1. ✅ Install and test locally
2. ✅ Upload some test files
3. ✅ Test contact form emails
4. ✅ Set up custom domain
5. ✅ Deploy to production (Heroku, AWS, DigitalOcean, etc.)

---

For detailed documentation, see: **FLASK_BACKEND_README.md**
