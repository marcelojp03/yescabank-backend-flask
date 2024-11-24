from myapp import db
from datetime import datetime

class CustomerPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    photo_type = db.Column(db.String(50), nullable=False)  # Por ejemplo: 'profile', 'id_front', 'id_back'
    photo_url = db.Column(db.String(255), nullable=False)  # URL o ruta de la imagen almacenada
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'photo_type': self.photo_type,
            'photo_url': self.photo_url,
            'created_at': self.created_at
        }
