import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    app = create_app()
    with app.app_context():
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'adminpass123')

        existing_admin = User.query.filter_by(username=admin_username).first()

        if existing_admin:
            print("Admin user already exists.")
        else:
            new_admin = User(
                username=admin_username,
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully.")

if __name__ == "__main__":
    create_admin()
