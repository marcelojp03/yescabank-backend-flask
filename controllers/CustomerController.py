from flask import Blueprint, request, jsonify
from repository.CustomerRepository import CustomerRepository
from Utils.Responses import Responses
from flask_jwt_extended import  jwt_required

customer_bp = Blueprint('customer', __name__, url_prefix='/api/customers')
customerRepository = CustomerRepository()

@customer_bp.route('/listar', methods=['GET'])
# @jwt_required()
def get_all_customers():
    customers = customerRepository.get_all()
    response = Responses.success(
        code=0,
        data=customers,
        description='Clientes listados correctamente'
    )
    return jsonify(response)

@customer_bp.route('/buscar/<int:customer_id>', methods=['GET'])
# @jwt_required()
def get_customer_by_id(customer_id):
    customer = customerRepository.get_by_id(customer_id)
    if customer:
        response = Responses.success(
            code=0,
            data=customer,
            description='Cliente encontrado'
        )
    else:
        response = Responses.error(
            code=1,
            description=f'Cliente con ID {customer_id} no encontrado'
        )
    return jsonify(response)

@customer_bp.route('/registrar', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.json
    required_fields = ['name', 'lastname', 'ci', 'birthdate', 'email', 'occupation', 'address']
    if all(field in data for field in required_fields):
        new_customer = customerRepository.create(
            name=data['name'],
            lastname=data['lastname'],
            ci=data['ci'],
            birthdate=data['birthdate'],
            email=data['email'],
            phone=data.get('phone'),
            occupation=data['occupation'],
            address=data['address'],
            reference=data.get('reference'),
            reference_phone=data.get('reference_phone')
        )
        response = Responses.success(
            code=0,
            data=new_customer,
            description='Cliente creado correctamente'
        )
    else:
        response = Responses.error(
            code=1,
            description='Faltan campos requeridos'
        )
    return jsonify(response)

