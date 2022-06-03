from dataclasses_jsonschema import SchemaType
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS

from config import Config


db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
cors: CORS = CORS(supports_credentials=True)
api: Api = Api(
    title="My Note Api",
    version="1.0",
    description="Simple Backend app For testing Crud and User auth",
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    blueprint = Blueprint("api", __name__)
    api.init_app(blueprint)
    app.register_blueprint(blueprint, url_prefix="/api/v1")

    @api.errorhandler
    @api.errorhandler(TypeError)
    def default_error_handler(error):
        """Default error handler"""
        return {"message": str(error), "status": Config.ERROR_STATUS}, getattr(
            error, "code", 500
        )

    return app


from app.routes import *
from app.model import *
