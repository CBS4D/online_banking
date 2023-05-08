from marshmallow import post_load, validate
from copy import copy

from src.models.transaction import TransactionModel
from src.schemas import ma


class TransactionPostSchema(ma.Schema):

    amount = ma.Float(required=True, validate=validate.Range(min=1, max=50000))
    transaction_type = ma.String(required=True, validate=validate.OneOf(["credit", "debit"]))
    details = ma.String(required=True)
    created_date = ma.DateTime(format="%Y-%m-%d %H:%M:%S")

    @post_load
    def make_transaction(self, data, **kwargs):
        return TransactionModel(**data)
    

class TransactionPutSchema(ma.Schema):

    payee_id = ma.Integer(required=True)
    amount = ma.Float(required=True, validate=validate.Range(min=1, max=50000))
    transaction_type = ma.String(required=True, validate=validate.Equal("debit"))
    details = ma.String(required=True)
    created_date = ma.DateTime(format="%Y-%m-%d %H:%M:%S")

    @post_load
    def make_transaction(self, data, **kwargs):
        temp = copy(data)
        del temp["payee_id"]
        return TransactionModel(**temp)