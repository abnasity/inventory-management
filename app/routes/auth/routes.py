from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from app.forms import LoginForm, ProfileForm, RegisterForm
from app.decorators import admin_required
from app.routes.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('reports.dashboard'))
            
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data,
            email=form.email.data
        ).first()
        
        if user and user.check_password(form.password.data):
            # Update last seen timestamp
            user.last_seen = db.func.now()
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('reports.dashboard'))
        else:
            flash('Invalid login credentials. Please check your username, email, and password.', 'danger')
            
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    form = RegisterForm()  # Form for the add user modal
    return render_template('auth/users.html', users=users, form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(current_user.username, current_user.email)
    
    if form.validate_on_submit():
        if form.current_password.data and not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return render_template('auth/profile.html', form=form)
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        if form.new_password.data:
            if form.new_password.data != form.confirm_password.data:
                flash('New passwords do not match', 'danger')
                return render_template('auth/profile.html', form=form)
            current_user.set_password(form.new_password.data)
        
        db.session.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('auth.profile'))
    
    # Pre-populate form with current data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('auth/profile.html', form=form)

@bp.route('/users/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    
    if not all([username, email, password, role]) or role not in ['admin', 'staff']:
        flash('Please fill in all required fields correctly', 'danger')
        return redirect(url_for('auth.users'))
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'danger')
        return redirect(url_for('auth.users'))
    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'danger')
        return redirect(url_for('auth.users'))
    
    # Create new user
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    
    try:
        db.session.commit()
        flash(f'User {username} has been created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error creating user', 'danger')
    
    return redirect(url_for('auth.users'))

@bp.route('/users/<int:user_id>/toggle_status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deactivation
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot modify your own status'})
    
    user.is_active = not user.is_active
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'User {user.username} has been {"activated" if user.is_active else "deactivated"}'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Database error occurred'})

@bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def get_user(user_id):
    """Get user data for editing"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })

@bp.route('/users/<int:user_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Handle user edit form submission"""
    user = User.query.get_or_404(user_id)
    
    # Check if it's an attempt to modify the current admin's role
    if user.id == current_user.id and user.role == 'admin' and request.form.get('role') != 'admin':
        flash('Cannot remove admin role from yourself', 'danger')
        return redirect(url_for('auth.users'))
    
    # Update user data
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    new_password = request.form.get('password')
    
    # Validate required fields
    if not all([username, email, role]) or role not in ['admin', 'staff']:
        flash('Please fill in all required fields correctly', 'danger')
        return redirect(url_for('auth.users'))
    
    # Check if username/email are taken by other users
    username_exists = User.query.filter(User.username == username, User.id != user_id).first()
    email_exists = User.query.filter(User.email == email, User.id != user_id).first()
    
    if username_exists:
        flash('Username already exists', 'danger')
        return redirect(url_for('auth.users'))
    if email_exists:
        flash('Email already registered', 'danger')
        return redirect(url_for('auth.users'))
    
    # Update user
    user.username = username
    user.email = email
    user.role = role
    if new_password:
        user.set_password(new_password)
    
    try:
        db.session.commit()
        flash('User updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating user: ' + str(e), 'danger')
    
    return redirect(url_for('auth.users'))
