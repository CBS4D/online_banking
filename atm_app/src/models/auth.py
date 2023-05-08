from datetime import datetime

from flask import current_app as app
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from src.models.user import UserModel


class AuthDAO():

    def __init__(self, user_id, payeed_id=None):
        self.user = UserModel._search(id=user_id).first()
        if payeed_id:
            self.payee = UserModel._search(id=payeed_id).first()

    def verify_password(self, input_password):
        return check_password_hash(self.user.password, input_password)

    def encode_auth_token(self):
        """
        Generates the Auth Token
        """
        try:
            return create_access_token(identity=self.user.id)
        except Exception as e:
            raise e
        
    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'