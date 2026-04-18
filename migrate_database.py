#!/usr/bin/env python3
"""
Safe Database Migration for Alert Table
Adds new columns to existing alert table without losing data
COMPLETELY SAFE: Only adds columns, never deletes or modifies existing data
"""

import sys
import logging
from app import app, db

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def migrate_alert_table():
    """
    Add media_type and media_filename columns to alert table
    SAFE: Uses raw SQL ALTER TABLE to add columns if they don't exist
    """
    
    print("\n" + "="*70)
    print("🔄 SAFE MIGRATION: Adding Media Support to Alert Table")
    print("="*70 + "\n")
    
    with app.app_context():
        try:
            connection = db.engine.connect()
            
            # Get current columns
            print("📋 Step 1: Checking existing columns in alert table...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('alert')]
            print(f"✅ Current columns: {', '.join(existing_columns)}\n")
            
            # Check if columns already exist
            needs_migration = False
            missing_columns = []
            
            if 'media_type' not in existing_columns:
                missing_columns.append('media_type')
                needs_migration = True
            if 'media_filename' not in existing_columns:
                missing_columns.append('media_filename')
                needs_migration = True
            
            if not needs_migration:
                print("✅ Alert table already has media_type and media_filename columns")
                print("   No migration needed!\n")
                return True
            
            print(f"📋 Step 2: Adding missing columns: {', '.join(missing_columns)}\n")
            
            # Add columns using raw SQL (safer than SQLAlchemy for this operation)
            if 'media_type' in missing_columns:
                print("   Adding media_type column...")
                try:
                    sql_media_type = "ALTER TABLE alert ADD COLUMN media_type VARCHAR(50) DEFAULT 'text'"
                    connection.execute(db.text(sql_media_type))
                    print("   ✅ media_type column added successfully")
                except Exception as e:
                    if 'duplicate column' in str(e).lower():
                        print("   ℹ️  media_type column already exists (skipped)")
                    else:
                        raise
            
            if 'media_filename' in missing_columns:
                print("   Adding media_filename column...")
                try:
                    sql_media_filename = "ALTER TABLE alert ADD COLUMN media_filename VARCHAR(255)"
                    connection.execute(db.text(sql_media_filename))
                    print("   ✅ media_filename column added successfully")
                except Exception as e:
                    if 'duplicate column' in str(e).lower():
                        print("   ℹ️  media_filename column already exists (skipped)")
                    else:
                        raise
            
            connection.commit()
            connection.close()
            
            print("\n📋 Step 3: Verifying migration...")
            new_columns = [col['name'] for col in inspector.get_columns('alert')]
            print(f"✅ New columns: {', '.join(new_columns)}\n")
            
            # Check if is_active column exists and update default values if needed
            if 'is_active' in new_columns:
                print("📋 Step 4: Checking is_active default values...")
                # This is just for info, we don't modify existing data
                print("   ✅ is_active column exists\n")
            
            print("="*70)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY")
            print("="*70)
            print("\n✅ Alert table now supports media content (text, image, video)")
            print("✅ All existing alert data has been preserved\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ MIGRATION ERROR: {str(e)}")
            logger.error(f"Migration failed: {str(e)}", exc_info=True)
            try:
                connection.rollback()
            except:
                pass
            return False


def verify_migrations():
    """Verify all migrations are applied"""
    print("📊 VERIFYING DATABASE SCHEMA AFTER MIGRATION:\n")
    
    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        # Check alert table
        alert_columns = [col['name'] for col in inspector.get_columns('alert')]
        print("Alert table columns:")
        for col in sorted(alert_columns):
            print(f"   ✓ {col}")
        
        # Check program table
        if 'program' in inspector.get_table_names():
            program_columns = [col['name'] for col in inspector.get_columns('program')]
            print("\nProgram table columns:")
            for col in sorted(program_columns):
                print(f"   ✓ {col}")
        
        print()


if __name__ == '__main__':
    try:
        success = migrate_alert_table()
        
        if success:
            verify_migrations()
            print("✅ Database ready! You can now run: python app.py")
            sys.exit(0)
        else:
            print("❌ Migration failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
