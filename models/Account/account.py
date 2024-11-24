from myapp import db
from datetime import datetime

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) 
    account_number = db.Column(db.String(100), unique = True, nullable=False)
    account_type_id = db.Column(db.Integer, db.ForeignKey('account_type.id'), nullable=False)
    currency_type_id = db.Column(db.Integer, db.ForeignKey('currency_type.id'), nullable=False)
    balance = db.Column(db.Numeric(15, 2), nullable=False, default=0)  # Atributo para el monto, inicializado en 0
    status = db.Column(db.Boolean, server_default='1')
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow) # id del usuario que lo creo
    # created_himself = db.Column(db.Boolean) # si está en true, fue creado por el mismo
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    blocked_at = db.Column(db.TIMESTAMP, nullable=True)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)

    # Relaciones
    account_type = db.relationship('AccountType', back_populates='accounts', lazy='joined')
    currency_type = db.relationship('CurrencyType', back_populates='accounts',lazy='joined')
    customer = db.relationship('Customer', back_populates='accounts',lazy='joined')
    created_by_user = db.relationship('User', back_populates='created_accounts',lazy='joined')

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id, 
            'customer': self.customer.name if self.customer else None,
            'account_number': self.account_number,
            'account_type_id': self.account_type_id,
            'account_type': self.account_type.name if self.account_type else None,
            'currency_type_id': self.currency_type_id,
            'currency_type': self.currency_type.name if self.currency_type else None,
            'balance': self.balance,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'blocked_at': self.blocked_at,
            'created_by': self.created_by,
            'user' : self.created_by_user.name if self.created_by_user else None,
            'updated_by': self.updated_by,
        }
