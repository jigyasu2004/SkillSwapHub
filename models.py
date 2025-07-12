from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    profile_photo = db.Column(db.String(200), nullable=True)
    availability = db.Column(db.String(200), nullable=True)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_banned = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills_offered = db.relationship('UserSkill', foreign_keys='UserSkill.user_id', 
                                   primaryjoin='and_(User.id==UserSkill.user_id, UserSkill.skill_type=="offered")',
                                   backref='offering_user', lazy='dynamic')
    skills_wanted = db.relationship('UserSkill', foreign_keys='UserSkill.user_id',
                                  primaryjoin='and_(User.id==UserSkill.user_id, UserSkill.skill_type=="wanted")',
                                  backref='wanting_user', lazy='dynamic')
    sent_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.requester_id',
                                  backref='requester', lazy='dynamic')
    received_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.receiver_id',
                                      backref='receiver', lazy='dynamic')
    given_ratings = db.relationship('Rating', foreign_keys='Rating.rater_id',
                                  backref='rater', lazy='dynamic')
    received_ratings = db.relationship('Rating', foreign_keys='Rating.rated_id',
                                     backref='rated_user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_average_rating(self):
        ratings = self.received_ratings.all()
        if not ratings:
            return 0.0
        return sum(r.rating for r in ratings) / len(ratings)
    
    def get_offered_skills_list(self):
        return [us.skill.name for us in self.skills_offered.all()]
    
    def get_wanted_skills_list(self):
        return [us.skill.name for us in self.skills_wanted.all()]

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    is_approved = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_skills = db.relationship('UserSkill', backref='skill', lazy='dynamic')

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    skill_type = db.Column(db.String(20), nullable=False)  # 'offered' or 'wanted'
    proficiency_level = db.Column(db.String(20), nullable=True)  # 'beginner', 'intermediate', 'advanced'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'skill_id', 'skill_type'),)

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offered_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    wanted_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'accepted', 'rejected', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    offered_skill = db.relationship('Skill', foreign_keys=[offered_skill_id])
    wanted_skill = db.relationship('Skill', foreign_keys=[wanted_skill_id])

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swap_request_id = db.Column(db.Integer, db.ForeignKey('swap_request.id'), nullable=False)
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rated_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    swap_request = db.relationship('SwapRequest', backref='ratings')

class AdminMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    creator = db.relationship('User', backref='admin_messages')
