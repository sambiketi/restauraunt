from app import create_app
from models import User
from db_postgres import db
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt()

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print('✅ Admin user already exists!')
        print(f'   Username: {admin.username}')
        print(f'   Email: {admin.email}')
    else:
        # Create admin user
        hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            username='admin',
            email='admin@bellavita.com',
            password_hash=hashed,
            is_admin=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin user created successfully!')
        print('   Username: admin')
        print('   Password: admin123')
