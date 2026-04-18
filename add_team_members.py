"""
Script to add initial team members to the database
"""

from app import app, db, TeamMember
from datetime import datetime

# Team members data
team_data = [
    {
        'name': 'Godfred Arhin',
        'role': 'Founder',
        'department': 'Leadership',
        'image_filename': 'Godfred Arhin.jpg',
        'bio': 'Founder and visionary leader of INNOVORA EcoHub Group',
    },
    {
        'name': 'Mamiella Asmah',
        'role': 'Faculty Advisor',
        'department': 'Advisory',
        'image_filename': 'Mamiella Asmah.jpg',
        'bio': 'Faculty advisor providing strategic guidance and mentorship',
    },
    {
        'name': 'Micheal Dordzavu',
        'role': 'Programs Lead',
        'department': 'Programs & Operations',
        'image_filename': 'Micheal Dordzavu.jpg',
        'bio': 'Leading program development and execution',
    },
    {
        'name': 'Samuel Nyamekye',
        'role': 'Head of IT',
        'department': 'Technology',
        'image_filename': 'Samuel Nyamekye.jpeg',
        'bio': 'Managing technology infrastructure and digital innovation',
    },
]

def add_team_members():
    """Add team members to the database"""
    try:
        with app.app_context():
            # Check if team members already exist
            existing_count = TeamMember.query.count()
            if existing_count > 0:
                print(f'ℹ️  Database already has {existing_count} team members')
                response = input('Do you want to add more? (y/n): ').strip().lower()
                if response != 'y':
                    print('✓ Skipping team member addition')
                    return
            
            # Add each team member
            added_count = 0
            for member_data in team_data:
                # Check if member already exists
                existing = TeamMember.query.filter_by(name=member_data['name']).first()
                if existing:
                    print(f'⚠️  {member_data["name"]} already exists in database')
                    continue
                
                # Create new team member
                member = TeamMember(
                    name=member_data['name'],
                    role=member_data['role'],
                    department=member_data['department'],
                    image_filename=member_data['image_filename'],
                    bio=member_data['bio'],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.session.add(member)
                added_count += 1
                print(f'✓ Added: {member_data["name"]} ({member_data["role"]})')
            
            if added_count > 0:
                db.session.commit()
                print(f'\n✅ Successfully added {added_count} team members to the database!')
                print('\nℹ️  You can now edit their details (email, social media, bio) via the admin page:')
                print('   - Go to Admin > Team Management')
                print('   - Click the Edit button on each team member card')
                print('   - Add their email, LinkedIn, Twitter, Facebook, etc.')
            else:
                print('ℹ️  No new team members were added (all already exist)')
    
    except Exception as e:
        print(f'❌ Error adding team members: {str(e)}')
        db.session.rollback()
        raise

if __name__ == '__main__':
    print('=' * 60)
    print('INNOVORA EcoHub - Add Team Members')
    print('=' * 60)
    add_team_members()
