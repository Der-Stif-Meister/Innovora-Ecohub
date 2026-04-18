#!/usr/bin/env python3
"""
Database Verification Script for EcoHub Application
Ensures all tables and columns exist without dropping or modifying existing data
SAFE: Uses SQLAlchemy inspection to check schema without modifying it
"""

import sys
from app import app, db
from sqlalchemy import inspect

def verify_database():
    """Verify database schema is correct"""
    print("\n" + "="*60)
    print("🔍 ECOHUB DATABASE VERIFICATION")
    print("="*60 + "\n")
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check if tables exist
        existing_tables = inspector.get_table_names()
        print(f"✅ Existing tables: {', '.join(existing_tables)}\n")
        
        # Expected models and their required columns
        expected_schema = {
            'team_member': [
                'id', 'name', 'role', 'department', 'bio', 'image_filename',
                'email', 'show_email', 'linkedin_url', 'twitter_url',
                'facebook_url', 'tiktok_url', 'other_url', 'created_at', 'updated_at'
            ],
            'alert': [
                'id', 'title', 'message', 'media_type', 'media_filename',
                'created_at', 'is_active'
            ],
            'program': [
                'id', 'title', 'description', 'category', 'event_date', 'location',
                'media_type', 'media_filename', 'created_at', 'updated_at'
            ],
            'admin': [
                'id', 'username', 'email', 'password_hash', 'created_at', 'is_active'
            ],
            'uploaded_file': [
                'id', 'filename', 'original_filename', 'file_path', 'file_size',
                'file_type', 'uploaded_by', 'uploaded_at'
            ],
            'contact_message': [
                'id', 'name', 'email', 'subject', 'message', 'submitted_at',
                'ip_address', 'read'
            ]
        }
        
        print("📋 SCHEMA VERIFICATION:\n")
        
        all_good = True
        for table_name, required_columns in expected_schema.items():
            if table_name in existing_tables:
                actual_columns = [col['name'] for col in inspector.get_columns(table_name)]
                print(f"✅ Table '{table_name}' exists")
                
                missing_columns = set(required_columns) - set(actual_columns)
                if missing_columns:
                    print(f"   ⚠️  WARNING: Missing columns: {', '.join(missing_columns)}")
                    all_good = False
                else:
                    print(f"   ✅ All required columns present ({len(actual_columns)} columns)")
                
                extra_columns = set(actual_columns) - set(required_columns)
                if extra_columns:
                    print(f"   ℹ️  Extra columns (safe): {', '.join(extra_columns)}")
                
                print()
            else:
                print(f"❌ Table '{table_name}' NOT FOUND")
                all_good = False
                print()
        
        print("="*60)
        if all_good:
            print("✅ DATABASE SCHEMA VERIFICATION PASSED")
            print("="*60 + "\n")
            return True
        else:
            print("⚠️  DATABASE SCHEMA HAS ISSUES (See above)")
            print("="*60 + "\n")
            return False


def check_data_integrity():
    """Check data in tables"""
    print("📊 DATA INTEGRITY CHECK:\n")
    
    with app.app_context():
        from app import TeamMember, Alert, Program, Admin, ContactMessage
        
        team_count = TeamMember.query.count()
        alert_count = Alert.query.count()
        program_count = Program.query.count()
        admin_count = Admin.query.count()
        message_count = ContactMessage.query.count()
        
        print(f"👥 Team Members: {team_count} records")
        print(f"🔔 Alerts: {alert_count} records")
        print(f"📅 Programs: {program_count} records")
        print(f"🔐 Admins: {admin_count} records")
        print(f"💬 Contact Messages: {message_count} records")
        print()


if __name__ == '__main__':
    try:
        schema_ok = verify_database()
        check_data_integrity()
        
        if schema_ok:
            print("✅ DATABASE IS READY FOR USE")
            sys.exit(0)
        else:
            print("❌ DATABASE HAS ISSUES - Please check schema")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR during verification: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
