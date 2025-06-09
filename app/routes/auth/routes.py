from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from app.forms import LoginForm
from app.decorators import admin_required
from app.routes.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web_reports.dashboard'))
            
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Update last seen timestamp
            user.last_seen = db.func.now()
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('web_reports.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('web_auth.login'))

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('auth/users.html', users=users)
