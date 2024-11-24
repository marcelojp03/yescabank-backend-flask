from myapp import db
from models.Account.account import Account

class AccountRepository:
    def get_all(self):
        accounts = Account.query.all()
        return [account.serialize() for account in accounts]

    def get_by_id(self, id):
        account = Account.query.get(id)
        return account.serialize() if account else None
    
    def get_by_customer_id(self, customer_id):
        accounts = Account.query.filter_by(customer_id=customer_id).all()
        return [account.serialize() for account in accounts]

    def create(self, customer_id, account_number, account_type_id, currency_type_id, created_by, balance = None):
        new_account = Account(
            customer_id = customer_id,
            account_number=account_number,
            account_type_id=account_type_id,
            currency_type_id=currency_type_id,
            balance = balance,
            created_by = created_by
        )
        db.session.add(new_account)
        db.session.commit()
        return new_account.serialize()

    def update(self, id, account_number, account_type_id, currency_type_id, updated_by):
        account = Account.query.get(id)
        if account:
            account.account_number = account_number
            account.account_type_id = account_type_id
            account.currency_type_id = currency_type_id
            account.updated_by = updated_by
            db.session.commit()
        return account.serialize() if account else None

    def delete(self, id):
        account = Account.query.get(id)
        if account:
            db.session.delete(account)
            db.session.commit()
        return account.serialize() if account else None
