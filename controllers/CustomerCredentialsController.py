from flask import Blueprint, request, jsonify
from repository.CustomerCredentialsRepository import CustomerCredentialsRepository
from repository.AccountRepository import AccountRepository
from repository.CustomerRepository import CustomerRepository
from Utils.Responses import Responses
from flask_jwt_extended import  jwt_required

customer_credentials_bp = Blueprint('customer_credentials', __name__, url_prefix='/api/clientes-credentials')
customerCredentialsRepository = CustomerCredentialsRepository()
accountRepository = AccountRepository()
customerRepository = CustomerRepository()

@customer_credentials_bp.route('/listar', methods=['GET'])
@jwt_required()
def get_all_credentials():
    credentials = customerCredentialsRepository.get_all()
    response = Responses.success(
        code=0,
        data=credentials,
        description='Credenciales listadas correctamente'
    )
    return jsonify(response)

@customer_credentials_bp.route('/buscar/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_credentials_by_customer_id(customer_id):
    credentials = customerCredentialsRepository.get_by_customer_id(customer_id)
    if credentials:
        response = Responses.success(
            code=0,
            data=credentials,
            description='Credenciales encontradas'
        )
    else:
        response = Responses.error(
            code=1,
            description=f'No se encontraron credenciales para el cliente con ID {customer_id}'
        )
    return jsonify(response)

@customer_credentials_bp.route('/login', methods=['POST'])
# @jwt_required()
def customer_login():
    data = request.json
    person_code = data.get('person_code')
    key = data.get('key')

    if not person_code or not key:
        response = Responses.error(
            code = 1,
            description = 'Código persona y clave son obligatorios'
        )
        return jsonify(response)
    
    credentials = customerCredentialsRepository.get_by_person_key(person_code=person_code, key=key)

    if not credentials:
        response = Responses.error(
            code = 1,
            description = 'Credenciales inválidas'
        )
        return jsonify(response)
    
    customer_account = accountRepository.get_by_customer_id(credentials['customer_id'])
    if not customer_account:
        response = Responses.error(
            code = 1,
            description = 'Error al obtener las cuentas del cliente'
        )
        return jsonify(response)
    
    customer_information = customerRepository.get_by_id(credentials['customer_id'])
    if not customer_information:
        response = Responses.error(
            code = 1,
            description = 'Error al obtener los datos del cliente'
        )
        return jsonify(response)

    response = Responses.success(
            code=0,
            data={
                "customer": customer_information,
                "account": customer_account,
            },
            description="Credenciales válidas"
        )
    return jsonify(response), 201
