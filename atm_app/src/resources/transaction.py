from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.transaction import TransactionDAO
from src.models.user import UserDAO
from src.schemas.transaction import TransactionPostSchema, TransactionPutSchema
from src.utils.common import generate_response
from src.utils.http_code import (
    HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND, HTTP_200_OK,
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR)


class AuthResource(Resource):

    decorators = [jwt_required()]


class TranctionResource(AuthResource):
    
    def get(self):
        user_id = get_jwt_identity()
        user_dao = UserDAO(user_id)
        if not user_dao.user:
            return generate_response(
                message="No user/transactions found",
                status=HTTP_404_NOT_FOUND
            )
        user_transactions = user_dao.get_user_transactions()
        user_data = TransactionPostSchema(many=True).dump(user_transactions)
        return generate_response(
            data=user_data,
            message="success",
            status=HTTP_200_OK
        )

    def post(self):
        try:
            request_data = request.get_json()
            # validate data
            transaction_schema = TransactionPostSchema()
            user_id = get_jwt_identity()
            transaction = transaction_schema.load(request_data)
            user_dao = UserDAO(user_id)
            if not user_dao.user:
                return generate_response(
                    message="User not found",
                    status=HTTP_404_NOT_FOUND
                )

            if transaction.transaction_type == 'credit':
                user_dao.credit_account_balance(transaction.amount)
            else:
                if user_dao.user.balance < transaction.amount:
                    return generate_response(
                        message="Transaction not allowed, insufficient balance.",
                        status=HTTP_422_UNPROCESSABLE_ENTITY
                    )
                user_dao.debit_account_balance(transaction.amount)

            transaction.user_id = user_id
            transaction.save()
            return generate_response(
                data=transaction_schema.dump(transaction),
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
        
    def put(self):
        try:
            request_data = request.get_json()
            # validate data
            transaction_schema = TransactionPutSchema()
            user_id = get_jwt_identity()
            transaction = transaction_schema.load(request_data)

            if user_id == request_data['payee_id']:
                return generate_response(
                    message="Operation not allowed",
                    status=HTTP_422_UNPROCESSABLE_ENTITY
                )
            user_dao = UserDAO(user_id, request_data.get('payee_id'))
            if not user_dao.user:
                return generate_response(
                    message="User not found",
                    status=HTTP_404_NOT_FOUND
                )
            if not user_dao.payee:
                return generate_response(
                    message="Payee not found",
                    status=HTTP_404_NOT_FOUND
                )

            payee_transaction = TransactionDAO(
                transaction.amount, "credit", transaction.details,
                request_data.get('payee_id')).transaction

            if user_dao.user.balance < transaction.amount:
                return generate_response(
                message="Transaction not allowed, Insufficient balance",
                status=HTTP_422_UNPROCESSABLE_ENTITY
            )

            user_dao.transfer_between_accounts(transaction, payee_transaction)

            return generate_response(
                data=transaction_schema.dump(transaction),
                message="success",
                status=HTTP_200_OK
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