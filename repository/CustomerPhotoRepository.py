from myapp import db
from models.Customer.customer_photos import CustomerPhoto

class CustomerPhotoRepository:
    def get_all(self):
        photos = CustomerPhoto.query.all()
        return [photo.serialize() for photo in photos]

    def get_by_customer_id(self, customer_id):
        photos = CustomerPhoto.query.filter_by(customer_id=customer_id).all()
        return [photo.serialize() for photo in photos]

    def create(self, customer_id, photo_type, photo_url):
        new_photo = CustomerPhoto(
            customer_id=customer_id,
            photo_type=photo_type,
            photo_url=photo_url
        )
        db.session.add(new_photo)
        db.session.commit()
        return new_photo.serialize()
