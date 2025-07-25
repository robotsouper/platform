from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes import auth_routes, post_routes, comment_routes, like_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(post_routes.bp)
    app.register_blueprint(comment_routes.bp)
    app.register_blueprint(like_routes.bp)

    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route("/login.html")
    def login_page():
        return render_template("login.html")
    
    return app
