from myapp import db
from datetime import datetime

class AccountType(db.Model):
    __tablename__ = 'account_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable = False)
    interest_rate = db.Column(db.Numeric(15, 2), nullable=False)  # Tipo de interés específico para este tipo de cuenta


    accounts = db.relationship('Account', back_populates='account_type')
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'interest_rate': self.interest_rate
        }
