"""
Safe data migration from SQLite to PostgreSQL (Supabase)
Reads all records from SQLite and inserts into PostgreSQL
Preserves all existing data without loss
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

# ============================================
# DATABASE CONNECTIONS
# ============================================

BASE_DIR = Path(__file__).resolve().parent

# SQLite source database
sqlite_path = f'sqlite:///{BASE_DIR}/ecohub.db'
sqlite_engine = create_engine(sqlite_path)

# PostgreSQL target database
postgres_url = os.getenv('DATABASE_URL')
if not postgres_url:
    print("ERROR: DATABASE_URL environment variable not set!")
    print("Please set DATABASE_URL to your Supabase PostgreSQL connection string")
    exit(1)

# Convert postgres:// to postgresql:// if needed
if postgres_url.startswith('postgres://'):
    postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)

postgres_engine = create_engine(
    postgres_url,
    connect_args={'sslmode': 'require'}
)

# ============================================
# DATA MIGRATION FUNCTIONS
# ============================================

def get_all_table_names(engine):
    """Get all table names from database"""
    inspector = text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    with engine.connect() as conn:
        result = conn.execute(inspector)
        return [row[0] for row in result]

def migrate_table_data(table_name, source_engine, target_engine):
    """Migrate all data from source table to target table"""
    try:
        # Create SQLAlchemy sessions
        SourceSession = sessionmaker(bind=source_engine)
        TargetSession = sessionmaker(bind=target_engine)
        
        source_session = SourceSession()
        target_session = TargetSession()
        
        # Get all records from source table
        query = text(f"SELECT * FROM {table_name}")
        with source_engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()
        
        if not rows:
            print(f"  ✓ {table_name}: No data to migrate")
            return 0
        
        # Get column names
        col_query = text(f"PRAGMA table_info({table_name})")
        with source_engine.connect() as conn:
            col_result = conn.execute(col_query)
            columns = [row[1] for row in col_result]
        
        # Insert data into target table
        migrated_count = 0
        for row in rows:
            insert_query = text(
                f"INSERT INTO {table_name} ({', '.join(columns)}) "
                f"VALUES ({', '.join([':' + str(i) for i in range(len(columns))])})"
            )
            
            row_dict = {str(i): row[i] for i in range(len(columns))}
            
            with target_engine.connect() as conn:
                conn.execute(insert_query, row_dict)
                conn.commit()
            
            migrated_count += 1
        
        print(f"  ✓ {table_name}: Migrated {migrated_count} records")
        return migrated_count
        
    except Exception as e:
        print(f"  ✗ {table_name}: Error - {str(e)}")
        return 0

def test_connections():
    """Test database connections"""
    print("\n" + "="*60)
    print("TESTING DATABASE CONNECTIONS")
    print("="*60)
    
    try:
        with sqlite_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ SQLite connection: OK")
    except Exception as e:
        print(f"✗ SQLite connection failed: {e}")
        return False
    
    try:
        with postgres_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ PostgreSQL connection: OK")
    except Exception as e:
        print(f"✗ PostgreSQL connection failed: {e}")
        return False
    
    return True

def migrate_all_data():
    """Migrate all data from SQLite to PostgreSQL"""
    print("\n" + "="*60)
    print("MIGRATING DATA: SQLite → PostgreSQL")
    print("="*60 + "\n")
    
    try:
        # Get table names from SQLite
        sqlite_tables = get_all_table_names(sqlite_engine)
        print(f"Found {len(sqlite_tables)} tables in SQLite\n")
        
        total_records = 0
        for table in sqlite_tables:
            migrated = migrate_table_data(table, sqlite_engine, postgres_engine)
            total_records += migrated
        
        print(f"\n" + "="*60)
        print(f"MIGRATION COMPLETE: {total_records} total records migrated")
        print("="*60)
        
    except Exception as e:
        print(f"\nMIGRATION FAILED: {e}")
        return False
    
    return True

def main():
    """Main migration workflow"""
    print("\n" + "="*60)
    print("EcoHub: SQLite → PostgreSQL (Supabase) Data Migration")
    print("="*60)
    
    # Test connections first
    if not test_connections():
        print("\nAborted: Database connection test failed")
        return False
    
    # Confirm before proceeding
    print("\n⚠️  WARNING: This will migrate all data from SQLite to PostgreSQL")
    print("   Ensure PostgreSQL tables already exist!")
    response = input("\nProceed with migration? (type 'yes' to continue): ")
    
    if response.lower() != 'yes':
        print("Migration cancelled")
        return False
    
    # Run migration
    return migrate_all_data()

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
