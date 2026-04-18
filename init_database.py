#!/usr/bin/env python3
"""
Safe Database Initialization Script for EcoHub
Creates tables WITHOUT dropping existing data
SAFE: Only creates missing tables, never deletes or modifies existing tables
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

def init_database():
    """
    Initialize database safely:
    1. Check existing tables
    2. Create only missing tables
    3. Preserve all existing data
    """
    
    print("\n" + "="*70)
    print("🗄️  SAFE DATABASE INITIALIZATION FOR ECOHUB")
    print("="*70 + "\n")
    
    with app.app_context():
        try:
            print("📋 Step 1: Checking existing database state...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = set(inspector.get_table_names())
            
            print(f"✅ Found {len(existing_tables)} existing tables")
            if existing_tables:
                print(f"   Tables: {', '.join(sorted(existing_tables))}\n")
            
            print("📋 Step 2: Running create_all() to create missing tables only...")
            print("   ⚠️  This will NOT drop any existing tables or data\n")
            
            # This is safe - SQLAlchemy's create_all only creates missing tables
            db.create_all()
            
            print("✅ create_all() completed successfully")
            
            print("\n📋 Step 3: Verifying all tables exist...")
            inspector = inspect(db.engine)
            new_tables = set(inspector.get_table_names())
            
            if new_tables:
                print(f"✅ Verified {len(new_tables)} tables in database:")
                for table in sorted(new_tables):
                    columns = [col['name'] for col in inspector.get_columns(table)]
                    print(f"   ✓ {table:<25} ({len(columns)} columns)")
            
            print("\n" + "="*70)
            print("✅ DATABASE INITIALIZATION COMPLETED SUCCESSFULLY")
            print("="*70)
            print("\nℹ️  All existing data has been preserved.")
            print("ℹ️  New tables have been created as needed.")
            print("ℹ️  Database is ready for use!\n")
            
            return True
            
        except Exception as e:
            print("\n❌ ERROR DURING DATABASE INITIALIZATION")
            print(f"Error: {str(e)}\n")
            logger.error(f"Database initialization failed: {str(e)}", exc_info=True)
            return False


def backup_database_info():
    """Log database information for backup purposes"""
    print("📊 DATABASE BACKUP INFORMATION:\n")
    
    with app.app_context():
        from app import TeamMember, Alert, Program, Admin, ContactMessage, UploadedFile
        
        # Count records in each table
        data_summary = {
            'Team Members': TeamMember.query.count(),
            'Alerts': Alert.query.count(),
            'Programs': Program.query.count(),
            'Admins': Admin.query.count(),
            'Contact Messages': ContactMessage.query.count(),
            'Uploaded Files': UploadedFile.query.count(),
        }
        
        total_records = sum(data_summary.values())
        
        for name, count in data_summary.items():
            print(f"   {name:<25} : {count:>5} records")
        
        print(f"\n   {'Total':<25} : {total_records:>5} records")
        print()
        
        logger.info(f"Database contains {total_records} total records")
        return data_summary


if __name__ == '__main__':
    try:
        # Initialize database
        success = init_database()
        
        if success:
            # Show data summary
            backup_database_info()
            
            print("✅ Ready to run: python app.py")
            sys.exit(0)
        else:
            print("❌ Database initialization failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
