from myapp import db

class CurrencyType(db.Model):
    __tablename__ = 'currency_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable = False)
    exchange_rate = db.Column(db.Numeric(15, 2), nullable=False)  # Almacenar el tipo de cambio

    accounts = db.relationship('Account', back_populates='currency_type')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'exchange_rate': self.exchange_rate        
        }
