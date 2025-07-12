from app import db
from models import User, Skill, UserSkill, SwapRequest, Rating
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data if tables are empty"""
    
    # Check if data already exists
    if User.query.count() > 0:
        return
    
    print("Creating sample data...")
    
    # Create admin user
    admin = User(username='admin', name='Jigyasu Patel', is_admin=True, is_public=True)
    admin.set_password('admin123')
    admin.location = 'India'
    admin.availability = 'Weekends'
    db.session.add(admin)
    
    # Create sample skills
    skills_data = [
        {'name': 'JavaScript', 'category': 'Programming'},
        {'name': 'Python', 'category': 'Programming'},
        {'name': 'Java', 'category': 'Programming'},
        {'name': 'React', 'category': 'Programming'},
        {'name': 'Node.js', 'category': 'Programming'},
        {'name': 'Photoshop', 'category': 'Design'},
        {'name': 'Graphic Design', 'category': 'Design'},
        {'name': 'UI/UX Design', 'category': 'Design'},
        {'name': 'Web Design', 'category': 'Design'},
        {'name': 'Logo Design', 'category': 'Design'},
        {'name': 'Photography', 'category': 'Creative'},
        {'name': 'Video Editing', 'category': 'Creative'},
        {'name': 'Content Writing', 'category': 'Writing'},
        {'name': 'Copywriting', 'category': 'Writing'},
        {'name': 'Data Analysis', 'category': 'Analytics'},
        {'name': 'Excel', 'category': 'Analytics'},
        {'name': 'Digital Marketing', 'category': 'Marketing'},
        {'name': 'SEO', 'category': 'Marketing'},
        {'name': 'Social Media Marketing', 'category': 'Marketing'},
        {'name': 'English Teaching', 'category': 'Education'},
        {'name': 'Guitar', 'category': 'Music'},
        {'name': 'Piano', 'category': 'Music'},
        {'name': 'Cooking', 'category': 'Lifestyle'},
        {'name': 'Fitness Training', 'category': 'Health'},
        {'name': 'Yoga', 'category': 'Health'}
    ]
    
    skills = []
    for skill_data in skills_data:
        skill = Skill(name=skill_data['name'], category=skill_data['category'])
        skills.append(skill)
        db.session.add(skill)
    
    db.session.flush()  # Get skill IDs
    
    # Create sample users
    users_data = [
        {
            'username': 'marc_demo',
            'password': 'password123',
            'name': 'Marc Demo',
            'location': 'New York, USA',
            'availability': 'Weekends',
            'offered_skills': ['JavaScript', 'Python'],
            'wanted_skills': ['Photoshop', 'Graphic Design']
        },
        {
            'username': 'michell',
            'password': 'password123',
            'name': 'Michell',
            'location': 'London, UK',
            'availability': 'Evenings',
            'offered_skills': ['Java', 'React'],
            'wanted_skills': ['Photography', 'Video Editing']
        },
        {
            'username': 'joe_wills',
            'password': 'password123',
            'name': 'Joe Wills',
            'location': 'Toronto, Canada',
            'availability': 'Weekdays',
            'offered_skills': ['Node.js', 'Web Design'],
            'wanted_skills': ['Digital Marketing', 'SEO']
        },
        {
            'username': 'alice_johnson',
            'password': 'password123',
            'name': 'Alice Johnson',
            'location': 'Sydney, Australia',
            'availability': 'Weekends, Evenings',
            'offered_skills': ['UI/UX Design', 'Photoshop'],
            'wanted_skills': ['Data Analysis', 'Excel']
        },
        {
            'username': 'bob_smith',
            'password': 'password123',
            'name': 'Bob Smith',
            'location': 'Berlin, Germany',
            'availability': 'Weekends',
            'offered_skills': ['Photography', 'Video Editing'],
            'wanted_skills': ['Digital Marketing', 'Content Writing']
        },
        {
            'username': 'sarah_wilson',
            'password': 'password123',
            'name': 'Sarah Wilson',
            'location': 'Paris, France',
            'availability': 'Evenings',
            'offered_skills': ['Graphic Design', 'Logo Design'],
            'wanted_skills': ['Python', 'JavaScript']
        },
        {
            'username': 'david_chen',
            'password': 'password123',
            'name': 'David Chen',
            'location': 'Singapore',
            'availability': 'Weekdays, Weekends',
            'offered_skills': ['Data Analysis', 'Excel'],
            'wanted_skills': ['Guitar', 'Piano']
        },
        {
            'username': 'emma_garcia',
            'password': 'password123',
            'name': 'Emma Garcia',
            'location': 'Barcelona, Spain',
            'availability': 'Weekends',
            'offered_skills': ['Digital Marketing', 'SEO'],
            'wanted_skills': ['Cooking', 'Yoga']
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user = User(
            username=user_data['username'],
            name=user_data['name'],
            location=user_data['location'],
            availability=user_data['availability'],
            is_public=True
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.flush()
        
        # Add skills for user
        for skill_name in user_data['offered_skills']:
            skill = next((s for s in skills if s.name == skill_name), None)
            if skill:
                user_skill = UserSkill(user_id=user.id, skill_id=skill.id, skill_type='offered')
                db.session.add(user_skill)
        
        for skill_name in user_data['wanted_skills']:
            skill = next((s for s in skills if s.name == skill_name), None)
            if skill:
                user_skill = UserSkill(user_id=user.id, skill_id=skill.id, skill_type='wanted')
                db.session.add(user_skill)
        
        created_users.append(user)
    
    db.session.flush()
    
    # Create sample swap requests
    swap_requests_data = [
        {
            'requester': 'marc_demo',
            'receiver': 'alice_johnson',
            'offered_skill': 'JavaScript',
            'wanted_skill': 'Photoshop',
            'status': 'pending',
            'message': 'Hi! I would love to learn Photoshop in exchange for JavaScript tutoring.'
        },
        {
            'requester': 'michell',
            'receiver': 'bob_smith',
            'offered_skill': 'React',
            'wanted_skill': 'Photography',
            'status': 'accepted',
            'message': 'I can teach you React if you can help me with photography basics.'
        },
        {
            'requester': 'joe_wills',
            'receiver': 'emma_garcia',
            'offered_skill': 'Web Design',
            'wanted_skill': 'Digital Marketing',
            'status': 'completed',
            'message': 'Looking to learn digital marketing strategies. Can offer web design skills.'
        },
        {
            'requester': 'david_chen',
            'receiver': 'marc_demo',
            'offered_skill': 'Data Analysis',
            'wanted_skill': 'Python',
            'status': 'rejected',
            'message': 'Would like to learn Python programming. I can teach data analysis.'
        },
        {
            'requester': 'sarah_wilson',
            'receiver': 'michell',
            'offered_skill': 'Graphic Design',
            'wanted_skill': 'Java',
            'status': 'pending',
            'message': 'Interested in learning Java. I can help with graphic design projects.'
        }
    ]
    
    for req_data in swap_requests_data:
        requester = next((u for u in created_users if u.username == req_data['requester']), None)
        receiver = next((u for u in created_users if u.username == req_data['receiver']), None)
        offered_skill = next((s for s in skills if s.name == req_data['offered_skill']), None)
        wanted_skill = next((s for s in skills if s.name == req_data['wanted_skill']), None)
        
        if requester and receiver and offered_skill and wanted_skill:
            swap_request = SwapRequest(
                requester_id=requester.id,
                receiver_id=receiver.id,
                offered_skill_id=offered_skill.id,
                wanted_skill_id=wanted_skill.id,
                message=req_data['message'],
                status=req_data['status'],
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(swap_request)
    
    db.session.flush()
    
    # Create sample ratings for completed swaps
    completed_swaps = SwapRequest.query.filter_by(status='completed').all()
    for swap in completed_swaps:
        # Rating from requester to receiver
        rating1 = Rating(
            swap_request_id=swap.id,
            rater_id=swap.requester_id,
            rated_id=swap.receiver_id,
            rating=random.randint(4, 5),
            feedback='Great experience! Very knowledgeable and patient teacher.',
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 20))
        )
        db.session.add(rating1)
        
        # Rating from receiver to requester
        rating2 = Rating(
            swap_request_id=swap.id,
            rater_id=swap.receiver_id,
            rated_id=swap.requester_id,
            rating=random.randint(4, 5),
            feedback='Excellent skill swap partner. Highly recommended!',
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 20))
        )
        db.session.add(rating2)
    
    try:
        db.session.commit()
        print("Sample data created successfully!")
        print("\nSample users created:")
        print("- admin (password: admin123) - Admin user")
        for user_data in users_data:
            print(f"- {user_data['username']} (password: {user_data['password']}) - {user_data['name']}")
        
        print("\nSample skills include:")
        print("- Programming: JavaScript, Python, Java, React, Node.js")
        print("- Design: Photoshop, Graphic Design, UI/UX Design, Web Design")
        print("- Creative: Photography, Video Editing")
        print("- Marketing: Digital Marketing, SEO, Social Media Marketing")
        print("- Analytics: Data Analysis, Excel")
        print("- And many more...")
        
        print("\nSample swap requests with different statuses have been created.")
        print("Sample ratings and feedback have been added for completed swaps.")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")
