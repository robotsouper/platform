from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes import auth_routes, post_routes, comment_routes, like_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(post_routes.bp)
    app.register_blueprint(comment_routes.bp)
    app.register_blueprint(like_routes.bp)

    # @app.route('/')
    # def index():
    #     return "API is running!"

    return app
