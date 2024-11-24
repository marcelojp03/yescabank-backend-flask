from myapp import db
from models.Customer.customer_credentials import CustomerCredentials

class CustomerCredentialsRepository:
    def get_all(self):
        credentials = CustomerCredentials.query.all()
        return [cred.serialize() for cred in credentials]

    def get_by_customer_id(self, customer_id):
        credentials = CustomerCredentials.query.filter_by(customer_id=customer_id).first()
        return credentials.serialize() if credentials else None
    
    def get_by_person_key(self, person_code, key):
        credentials = CustomerCredentials.query.filter_by(person_code=person_code, key=key).first()
        return credentials.serialize() if credentials else None

    def create(self, customer_id, person_code, key):
        new_credential = CustomerCredentials(
            customer_id=customer_id,
            person_code=person_code,
            key=key
        )
        db.session.add(new_credential)
        db.session.commit()
        return new_credential.serialize()

