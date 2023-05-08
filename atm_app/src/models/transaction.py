from datetime import datetime
from src.models import db, BaseActions


class TransactionModel(db.Model, BaseActions):

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_details.id"), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class TransactionDAO():

    def __init__(self, amount, transaction_type, details, user_id):
        self.transaction = TransactionModel()
        self.transaction.amount = amount
        self.transaction.transaction_type = transaction_type
        self.transaction.details = details
        self.transaction.user_id = user_id

    def transfer_between_accounts(transactions):
        db.session.add_all(transactions)