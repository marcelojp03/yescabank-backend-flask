from myapp import db
from models.Customer.customer import Customer

class CustomerRepository:
    def get_all(self):
        customers = Customer.query.all()
        return [customer.serialize() for customer in customers]

    def get_by_id(self, customer_id):
        customer = Customer.query.get(customer_id)
        return customer.serialize() if customer else None

    def create(self, name, lastname, ci, birthdate, email, phone, occupation, address, reference=None, reference_phone=None):
        new_customer = Customer(
            name=name,
            lastname=lastname,
            ci=ci,
            birthdate=birthdate,
            email=email,
            phone=phone,
            occupation=occupation,
            address=address,
            reference=reference,
            reference_phone=reference_phone
        )
        db.session.add(new_customer)
        db.session.commit()
        return new_customer.serialize()

    def update(self, customer_id, data):
        customer = Customer.query.get(customer_id)
        if customer:
            for key, value in data.items():
                setattr(customer, key, value)
            db.session.commit()
            return customer.serialize()
        return None
