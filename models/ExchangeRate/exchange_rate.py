from myapp import db
from datetime import datetime

class ExchangeRate(db.Model):
    __tablename__ = 'account_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rate = db.Column()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.rate,          
        }
