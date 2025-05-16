from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'temp'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../workouts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)
    
    from .auth import auth
    app.register_blueprint(auth)

    # Context processor to make `user` available globally in templates
    @app.context_processor
    def inject_user():
        from flask import session
        from .models import User  # import here to avoid circular import issues
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return dict(user=user)

    return app
