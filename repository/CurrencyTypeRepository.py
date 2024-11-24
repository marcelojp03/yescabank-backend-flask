
from myapp import db
from models.CurrencyType.currency_type import CurrencyType

class CurrencyTypeRepository:
    def get_all(self):
        currencies = CurrencyType.query.all()
        return [currency.serialize() for currency in currencies]

    def get_by_id(self, id):
        currency = CurrencyType.query.get(id)
        return currency.serialize() if currency else None

    def create(self, name, exchange_rate = None):
        new_currency = CurrencyType(
            name = name,
            exchange_rate = exchange_rate
        )
        db.session.add(new_currency)
        db.session.commit()
        return new_currency.serialize()

    def update(self, id, name, exchange_rate = None):
        currency = CurrencyType.query.get(id)
        if currency:
            currency.name = name
            currency.exchange_rate = exchange_rate
            db.session.commit()

        return currency.serialize() if currency else None

    def delete(self, id):
        currency = CurrencyType.query.get(id)
        if currency:
            #db.session.delete(rol)
            currency.status = False
            db.session.commit()

        return currency.serialize() if currency else None
    
    # def deletePer(self, rol_id):
    #     rol = CurrencyType.query.get(rol_id)
    #     if rol:
    #         db.session.delete(rol)
    #         #rol.estado=False
    #         db.session.commit()

    #     return rol.serialize() if rol else None