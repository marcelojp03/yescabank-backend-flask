from myapp import db
from models.Account.account_type import AccountType

class AccountTypeRepository:
    def get_all(self):
        account_types = AccountType.query.all()
        return [account_type.serialize() for account_type in account_types]

    def get_by_id(self, id):
        account_type = AccountType.query.get(id)
        return account_type.serialize() if account_type else None

    def create(self, name, interest_rate):
        new_account_type = AccountType(
            name=name,
            interest_rate=interest_rate
        )
        db.session.add(new_account_type)
        db.session.commit()
        return new_account_type.serialize()

    def update(self, id, name, interest_rate):
        account_type = AccountType.query.get(id)
        if account_type:
            account_type.name = name
            account_type.interest_rate = interest_rate
            db.session.commit()
        return account_type.serialize() if account_type else None

    def delete(self, id):
        account_type = AccountType.query.get(id)
        if account_type:
            db.session.delete(account_type)
            db.session.commit()
        return account_type.serialize() if account_type else None
