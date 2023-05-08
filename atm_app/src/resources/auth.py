from datetime import datetime
from flask import request, current_app as app
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import get_jwt, jwt_required

from src.utils.redis_connection import redis_connection
from src.models.user import UserModel
from src.models.auth import AuthDAO
from src.schemas.user import UserRegistrationSchema, UserLoginSchema
from src.utils.common import generate_response
from src.utils.http_code import (
    HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,
    HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR)


class UserRegistrationResource(Resource):

    def post(self):
        """
        User Registration
        """
        try:
            request_data = request.get_json()
            # validate data
            user_schema = UserRegistrationSchema()
            user = user_schema.load(request_data)

            user_db = UserModel._search(email=user.email).first()
            if user_db:
                return generate_response(
                    message="User already exists. Please Log in.",
                    status=HTTP_422_UNPROCESSABLE_ENTITY
                )

            user.save()
            return generate_response(
                data=user_schema.dump(user),
                message="success",
                status=HTTP_201_CREATED
            )

        except ValidationError as v_err:
            return generate_response(
                data=v_err.messages,
                message="failed",
                status=HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as e:
            return generate_response(
                data=str(e),
                message="failed",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class UserAuthResource(Resource):

    def post(self):
        """
        User Login Resource
        """
        try:
            request_data = request.get_json()
            # validate data
            user_schema = UserLoginSchema()
            user = user_schema.load(request_data)

            user_db = UserModel._search(email=user.email).first()

            if not user_db:
                return generate_response(
                data="Invalid credentials",
                message="failed",
                status=HTTP_401_UNAUTHORIZED
            )

            auth_dao = AuthDAO(user_db.id)
            if not auth_dao.verify_password(user.password):
                return generate_response(
                data="Invalid credentials",
                message="failed",
                status=HTTP_401_UNAUTHORIZED
            )
            
            auth_token = auth_dao.encode_auth_token()

            return generate_response(
                data={'auth_token': auth_token},
                message="success",
                status=HTTP_201_CREATED
            )

        except ValidationError as v_err:
            return generate_response(
                data=v_err.messages,
                message="failed",
                status=HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as e:
            return generate_response(
                data=str(e),
                message="failed",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @jwt_required()
    def delete(self):
        try:
            jwt_identifier = get_jwt()["jti"]
            redis_connection.set(jwt_identifier, "", ex=app.config["JWT_ACCESS_TOKEN_EXPIRES"])
            return generate_response(
                message="User Logged Out.",
                status=200
            )
        except Exception as e:
            return generate_response(
                data=str(e),
                message="failed",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )