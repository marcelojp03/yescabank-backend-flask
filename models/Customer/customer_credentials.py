from myapp import db
class CustomerCredentials(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    person_code = db.Column(db.String(100), unique=True, nullable=False)
    key = db.Column(db.String(255), nullable=False) 

    def serialize(self):
        return {
            'customer_id': self.customer_id,
            'person_code': self.person_code,
            'key': self.key
        }
