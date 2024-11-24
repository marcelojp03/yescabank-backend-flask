from flask import jsonify, request, Blueprint
from repository.AccountTypeRepository import AccountTypeRepository
from Utils.Responses import Responses
from flask_jwt_extended import jwt_required

account_type_bp = Blueprint('account_type', __name__, url_prefix='/api/account-types')
accountTypeRepository = AccountTypeRepository()

@account_type_bp.route('/listar', methods=['GET'])
# @jwt_required()
def get_all():
    account_types = accountTypeRepository.get_all()
    response = Responses.success(
        code=0,
        data=account_types,
        description='Tipos de cuenta listados correctamente'
    )
    return jsonify(response)

@account_type_bp.route('/buscar/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    account_type = accountTypeRepository.get_by_id(id)
    if account_type:
        response = Responses.success(
            code=0,
            data=account_type,
            description='Tipo de cuenta encontrado correctamente'
        )
        return jsonify(response)
    else:
        response = Responses.error(
            code=1,
            description=f'Tipo de cuenta con ID {id} no encontrado'
        )
        return jsonify(response)

@account_type_bp.route('/registrar', methods=['POST'])
@jwt_required()
def create():
    data = request.json
    name = data.get('name')
    interest_rate = data.get('interest_rate')

    new_account_type = accountTypeRepository.create(name=name, interest_rate=interest_rate)
    if new_account_type:
        response = Responses.success(
            code=0,
            data=new_account_type,
            description='Tipo de cuenta creado con éxito'
        )
        return jsonify(response)
    else:
        response = Responses.error(
            code=1,
            description='Error al crear el tipo de cuenta'
        )
        return jsonify(response)

@account_type_bp.route('/editar/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    data = request.json
    name = data.get('name')
    interest_rate = data.get('interest_rate')
    
    account_type_updated = accountTypeRepository.update(id=id, name=name, interest_rate=interest_rate)
    if account_type_updated:
        return jsonify(Responses.success(account_type_updated))
    else:
        return jsonify(Responses.error(f'Tipo de cuenta con ID {id} no encontrado'))

@account_type_bp.route('/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    account_type_deleted = accountTypeRepository.delete(id)
    if account_type_deleted:
        return jsonify(Responses.success(account_type_deleted))
    else:
        return jsonify(Responses.error(f'Tipo de cuenta con ID {id} no encontrado'))
