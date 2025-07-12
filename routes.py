from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import User, Skill, UserSkill, SwapRequest, Rating, AdminMessage
from sqlalchemy import or_, and_
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Helper function to get current user
def get_current_user():
    if is_logged_in():
        return User.query.get(session['user_id'])
    return None

# Helper function to check if user is admin
def is_admin():
    user = get_current_user()
    return user and user.is_admin

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)
    availability_filter = request.args.get('availability', '', type=str)
    
    # Base query for public users who are not banned
    query = User.query.filter(User.is_public == True, User.is_banned == False)
    
    # Apply search filter
    if search_query:
        # Search in user skills
        skill_users = db.session.query(User.id).join(UserSkill).join(Skill).filter(
            Skill.name.ilike(f'%{search_query}%')
        ).subquery()
        
        query = query.filter(or_(
            User.name.ilike(f'%{search_query}%'),
            User.location.ilike(f'%{search_query}%'),
            User.id.in_(skill_users)
        ))
    
    # Apply availability filter
    if availability_filter:
        query = query.filter(User.availability.ilike(f'%{availability_filter}%'))
    
    # Paginate results
    per_page = 6
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Get unique availability options for filter
    availability_options = db.session.query(User.availability).filter(
        User.availability.isnot(None), User.is_public == True, User.is_banned == False
    ).distinct().all()
    availability_options = [opt[0] for opt in availability_options if opt[0]]
    
    return render_template('index.html', users=users, search_query=search_query,
                         availability_filter=availability_filter,
                         availability_options=availability_options)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.is_banned:
                flash('Your account has been banned. Please contact support.', 'error')
                return render_template('login.html')
            
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            session['user_id'] = user.id
            flash('Registration successful! Please complete your profile.', 'success')
            return redirect(url_for('edit_profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if not is_logged_in():
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))
    
    user = get_current_user()
    # Get user's recent ratings sorted by date
    recent_ratings = Rating.query.filter_by(rated_id=user.id).order_by(Rating.created_at.desc()).limit(5).all()
    
    return render_template('profile.html', user=user, recent_ratings=recent_ratings)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not is_logged_in():
        flash('Please log in to edit your profile.', 'error')
        return redirect(url_for('login'))
    
    user = get_current_user()
    
    if request.method == 'POST':
        # Update basic info
        user.name = request.form.get('name', '').strip()
        user.location = request.form.get('location', '').strip()
        user.availability = request.form.get('availability', '').strip()
        user.is_public = request.form.get('is_public') == 'on'
        
        # Handle skills
        offered_skills = request.form.getlist('offered_skills')
        wanted_skills = request.form.getlist('wanted_skills')
        
        # Remove existing skills
        UserSkill.query.filter_by(user_id=user.id).delete()
        
        # Add offered skills
        for skill_name in offered_skills:
            if skill_name.strip():
                skill = Skill.query.filter_by(name=skill_name.strip()).first()
                if not skill:
                    skill = Skill(name=skill_name.strip())
                    db.session.add(skill)
                    db.session.flush()
                
                user_skill = UserSkill(user_id=user.id, skill_id=skill.id, skill_type='offered')
                db.session.add(user_skill)
        
        # Add wanted skills
        for skill_name in wanted_skills:
            if skill_name.strip():
                skill = Skill.query.filter_by(name=skill_name.strip()).first()
                if not skill:
                    skill = Skill(name=skill_name.strip())
                    db.session.add(skill)
                    db.session.flush()
                
                user_skill = UserSkill(user_id=user.id, skill_id=skill.id, skill_type='wanted')
                db.session.add(user_skill)
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'error')
    
    # Get all skills for autocomplete
    all_skills = [skill.name for skill in Skill.query.all()]
    
    return render_template('edit_profile.html', user=user, all_skills=all_skills)

@app.route('/user/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check if profile is public or if viewing own profile
    current_user = get_current_user()
    if not user.is_public and (not current_user or current_user.id != user.id):
        flash('This profile is private.', 'error')
        return redirect(url_for('index'))
    
    if user.is_banned:
        flash('This user account has been banned.', 'error')
        return redirect(url_for('index'))
    
    # Get user's ratings sorted by date
    ratings = Rating.query.filter_by(rated_id=user.id).order_by(Rating.created_at.desc()).all()
    
    return render_template('user_detail.html', user=user, ratings=ratings)

@app.route('/send_request/<int:receiver_id>', methods=['GET', 'POST'])
def send_request(receiver_id):
    if not is_logged_in():
        flash('Please log in to send swap requests.', 'error')
        return redirect(url_for('login'))
    
    current_user = get_current_user()
    receiver = User.query.get_or_404(receiver_id)
    
    if current_user.id == receiver_id:
        flash('You cannot send a swap request to yourself.', 'error')
        return redirect(url_for('user_detail', user_id=receiver_id))
    
    if request.method == 'POST':
        offered_skill_id = request.form.get('offered_skill_id', type=int)
        wanted_skill_id = request.form.get('wanted_skill_id', type=int)
        message = request.form.get('message', '').strip()
        
        if not offered_skill_id or not wanted_skill_id:
            flash('Please select both skills for the swap.', 'error')
            return redirect(url_for('send_request', receiver_id=receiver_id))
        
        # Check if skills are valid
        offered_skill = Skill.query.get(offered_skill_id)
        wanted_skill = Skill.query.get(wanted_skill_id)
        
        if not offered_skill or not wanted_skill:
            flash('Invalid skill selection.', 'error')
            return redirect(url_for('send_request', receiver_id=receiver_id))
        
        # Check if user has the offered skill and receiver has the wanted skill
        user_has_offered = UserSkill.query.filter_by(
            user_id=current_user.id, skill_id=offered_skill_id, skill_type='offered'
        ).first()
        receiver_has_wanted = UserSkill.query.filter_by(
            user_id=receiver_id, skill_id=wanted_skill_id, skill_type='offered'
        ).first()
        
        if not user_has_offered:
            flash('You do not have the selected offered skill.', 'error')
            return redirect(url_for('send_request', receiver_id=receiver_id))
        
        if not receiver_has_wanted:
            flash('The user does not offer the selected skill.', 'error')
            return redirect(url_for('send_request', receiver_id=receiver_id))
        
        # Check for duplicate requests
        existing_request = SwapRequest.query.filter_by(
            requester_id=current_user.id,
            receiver_id=receiver_id,
            offered_skill_id=offered_skill_id,
            wanted_skill_id=wanted_skill_id,
            status='pending'
        ).first()
        
        if existing_request:
            flash('You already have a pending request for this skill swap.', 'error')
            return redirect(url_for('user_detail', user_id=receiver_id))
        
        # Create swap request
        swap_request = SwapRequest(
            requester_id=current_user.id,
            receiver_id=receiver_id,
            offered_skill_id=offered_skill_id,
            wanted_skill_id=wanted_skill_id,
            message=message
        )
        
        try:
            db.session.add(swap_request)
            db.session.commit()
            flash('Swap request sent successfully!', 'success')
            return redirect(url_for('user_detail', user_id=receiver_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while sending the request.', 'error')
    
    # Get skills for dropdowns
    user_offered_skills = db.session.query(Skill).join(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_type == 'offered'
    ).all()
    
    receiver_offered_skills = db.session.query(Skill).join(UserSkill).filter(
        UserSkill.user_id == receiver_id,
        UserSkill.skill_type == 'offered'
    ).all()
    
    return render_template('send_request.html', receiver=receiver,
                         user_offered_skills=user_offered_skills,
                         receiver_offered_skills=receiver_offered_skills)

@app.route('/swap_requests')
def swap_requests():
    if not is_logged_in():
        flash('Please log in to view swap requests.', 'error')
        return redirect(url_for('login'))
    
    current_user = get_current_user()
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '', type=str)
    
    # Get received requests
    received_query = SwapRequest.query.filter_by(receiver_id=current_user.id)
    if status_filter:
        received_query = received_query.filter_by(status=status_filter)
    
    received_requests = received_query.order_by(SwapRequest.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get sent requests
    sent_requests = SwapRequest.query.filter_by(requester_id=current_user.id).order_by(
        SwapRequest.created_at.desc()
    ).all()
    
    return render_template('swap_requests.html', received_requests=received_requests,
                         sent_requests=sent_requests, status_filter=status_filter)

@app.route('/handle_request/<int:request_id>/<action>')
def handle_request(request_id, action):
    if not is_logged_in():
        flash('Please log in to handle requests.', 'error')
        return redirect(url_for('login'))
    
    current_user = get_current_user()
    swap_request = SwapRequest.query.get_or_404(request_id)
    
    # Check if user is the receiver of this request
    if swap_request.receiver_id != current_user.id:
        flash('You are not authorized to handle this request.', 'error')
        return redirect(url_for('swap_requests'))
    
    if swap_request.status != 'pending':
        flash('This request has already been handled.', 'error')
        return redirect(url_for('swap_requests'))
    
    if action in ['accept', 'reject']:
        swap_request.status = 'accepted' if action == 'accept' else 'rejected'
        swap_request.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Request {action}ed successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while handling the request.', 'error')
    else:
        flash('Invalid action.', 'error')
    
    return redirect(url_for('swap_requests'))

@app.route('/delete_request/<int:request_id>')
def delete_request(request_id):
    if not is_logged_in():
        flash('Please log in to delete requests.', 'error')
        return redirect(url_for('login'))
    
    current_user = get_current_user()
    swap_request = SwapRequest.query.get_or_404(request_id)
    
    # Check if user is the requester
    if swap_request.requester_id != current_user.id:
        flash('You are not authorized to delete this request.', 'error')
        return redirect(url_for('swap_requests'))
    
    if swap_request.status == 'accepted':
        flash('You cannot delete an accepted request.', 'error')
        return redirect(url_for('swap_requests'))
    
    try:
        db.session.delete(swap_request)
        db.session.commit()
        flash('Request deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the request.', 'error')
    
    return redirect(url_for('swap_requests'))

@app.route('/rate_user/<int:swap_request_id>', methods=['GET', 'POST'])
def rate_user(swap_request_id):
    if not is_logged_in():
        flash('Please log in to rate users.', 'error')
        return redirect(url_for('login'))
    
    current_user = get_current_user()
    swap_request = SwapRequest.query.get_or_404(swap_request_id)
    
    # Check if user is part of this swap and if it's completed
    if current_user.id not in [swap_request.requester_id, swap_request.receiver_id]:
        flash('You are not authorized to rate this swap.', 'error')
        return redirect(url_for('swap_requests'))
    
    if swap_request.status != 'accepted':
        flash('You can only rate completed swaps.', 'error')
        return redirect(url_for('swap_requests'))
    
    # Determine who to rate
    rated_user_id = swap_request.receiver_id if current_user.id == swap_request.requester_id else swap_request.requester_id
    rated_user = User.query.get(rated_user_id)
    
    # Check if already rated
    existing_rating = Rating.query.filter_by(
        swap_request_id=swap_request_id,
        rater_id=current_user.id
    ).first()
    
    if request.method == 'POST':
        rating_value = request.form.get('rating', type=int)
        feedback = request.form.get('feedback', '').strip()
        
        if not rating_value or rating_value < 1 or rating_value > 5:
            flash('Please provide a valid rating (1-5 stars).', 'error')
            return render_template('rate_user.html', swap_request=swap_request,
                                 rated_user=rated_user, existing_rating=existing_rating)
        
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.feedback = feedback
        else:
            rating = Rating(
                swap_request_id=swap_request_id,
                rater_id=current_user.id,
                rated_id=rated_user_id,
                rating=rating_value,
                feedback=feedback
            )
            db.session.add(rating)
        
        try:
            db.session.commit()
            flash('Rating submitted successfully!', 'success')
            return redirect(url_for('swap_requests'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the rating.', 'error')
    
    return render_template('rate_user.html', swap_request=swap_request,
                         other_user=rated_user, existing_rating=existing_rating)

@app.route('/admin')
def admin_dashboard():
    if not is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Get statistics
    total_users = User.query.count()
    total_swaps = SwapRequest.query.count()
    pending_swaps = SwapRequest.query.filter_by(status='pending').count()
    banned_users = User.query.filter_by(is_banned=True).count()
    
    # Get recent activities
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_swaps = SwapRequest.query.order_by(SwapRequest.created_at.desc()).limit(10).all()
    recent_skills = Skill.query.filter_by(is_approved=False).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users, total_swaps=total_swaps,
                         pending_swaps=pending_swaps, banned_users=banned_users,
                         recent_users=recent_users, recent_swaps=recent_swaps,
                         recent_skills=recent_skills)

@app.route('/admin/ban_user/<int:user_id>')
def ban_user(user_id):
    if not is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cannot ban admin users.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    user.is_banned = not user.is_banned
    
    try:
        db.session.commit()
        action = 'banned' if user.is_banned else 'unbanned'
        flash(f'User {user.username} has been {action}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating user status.', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/approve_skill/<int:skill_id>')
def approve_skill(skill_id):
    if not is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    skill = Skill.query.get_or_404(skill_id)
    skill.is_approved = True
    
    try:
        db.session.commit()
        flash(f'Skill "{skill.name}" has been approved.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while approving the skill.', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_skill/<int:skill_id>')
def delete_skill(skill_id):
    if not is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    skill = Skill.query.get_or_404(skill_id)
    
    try:
        # Delete related user skills first
        UserSkill.query.filter_by(skill_id=skill_id).delete()
        db.session.delete(skill)
        db.session.commit()
        flash(f'Skill "{skill.name}" has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the skill.', 'error')
    
    return redirect(url_for('admin_dashboard'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Template context processors
@app.context_processor
def inject_user():
    return dict(current_user=get_current_user(), is_logged_in=is_logged_in(), is_admin=is_admin())
