import logging
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.models import db
from src.schemas import ma
from src.urls import initialize_routes
from src.utils.redis_connection import redis_connection


app = Flask(__name__)
jwt = JWTManager()
api = Api(app, prefix="/api/v1/")


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_connection.get(jti)
    return token_in_redis is not None


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


def create_app(app_config):

    app.config.update(app_config)

    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    app_logging(app)

    initialize_routes(api)

    with app.app_context():
        db.create_all()

    return app


def app_logging(app):

    formatter = RequestFormatter(
        "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s in [%(module)s: %(lineno)d]: %(message)s"
    )

    if app.config.get("LOG_FILE"):
        fh = logging.FileHandler(app.config.get("LOG_FILE"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

    strm = logging.StreamHandler()
    strm.setLevel(logging.DEBUG)
    strm.setFormatter(formatter)

    app.logger.addHandler(strm)
    app.logger.setLevel(logging.DEBUG)

    root = logging.getLogger("core")
    root.addHandler(strm)