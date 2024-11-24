from flask import jsonify, request, Blueprint
from repository.AccountRepository import AccountRepository
from repository.CustomerRepository import CustomerRepository
from repository.CustomerCredentialsRepository import CustomerCredentialsRepository
from Utils.Responses import Responses
from flask_jwt_extended import jwt_required
import random
from flask_mail import Message
from myapp import mail

account_bp = Blueprint('account', __name__, url_prefix='/api/accounts')
accountRepository = AccountRepository()
customerRepository = CustomerRepository()
customerCredentialsRepository = CustomerCredentialsRepository()

@account_bp.route('/listar', methods=['GET'])
# @jwt_required()
def get_all():
    accounts = accountRepository.get_all()
    response = Responses.success(
        code=0,
        data=accounts,
        description='Cuentas listadas correctamente'
    )
    return jsonify(response)

@account_bp.route('/buscar/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    account = accountRepository.get_by_id(id)
    if account:
        response = Responses.success(
            code=0,
            data=account,
            description='Cuenta encontrada correctamente'
        )
        return jsonify(response)
    else:
        response = Responses.error(
            code=1,
            description=f'Cuenta con ID {id} no encontrada'
        )
        return jsonify(response)

@account_bp.route('/registrar', methods=['POST'])
@jwt_required()
def create():
    data = request.json
    account_number = data.get('account_number')
    account_type_id = data.get('account_type_id')
    currency_type_id = data.get('currency_type_id')
    balance = data.get('balance')
    created_by = data.get('created_by')

    new_account = accountRepository.create(
        account_number=account_number, 
        account_type_id=account_type_id,
        currency_type_id=currency_type_id,
        balance = balance,
        created_by=created_by
    )

    if new_account:
        response = Responses.success(
            code=0,
            data=new_account,
            description='Cuenta creada con éxito'
        )
        return jsonify(response)
    else:
        response = Responses.error(
            code=1,
            description='Error al crear la cuenta'
        )
        return jsonify(response)

@account_bp.route('/editar/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    data = request.json
    account_number = data.get('account_number')
    account_type_id = data.get('account_type_id')
    currency_type_id = data.get('currency_type_id')
    updated_by = data.get('updated_by')

    account_updated = accountRepository.update(
        id=id, 
        account_number=account_number, 
        account_type_id=account_type_id,
        currency_type_id=currency_type_id,
        updated_by=updated_by
    )

    if account_updated:
        return jsonify(Responses.success(account_updated))
    else:
        return jsonify(Responses.error(f'Cuenta con ID {id} no encontrada'))

@account_bp.route('/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    account_deleted = accountRepository.delete(id)
    if account_deleted:
        return jsonify(Responses.success(account_deleted))
    else:
        return jsonify(Responses.error(f'Cuenta con ID {id} no encontrada'))


@account_bp.route('/crear-cuenta', methods=['POST'])
# @jwt_required()
def create_account():
    data = request.json
    
    # Datos del cliente
    name = data.get('name')
    lastname = data.get('lastname')
    ci = data.get('ci')
    birthdate = data.get('birthdate')
    email = data.get('email')
    phone = data.get('phone')
    occupation = data.get('occupation')
    address = data.get('address')
    reference = data.get('reference')
    reference_phone = data.get('reference_phone')

    # Datos de la cuenta
    account_number = data.get('account_number')
    account_type_id = data.get('account_type_id')
    currency_type_id = data.get('currency_type_id')
    user_id = data.get('user_id')

    try:
        # Crear el cliente
        new_customer = customerRepository.create(
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

        if not new_customer:
            return jsonify(Responses.error(code=1, description="Error al crear el cliente")), 400
        

        # 2. Generar credenciales del cliente
        person_code = str(random.randint(10000000, 99999999))
        key = str(random.randint(1000, 9999))

        new_credentials = customerCredentialsRepository.create(
            customer_id=new_customer['id'],
            person_code=person_code,
            key=key
        )

        if not new_credentials:
            return jsonify(Responses.error(code=1, description="Error al crear las credenciales")), 400
        
        # Crear la cuenta para el cliente
        new_account = accountRepository.create(
            customer_id = new_customer['id'],  # Relacionar cuenta con el cliente creado
            account_number=account_number,
            account_type_id=account_type_id,
            currency_type_id=currency_type_id,
            created_by = user_id,
        )
        if not new_account:
            return jsonify(Responses.error(code=1, description="Error al crear la cuenta")), 400
        
        # 4. Enviar credenciales por correo
        send_credentials_email(email, person_code, key)

        response = Responses.success(
            code=0,
            data={
                "customer": new_customer,
                "account": new_account,
                "credentials": new_credentials
            },
            description="Cuenta y cliente creados correctamente"
        )
        return jsonify(response), 201

        # if new_account:
        #     response = Responses.success(
        #         code = 0,
        #         data={
        #             'customer': new_customer,
        #             'account': new_account
        #         },
        #         description='Cliente y cuenta creados correctamente'
        #     )
        #     return jsonify(response)

    except Exception as e:
        response = Responses.error(
            code = 1,
            description=f'Error al crear cliente o cuenta: {str(e)}'
        )
        return jsonify(response)
    
def send_credentials_email(to_email, person_code, key):
    try:
        msg = Message("Tus credenciales bancarias",
                      sender="yescabank@sent.com",
                      recipients=[to_email])

        msg.body = f"""
        Estimado cliente,

        Tus credenciales bancarias son las siguientes:
        - Código de persona: {person_code}
        - Clave: {key}

        Por favor, guarda esta información en un lugar seguro.

        Atentamente,
        Yesca Bank
        """
        mail.send(msg)
        print('Correo con credenciales mandado!')

    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# @account_bp.route('/editar/<int:id>', methods=['PUT'])
@account_bp.route("/send_test_email", methods = ['GET'])
def send_test_email():
    try:
        msg = Message("Correo de Prueba",
                      sender="yescabank@sent.com",
                      recipients=["marcelojimenezb@gmail.com"])
        msg.body = "Este es un correo de prueba enviado desde Flask-Mail."
        mail.send(msg)
        return "Correo de prueba enviado!"
    except Exception as e:
        return f"Error al enviar correo: {e}"

