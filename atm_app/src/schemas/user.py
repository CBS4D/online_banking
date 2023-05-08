from marshmallow import post_load, validates_schema, ValidationError, validate, pre_load
from werkzeug.security import generate_password_hash

from src.models.user import UserModel
from src.schemas.transaction import TransactionPostSchema
from src.schemas import ma


class UserRegistrationSchema(ma.Schema):

    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.Email(required=True, load_only=True)
    password = ma.String(required=True, load_only=True, validate=validate.Length(min=8, max=16))
    balance = ma.Float()
    created_date = ma.DateTime(format="%Y-%m-%d %H:%M:%S", load_only=True)
    updated_date = ma.DateTime(format="%Y-%m-%d %H:%M:%S", load_only=True)
    transactions = ma.List(ma.Nested(TransactionPostSchema), dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        data["password"] = generate_password_hash(data["password"], "sha256")
        return UserModel(**data)

    @validates_schema
    def password_check(self, data, **kwargs):
        upper_case = lower_case = is_digit = False

        if any(ele.isupper() for ele in data['password']):
            upper_case = True
        if any(ele.islower() for ele in data['password']):
            lower_case = True
        if any(ele.isdigit() for ele in data['password']):
            is_digit = True

        if not upper_case and lower_case and is_digit:
            raise ValidationError(
                {
                    "message": "Password must contain atleast one Upper, \
                        one lower case character and one digit."
                }
            )


class UserLoginSchema(ma.Schema):

    email = ma.Email(required=True, load_only=True)
    password = ma.String(required=True, load_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)
