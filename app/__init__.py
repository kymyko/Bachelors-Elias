from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kymyko:mara@localhost/mentalhealth'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['WTF_CSRF_ENABLED'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'

    with app.app_context():
        from app.models import Users, Psychologists, Appointments
        from app.routes import articles, auth, chatbot, users, main
        from app.routes.appointments import bp as appointments_bp

        app.register_blueprint(main.bp)
        app.register_blueprint(articles.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(chatbot.bp, url_prefix='/chatbot')
        app.register_blueprint(users.bp)
        app.register_blueprint(appointments_bp, url_prefix='/appointments')

        @login_manager.user_loader
        def load_user(user_id):
            return Users.query.get(int(user_id))

        db.create_all()

    return app
