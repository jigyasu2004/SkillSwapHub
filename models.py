from app import db, cache
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index, func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=True, index=True)
    location = db.Column(db.String(100), nullable=True, index=True)
    profile_photo = db.Column(db.String(200), nullable=True)
    availability = db.Column(db.String(200), nullable=True, index=True)
    is_public = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False, index=True)
    is_banned = db.Column(db.Boolean, default=False, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships with optimized lazy loading
    skills_offered = db.relationship('UserSkill', foreign_keys='UserSkill.user_id', 
                                   primaryjoin='and_(User.id==UserSkill.user_id, UserSkill.skill_type=="offered")',
                                   backref='offering_user', lazy='select')
    skills_wanted = db.relationship('UserSkill', foreign_keys='UserSkill.user_id',
                                  primaryjoin='and_(User.id==UserSkill.user_id, UserSkill.skill_type=="wanted")',
                                  backref='wanting_user', lazy='select')
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
    
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get_average_rating(self):
        avg_rating = db.session.query(func.avg(Rating.rating)).filter_by(rated_id=self.id).scalar()
        return float(avg_rating) if avg_rating else 0.0
    
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get_offered_skills_list(self):
        return [us.skill.name for us in self.skills_offered]
    
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get_wanted_skills_list(self):
        return [us.skill.name for us in self.skills_wanted]
    
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get_rating_count(self):
        return self.received_ratings.count()

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=True, index=True)
    is_approved = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_skills = db.relationship('UserSkill', backref='skill', lazy='dynamic')

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False, index=True)
    skill_type = db.Column(db.String(20), nullable=False, index=True)  # 'offered' or 'wanted'
    proficiency_level = db.Column(db.String(20), nullable=True)  # 'beginner', 'intermediate', 'advanced'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_user_skill_type', 'user_id', 'skill_type'),
        Index('idx_skill_type', 'skill_id', 'skill_type'),
    )

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    offered_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False, index=True)
    wanted_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with eager loading
    offered_skill = db.relationship('Skill', foreign_keys=[offered_skill_id], lazy='joined')
    wanted_skill = db.relationship('Skill', foreign_keys=[wanted_skill_id], lazy='joined')
    requester = db.relationship('User', foreign_keys=[requester_id], lazy='joined')
    receiver = db.relationship('User', foreign_keys=[receiver_id], lazy='joined')
    
    # Composite indexes for efficient queries
    __table_args__ = (
        Index('idx_requester_status', 'requester_id', 'status'),
        Index('idx_receiver_status', 'receiver_id', 'status'),
        Index('idx_status_created', 'status', 'created_at'),
    )

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swap_request_id = db.Column(db.Integer, db.ForeignKey('swap_request.id'), nullable=False, index=True)
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    rated_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False, index=True)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    swap_request = db.relationship('SwapRequest', backref='ratings', lazy='joined')
    rater = db.relationship('User', foreign_keys=[rater_id], lazy='joined')
    rated_user = db.relationship('User', foreign_keys=[rated_id], lazy='joined')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swap_request_id = db.Column(db.Integer, db.ForeignKey('swap_request.id'), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    swap_request = db.relationship('SwapRequest', backref='messages')
    sender = db.relationship('User', foreign_keys=[sender_id], lazy='joined')
    receiver = db.relationship('User', foreign_keys=[receiver_id], lazy='joined')
    
    # Composite indexes for efficient queries
    __table_args__ = (
        Index('idx_swap_request_created', 'swap_request_id', 'created_at'),
        Index('idx_receiver_read', 'receiver_id', 'is_read'),
    )

class AdminMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_broadcast = db.Column(db.Boolean, default=False, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    admin = db.relationship('User', foreign_keys=[admin_id], lazy='joined')
    recipient = db.relationship('User', foreign_keys=[recipient_id], lazy='joined')
