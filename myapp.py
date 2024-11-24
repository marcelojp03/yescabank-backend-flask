from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config
from flask_jwt_extended import JWTManager
from flask_mail import Mail
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Inicializar JWT
    JWTManager(app)

    db.init_app(app)
    mail.init_app(app)

    from controllers import AuthController
    from controllers import UserController
    from controllers import RoleController
    from controllers import CurrencyTypeController
    from controllers import AccountController
    from controllers import AccountTypeController
    from controllers import CustomerController
    from controllers import CustomerCredentialsController


    app.register_blueprint(AuthController.auth_bp)
    app.register_blueprint(UserController.user_bp)
    app.register_blueprint(RoleController.role_bp)
    app.register_blueprint(CurrencyTypeController.currency_type_bp)
    app.register_blueprint(AccountController.account_bp)
    app.register_blueprint(AccountTypeController.account_type_bp)
    app.register_blueprint(CustomerController.customer_bp)
    app.register_blueprint(CustomerCredentialsController.customer_credentials_bp)


    # crea las tablas de los modelos
    with app.app_context():
        db.create_all()
    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(port=7777, debug=True)
