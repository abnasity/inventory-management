from flask import Flask
from app import db, create_app
from app.models import User
import sys

def create_admin_user(username, email, password):
    """Create a new admin user or update existing user to admin role"""
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            # Update existing user to admin role
            user.role = 'admin'
            user.email = email
            user.set_password(password)
            db.session.commit()
            print(f"User '{username}' has been updated to admin role.")
        else:
            # Create new admin user
            user = User(
                username=username,
                email=email,
                role='admin'
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Admin user '{username}' has been created successfully.")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python create_admin.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_admin_user(username, email, password)
