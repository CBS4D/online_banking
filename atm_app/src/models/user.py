from datetime import datetime

from src.models import db, BaseActions


class UserModel(db.Model, BaseActions):

    __tablename__ = 'user_details'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime)

    transactions = db.relationship('TransactionModel', backref='user_transactions')


class UserDAO():

    def __init__(self, user_id, payeed_id=None):
        self.user = UserModel._search(id=user_id).first()
        if payeed_id:
            self.payee = UserModel._search(id=payeed_id).first()

    def get_user_transactions(self):
        return self.user.transactions

    def credit_account_balance(self, amount):
        self.user.balance += amount
        self.user.update()

    def debit_account_balance(self, amount):
        self.user.balance -= amount
        self.user.update()

    def transfer_between_accounts(self, user_transaction, payee_transaction):
        """
        need to make all database queries in one transaction.
        if any query fails will rollback complete transaction to maintain consistancy 
        bewtween both user's transaction.
        """
        try:
            user_transaction.user_id = self.user.id
            amount = user_transaction.amount
            self.user.balance -= amount
            self.payee.balance += amount
            db.session.add_all([self.user, self.payee, user_transaction, payee_transaction])
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e