from myapp import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.Integer, unique = True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    occupation = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    reference = db.Column(db.String(50))
    reference_phone = db.Column(db.String(50))
    status = db.Column(db.Boolean, server_default='1')
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    blocked_at = db.Column(db.TIMESTAMP, nullable=True)

    accounts = db.relationship('Account', back_populates='customer')


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'ci': self.ci,
            'birthdate': self.birthdate,
            'email': self.email,
            'phone': self.phone,
            'occupation': self.occupation,
            'address': self.address,
            'reference': self.reference,
            'reference_phone': self.reference_phone,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'blocked_at': self.blocked_at
        }
