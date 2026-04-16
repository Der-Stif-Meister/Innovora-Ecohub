# INNOVORA EcoHub - Flask Backend Application

Production-ready Flask backend for the INNOVORA EcoHub Group website with admin authentication, file upload management, and contact form handling.

## Features

### 🔐 Authentication
- Admin login/logout system using Flask-Login
- Secure password hashing (Werkzeug security)
- Session management with login_required decorator
- Rate limiting on login (5 attempts per minute)

### 📁 File Upload Management
- Support for PNG, JPG, JPEG, WebP, GIF formats
- 5MB file size limit
- Secure filename handling (prevents directory traversal)
- File tracking in SQLite database
- Admin dashboard for file management and deletion

### 📧 Contact Form & Email
- Flask-Mail integration with Gmail SMTP
- Contact form validation
- Automatic admin notification emails
- Automatic confirmation emails to users
- Contact message storage in database
- Rate limiting (5 per hour)

### 📊 Admin Dashboard
- View statistics (total files, total messages)
- Recent messages and file uploads
- File gallery with previews
- Contact message management
- Message read/unread status tracking

### 🔒 Security Features
- CSRF protection ready
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection with template escaping
- Secure file uploads validation
- Password hashing with Werkzeug
- Login required decorators
- Rate limiting on forms

### 📝 Logging & Error Handling
- File-based logging to `ecohub.log`
- Error pages (404, 403, 500)
- Comprehensive error handling
- Request logging

## Installation & Setup

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy and edit .env file
cp .env.example .env

# Edit .env with your settings:
```

**Important environment variables:**
```
FLASK_ENV=development                          # Set to 'production' for deployment
SECRET_KEY=your-secret-key-change-in-prod      # Generate a secure key
MAIL_USERNAME=your-email@gmail.com             # Gmail account
MAIL_PASSWORD=your-google-app-password         # Gmail app password (not regular password!)
DATABASE_URL=sqlite:///ecohub.db               # Database location
```

### 3. Gmail Configuration (for email sending)

1. Enable 2-Factor Authentication on your Gmail account
2. Create an App Password: https://myaccount.google.com/apppasswords
3. Copy the 16-character password to `MAIL_PASSWORD` in .env

### 4. Initialize Database

```bash
# Create database and tables
flask shell
>>> from app import db, Admin
>>> db.create_all()
>>> exit()

# OR use CLI command
python app.py  # This creates tables on first run
```

### 5. Create Admin User

```bash
# Use Flask CLI
flask create-admin

# Enter username, email, and password when prompted
```

Alternatively, create programmatically:
```python
from app import app, db, Admin

with app.app_context():
    admin = Admin(username='admin', email='admin@example.com')
    admin.set_password('secure_password_here')
    db.session.add(admin)
    db.session.commit()
```

### 6. Run Development Server

```bash
python app.py

# Server runs at http://localhost:5000
```

## Routes

### Public Routes
- `GET /` → Homepage
- `POST /contact` → Handle contact form (rate limited: 5/hour)

### Admin Routes (require login)
- `GET/POST /admin/login` → Admin login
- `GET /admin/logout` → Admin logout
- `GET /admin/dashboard` → Dashboard (statistics & recent items)
- `GET/POST /admin/upload` → File upload page
- `GET /admin/files` → Gallery of uploaded files
- `POST /admin/file/delete/<id>` → Delete a file
- `GET /admin/messages` → View contact messages
- `POST /admin/message/<id>/read` → Mark message as read

## Project Structure

```
EcoHub-Website/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── ecohub.db                  # SQLite database (created on first run)
├── ecohub.log                 # Application logs
│
├── static/
│   └── uploads/              # Uploaded files directory
│
└── templates/
    ├── index.html            # Homepage (from existing site)
    ├── admin/
    │   ├── login.html        # Login page
    │   ├── dashboard.html    # Admin dashboard
    │   ├── upload.html       # File upload page
    │   ├── files.html        # File gallery
    │   └── messages.html     # Message management
    └── errors/
        ├── 404.html          # Not found error
        ├── 403.html          # Forbidden error
        └── 500.html          # Server error
```

## Database Models

### Admin
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`
- `is_active`

### UploadedFile
- `id` (Primary Key)
- `filename`
- `original_filename`
- `file_path`
- `file_size`
- `file_type`
- `uploaded_by` (Foreign Key to Admin)
- `uploaded_at`

### ContactMessage
- `id` (Primary Key)
- `name`
- `email`
- `subject`
- `message`
- `submitted_at`
- `ip_address`
- `read` (Boolean)

## CLI Commands

```bash
# Initialize database
flask init-db

# Create admin user (interactive)
flask create-admin
```

## Email Configuration Examples

### Gmail (Recommended)
1. Enable 2FA: https://support.google.com/accounts/help/34918
2. Create App Password: https://myaccount.google.com/apppasswords
3. Use 16-char password in `.env`

### Alternative: Outlook/Office365
```
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

## Security Best Practices

✅ **Implemented:**
- Hashed passwords with Werkzeug
- CSRF protection framework (add tokens to forms if needed)
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection via template escaping
- Secure file uploads validation
- Rate limiting on sensitive endpoints
- Login required decorators
- Session management

⚠️ **Before Production:**
- Change `SECRET_KEY` to a secure random value
- Set `FLASK_ENV=production`
- Use a production WSGI server (Gunicorn, uWSGI)
- Enable HTTPS/SSL
- Use PostgreSQL instead of SQLite
- Set strong admin password
- Configure allowed file extensions carefully
- Set up regular database backups
- Enable logging and monitoring

## Deployment (Production)

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run app
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables (Production)

```bash
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-app-password
```

## Troubleshooting

### Emails not sending
- Check MAIL_USERNAME and MAIL_PASSWORD in .env
- Verify Gmail App Password (not regular password)
- Check if 2FA is enabled on Gmail account
- Allow "Less secure apps" if using regular password

### File uploads failing
- Verify `static/uploads/` folder exists
- Check file permissions
- Confirm file size < 5MB
- Verify file type is in allowed list

### Database errors
- Delete `ecohub.db` and run `python app.py` to reinitialize
- Check database path in .env
- Ensure write permissions to database directory

### Login issues
- Verify admin user was created: `flask shell` → `Admin.query.all()`
- Check password hash: `admin.check_password('password')`
- Clear browser cookies and try again

## Support & Documentation

- Flask: https://flask.palletsprojects.com/
- Flask-Login: https://flask-login.readthedocs.io/
- Flask-Mail: https://pythonhosted.org/Flask-Mail/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Werkzeug: https://werkzeug.palletsprojects.com/

## License

© 2026 INNOVORA EcoHub Group. All rights reserved.
