"""
INNOVORA ECOHUB GROUP - Flask Backend Application
Handles admin authentication, file uploads, and contact form emails
"""

import os
import logging
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

# Flask and extensions
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# APP CONFIGURATION
# ============================================

app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'

# Database Configuration
BASE_DIR = Path(__file__).resolve().parent
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{BASE_DIR}/ecohub.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration (Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'ecohubgroup5@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'dont-worry-password-is-safe...lol')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads folder if it doesn't exist
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# ============================================
# EXTENSIONS INITIALIZATION
# ============================================

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please log in to access admin features.'

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# ============================================
# LOGGING CONFIGURATION
# ============================================

logging.basicConfig(
    filename='ecohub.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# DATABASE MODELS
# ============================================

class Admin(UserMixin, db.Model):
    """Admin user model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'


class UploadedFile(db.Model):
    """Track uploaded files"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False, unique=True)
    file_size = db.Column(db.Integer)  # in bytes
    file_type = db.Column(db.String(50))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<UploadedFile {self.filename}>'


class ContactMessage(db.Model):
    """Store contact form submissions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_address = db.Column(db.String(45))
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactMessage {self.email}>'


class TeamMember(db.Model):
    """Team member profiles with advanced features"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    role = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120))
    bio = db.Column(db.Text)
    image_filename = db.Column(db.String(255))
    email = db.Column(db.String(120))
    show_email = db.Column(db.Boolean, default=False)
    
    # Social media links
    linkedin_url = db.Column(db.String(500))
    twitter_url = db.Column(db.String(500))
    facebook_url = db.Column(db.String(500))
    tiktok_url = db.Column(db.String(500))
    other_url = db.Column(db.String(500))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<TeamMember {self.name}>'


class Alert(db.Model):
    """Daily alerts displayed on homepage"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Alert {self.title}>'


# ============================================
# LOGIN MANAGER
# ============================================

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    return Admin.query.get(int(user_id))


# ============================================
# UTILITY FUNCTIONS
# ============================================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size_mb(size_bytes):
    """Convert bytes to MB"""
    return round(size_bytes / 1024 / 1024, 2)


def send_contact_email(name, email, subject, message):
    """Send email to admin when contact form is submitted"""
    try:
        msg = Message(
            subject=f'EcoHub Contact: {subject}',
            recipients=[app.config['MAIL_USERNAME']],
            html=f"""
            <h2>New Contact Message</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message.replace(chr(10), '<br>')}</p>
            <p><small>Submitted at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
            """
        )
        mail.send(msg)
        logger.info(f'Contact email sent from {email}')
        return True
    except Exception as e:
        logger.error(f'Failed to send contact email: {str(e)}')
        return False


def send_reply_email(recipient_email, name):
    """Send automatic reply to user"""
    try:
        msg = Message(
            subject='We Received Your Message - INNOVORA EcoHub Group',
            recipients=[recipient_email],
            html=f"""
            <h2>Thank You for Contacting INNOVORA EcoHub Group</h2>
            <p>Hi {name},</p>
            <p>We have received your message and appreciate you reaching out to us.</p>
            <p>Our team will review your inquiry and get back to you as soon as possible.</p>
            <p>Best regards,<br>
            <strong>INNOVORA EcoHub Group</strong></p>
            <p><small>This is an automatic reply. Please do not respond to this email.</small></p>
            """
        )
        mail.send(msg)
        logger.info(f'Reply email sent to {recipient_email}')
        return True
    except Exception as e:
        logger.error(f'Failed to send reply email: {str(e)}')
        return False


# ============================================
# ADMIN ROUTES
# ============================================

@app.route('/admin')
def admin():
    """Admin root - redirect to dashboard if authenticated, otherwise to login"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))


@app.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required.', 'error')
            logger.warning(f'Login attempt with missing credentials from {request.remote_addr}')
            return redirect(url_for('admin_login'))

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            login_user(admin)
            logger.info(f'Admin {username} logged in successfully')
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            logger.warning(f'Failed login attempt for username: {username} from {request.remote_addr}')

    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    username = current_user.username
    logout_user()
    logger.info(f'Admin {username} logged out')
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    total_files = UploadedFile.query.count()
    total_messages = ContactMessage.query.count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.submitted_at.desc()).limit(5).all()
    recent_files = UploadedFile.query.order_by(UploadedFile.uploaded_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_files=total_files,
        total_messages=total_messages,
        recent_messages=recent_messages,
        recent_files=recent_files
    )


@app.route('/admin/upload', methods=['GET', 'POST'])
@login_required
def admin_upload():
    """File upload page"""
    if request.method == 'POST':
        # Check if file is in request
        if 'file' not in request.files:
            flash('No file selected.', 'error')
            return redirect(url_for('admin_upload'))

        file = request.files['file']

        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('admin_upload'))

        # Validate file
        if not allowed_file(file.filename):
            flash(f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
            return redirect(url_for('admin_upload'))

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            flash(f'File size exceeds {get_file_size_mb(MAX_FILE_SIZE)}MB limit.', 'error')
            return redirect(url_for('admin_upload'))

        try:
            # Save file securely
            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)

            # Record in database
            uploaded_file = UploadedFile(
                filename=filename,
                original_filename=secure_filename(file.filename),
                file_path=f'/static/uploads/{filename}',
                file_size=file_size,
                file_type=file.filename.rsplit('.', 1)[1].lower(),
                uploaded_by=current_user.id
            )
            db.session.add(uploaded_file)
            db.session.commit()

            logger.info(f'File uploaded: {filename} by {current_user.username}')
            flash(f'File "{file.filename}" uploaded successfully ({get_file_size_mb(file_size)}MB).', 'success')
            return redirect(url_for('admin_files'))

        except Exception as e:
            logger.error(f'File upload error: {str(e)}')
            flash('An error occurred while uploading the file.', 'error')
            return redirect(url_for('admin_upload'))

    return render_template('admin/upload.html')


@app.route('/admin/files')
@login_required
def admin_files():
    """Display uploaded files"""
    page = request.args.get('page', 1, type=int)
    files = UploadedFile.query.order_by(UploadedFile.uploaded_at.desc()).paginate(page=page, per_page=12)
    return render_template('admin/files.html', files=files)


@app.route('/admin/file/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    """Delete uploaded file"""
    uploaded_file = UploadedFile.query.get_or_404(file_id)

    # Security: Only admin who uploaded can delete (optional: allow any admin)
    # if uploaded_file.uploaded_by != current_user.id:
    #     flash('You do not have permission to delete this file.', 'error')
    #     return redirect(url_for('admin_files'))

    try:
        file_path = os.path.join(BASE_DIR, uploaded_file.file_path.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(uploaded_file)
        db.session.commit()

        logger.info(f'File deleted: {uploaded_file.filename} by {current_user.username}')
        flash(f'File "{uploaded_file.original_filename}" deleted successfully.', 'success')

    except Exception as e:
        logger.error(f'File deletion error: {str(e)}')
        flash('An error occurred while deleting the file.', 'error')

    return redirect(url_for('admin_files'))


@app.route('/admin/messages')
@login_required
def admin_messages():
    """View contact messages"""
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.submitted_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/messages.html', messages=messages)


@app.route('/admin/message/<int:message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    """Mark message as read"""
    message = ContactMessage.query.get_or_404(message_id)
    message.read = True
    db.session.commit()
    logger.info(f'Message {message_id} marked as read by {current_user.username}')
    return jsonify({'status': 'success'})


# ============================================
# TEAM MANAGEMENT ROUTES
# ============================================

@app.route('/admin/team')
@login_required
def admin_team():
    """View all team members"""
    page = request.args.get('page', 1, type=int)
    team_members = TeamMember.query.order_by(TeamMember.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('admin/team.html', team_members=team_members)


@app.route('/admin/team/add', methods=['GET', 'POST'])
@login_required
def admin_team_add():
    """Add new team member"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            role = request.form.get('role', '').strip()
            department = request.form.get('department', '').strip()
            bio = request.form.get('bio', '').strip()
            email = request.form.get('email', '').strip()
            show_email = request.form.get('show_email') == 'on'
            
            linkedin_url = request.form.get('linkedin_url', '').strip()
            twitter_url = request.form.get('twitter_url', '').strip()
            facebook_url = request.form.get('facebook_url', '').strip()
            tiktok_url = request.form.get('tiktok_url', '').strip()
            other_url = request.form.get('other_url', '').strip()
            
            # Validation
            if not name or not role:
                flash('Name and role are required.', 'error')
                return redirect(url_for('admin_team_add'))

            # Handle image upload
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
                    image_filename = timestamp + 'team_' + filename
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    file.save(file_path)
                    logger.info(f'Team image uploaded: {image_filename}')

            # Create team member
            team_member = TeamMember(
                name=name,
                role=role,
                department=department,
                bio=bio,
                email=email,
                show_email=show_email,
                image_filename=image_filename,
                linkedin_url=linkedin_url,
                twitter_url=twitter_url,
                facebook_url=facebook_url,
                tiktok_url=tiktok_url,
                other_url=other_url
            )
            db.session.add(team_member)
            db.session.commit()

            logger.info(f'Team member added: {name} ({role})')
            flash(f'Team member "{name}" added successfully!', 'success')
            return redirect(url_for('admin_team'))

        except Exception as e:
            logger.error(f'Error adding team member: {str(e)}')
            flash('An error occurred while adding team member.', 'error')
            return redirect(url_for('admin_team_add'))

    return render_template('admin/team_add.html')


@app.route('/admin/team/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_team_edit(team_id):
    """Edit team member"""
    team_member = TeamMember.query.get_or_404(team_id)
    
    if request.method == 'POST':
        try:
            team_member.name = request.form.get('name', '').strip()
            team_member.role = request.form.get('role', '').strip()
            team_member.department = request.form.get('department', '').strip()
            team_member.bio = request.form.get('bio', '').strip()
            team_member.email = request.form.get('email', '').strip()
            team_member.show_email = request.form.get('show_email') == 'on'
            
            team_member.linkedin_url = request.form.get('linkedin_url', '').strip()
            team_member.twitter_url = request.form.get('twitter_url', '').strip()
            team_member.facebook_url = request.form.get('facebook_url', '').strip()
            team_member.tiktok_url = request.form.get('tiktok_url', '').strip()
            team_member.other_url = request.form.get('other_url', '').strip()
            
            # Validation
            if not team_member.name or not team_member.role:
                flash('Name and role are required.', 'error')
                return redirect(url_for('admin_team_edit', team_id=team_id))

            # Handle image upload (optional)
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    # Delete old image if exists
                    if team_member.image_filename:
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], team_member.image_filename)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    # Save new image
                    filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
                    image_filename = timestamp + 'team_' + filename
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    file.save(file_path)
                    team_member.image_filename = image_filename
                    logger.info(f'Team image updated: {image_filename}')

            db.session.commit()

            logger.info(f'Team member updated: {team_member.name}')
            flash(f'Team member "{team_member.name}" updated successfully!', 'success')
            return redirect(url_for('admin_team'))

        except Exception as e:
            logger.error(f'Error updating team member: {str(e)}')
            flash('An error occurred while updating team member.', 'error')
            return redirect(url_for('admin_team_edit', team_id=team_id))

    return render_template('admin/team_edit.html', team_member=team_member)


@app.route('/admin/team/<int:team_id>/delete', methods=['POST'])
@login_required
def delete_team_member(team_id):
    """Delete team member"""
    team_member = TeamMember.query.get_or_404(team_id)
    
    try:
        # Delete image file if exists
        if team_member.image_filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], team_member.image_filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        db.session.delete(team_member)
        db.session.commit()

        logger.info(f'Team member deleted: {team_member.name}')
        flash(f'Team member "{team_member.name}" deleted successfully.', 'success')

    except Exception as e:
        logger.error(f'Error deleting team member: {str(e)}')
        flash('An error occurred while deleting team member.', 'error')

    return redirect(url_for('admin_team'))


# ============================================
# ALERT MANAGEMENT ROUTES
# ============================================

@app.route('/admin/alerts')
@login_required
def admin_alerts():
    """View all alerts"""
    page = request.args.get('page', 1, type=int)
    alerts = Alert.query.order_by(Alert.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/alerts.html', alerts=alerts)


@app.route('/admin/alerts/add', methods=['GET', 'POST'])
@login_required
def admin_alerts_add():
    """Add new alert"""
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            message = request.form.get('message', '').strip()

            # Validation
            if not title or not message:
                flash('Title and message are required.', 'error')
                return redirect(url_for('admin_alerts_add'))

            # Create alert (automatically set as active)
            alert = Alert(
                title=title,
                message=message,
                is_active=True
            )
            db.session.add(alert)
            db.session.commit()

            logger.info(f'Alert created: {title}')
            flash(f'Alert "{title}" created successfully!', 'success')
            return redirect(url_for('admin_alerts'))

        except Exception as e:
            logger.error(f'Error creating alert: {str(e)}')
            flash('An error occurred while creating alert.', 'error')
            return redirect(url_for('admin_alerts_add'))

    return render_template('admin/alerts_add.html')


@app.route('/admin/alerts/<int:alert_id>/toggle', methods=['POST'])
@login_required
def toggle_alert(alert_id):
    """Toggle alert active status"""
    alert = Alert.query.get_or_404(alert_id)
    
    try:
        alert.is_active = not alert.is_active
        db.session.commit()
        
        status = 'activated' if alert.is_active else 'deactivated'
        logger.info(f'Alert {status}: {alert.title}')
        flash(f'Alert {status} successfully.', 'success')

    except Exception as e:
        logger.error(f'Error toggling alert: {str(e)}')
        flash('An error occurred while toggling alert.', 'error')

    return redirect(url_for('admin_alerts'))


@app.route('/admin/alerts/<int:alert_id>/delete', methods=['POST'])
@login_required
def delete_alert(alert_id):
    """Delete alert"""
    alert = Alert.query.get_or_404(alert_id)
    
    try:
        db.session.delete(alert)
        db.session.commit()

        logger.info(f'Alert deleted: {alert.title}')
        flash('Alert deleted successfully.', 'success')

    except Exception as e:
        logger.error(f'Error deleting alert: {str(e)}')
        flash('An error occurred while deleting alert.', 'error')

    return redirect(url_for('admin_alerts'))


# ============================================
# PUBLIC TEAM PAGE
# ============================================

@app.route('/team')
def team():
    """Display team members"""
    team_members = TeamMember.query.order_by(TeamMember.created_at.asc()).all()
    active_alert = Alert.query.filter_by(is_active=True).order_by(Alert.created_at.desc()).first()
    return render_template('team.html', team_members=team_members, active_alert=active_alert)


@app.route('/project/cocoa-husks')
def project_cocoa():
    """Display Cocoa Husks Sustainability Project"""
    active_alert = Alert.query.filter_by(is_active=True).order_by(Alert.created_at.desc()).first()
    return render_template('project_cocoa.html', active_alert=active_alert)


# ============================================
# PUBLIC ROUTES
# ============================================

@app.route('/')
def index():
    """Homepage - pass active alert"""
    active_alert = Alert.query.filter_by(is_active=True).order_by(Alert.created_at.desc()).first()
    return render_template('index.html', active_alert=active_alert)


@app.route('/contact', methods=['POST'])
@limiter.limit("5 per hour")
def contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Validation
        if not all([name, email, subject, message]):
            flash('All fields are required.', 'error')
            return redirect(request.referrer or url_for('index'))

        if len(message) < 10:
            flash('Message must be at least 10 characters long.', 'error')
            return redirect(request.referrer or url_for('index'))

        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[1]:
            flash('Please enter a valid email address.', 'error')
            return redirect(request.referrer or url_for('index'))

        # Save to database
        contact_msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=request.remote_addr
        )
        db.session.add(contact_msg)
        db.session.commit()

        # Send emails
        admin_email_sent = send_contact_email(name, email, subject, message)
        reply_email_sent = send_reply_email(email, name.split()[0])

        if admin_email_sent and reply_email_sent:
            logger.info(f'Contact form submitted by {email}')
            flash('Thank you for your message! We will get back to you soon.', 'success')
        else:
            logger.warning(f'Email sending partially failed for contact from {email}')
            flash('Message received, but there was an issue sending confirmation email.', 'warning')

        return redirect(request.referrer or url_for('index'))

    except Exception as e:
        logger.error(f'Contact form error: {str(e)}')
        flash('An error occurred while processing your message. Please try again.', 'error')
        return redirect(request.referrer or url_for('index'))


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f'404 error: {request.path}')
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f'500 error: {str(error)}')
    return render_template('errors/500.html'), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return render_template('errors/403.html'), 403


# ============================================
# CONTEXT PROCESSORS
# ============================================

@app.context_processor
def inject_config():
    """Inject configuration into templates"""
    return dict(
        app_name='INNOVORA EcoHub Group',
        current_year=datetime.utcnow().year
    )


# ============================================
# INITIALIZATION & CLI COMMANDS
# ============================================

@app.shell_context_processor
def make_shell_context():
    """Add to shell context"""
    return {'db': db, 'Admin': Admin, 'UploadedFile': UploadedFile, 'ContactMessage': ContactMessage}


@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    logger.info('Database initialized')
    print('✓ Database initialized')


@app.cli.command()
def create_admin():
    """Create a new admin user"""
    username = input('Enter admin username: ').strip()
    email = input('Enter admin email: ').strip()
    password = input('Enter admin password: ').strip()

    if not all([username, email, password]):
        print('✗ All fields are required')
        return

    if Admin.query.filter_by(username=username).first():
        print('✗ Username already exists')
        return

    if Admin.query.filter_by(email=email).first():
        print('✗ Email already exists')
        return

    try:
        admin = Admin(username=username, email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        logger.info(f'Admin user created: {username}')
        print(f'✓ Admin user "{username}" created successfully')
    except Exception as e:
        logger.error(f'Failed to create admin: {str(e)}')
        print(f'✗ Error: {str(e)}')
        db.session.rollback()


# ============================================
# APP ENTRY POINT
# ============================================

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()

    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
