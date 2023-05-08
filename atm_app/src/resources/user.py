from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.user import UserModel
from src.schemas.user import UserRegistrationSchema
from src.utils.common import generate_response
from src.utils.http_code import (
    HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND, HTTP_200_OK,
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR)


class AuthResource(Resource):

    decorators = [jwt_required()]


class UserResource(AuthResource):
    
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                return generate_response(
                    message="User not found",
                    status=HTTP_404_NOT_FOUND
                )

            user_data = UserRegistrationSchema(exclude=["transactions"]).dump(user)
            return generate_response(
                data=user_data,
                message="Sucess",
                status=HTTP_200_OK
            )
        except Exception as e:
            return generate_response(
                data=str(e),
                message="failed",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    # def post(self):
    #     try:
    #         request_data = request.get_json()
    #         # validate data
    #         user_schema = UserRegistrationSchema()
    #         user = user_schema.load(request_data)
    #         user.save()
    #         return generate_response(
    #             data=user_schema.dump(user),
    #             message="success",
    #             status=HTTP_201_CREATED
    #         )

    #     except ValidationError as v_err:
    #         return generate_response(
    #             data=v_err.messages,
    #             message="failed",
    #             status=HTTP_422_UNPROCESSABLE_ENTITY
    #         )
    #     except Exception as e:
    #         return generate_response(
    #             data=str(e),
    #             message="failed",
    #             status=HTTP_500_INTERNAL_SERVER_ERROR
    #         )
