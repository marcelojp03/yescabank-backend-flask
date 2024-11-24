from flask import jsonify, request, Blueprint
from repository.CurrencyTypeRepository import CurrencyTypeRepository
from Utils.Responses import Responses
from flask_jwt_extended import jwt_required


currency_type_bp = Blueprint('currency', __name__, url_prefix='/api/currencies')
currencyTypeRepository = CurrencyTypeRepository()

@currency_type_bp.route('/listar', methods=['GET'])
# @jwt_required()
def get_all():
    monedas = currencyTypeRepository.get_all()
    response = Responses.success(
            code = 0,
            data = monedas,
            description = 'Monedas encontradas correctamente'
        )  
    return jsonify(response)

@currency_type_bp.route('/buscar/<int:currency_id>', methods=['GET'])
@jwt_required()
def get_by_id(currency_id):
    currency = currencyTypeRepository.get_by_id(currency_id)
    if currency:
        response = Responses.success(
            code = 0,
            data = currency,
            description = 'Moneda encontrada correctamente'
        )  
        return jsonify(Responses.success(response))
    else:
        response = Responses.error(
            code = 1,
            description = f'Moneda con ID {currency_id} no encontrada'
        )  
        return jsonify(response)

@currency_type_bp.route('/registrar', methods=['POST'])
@jwt_required()
def create():
    data = request.json
    name = data.get('name')
    exchange_rate = data.get('exchange_rate')

    new_currency = currencyTypeRepository.create(name = name, exchange_rate = exchange_rate)
    if new_currency:
        response = Responses.success(
            code = 0,
            data = new_currency,
            description = 'Moneda creada con éxito'
        )  
        return jsonify(response)
    else:
        response = Responses.error(
            code = 1,
            description = 'Error al crear la moneda'
        )  
        return jsonify(response)   

@currency_type_bp.route('/editar/<int:currency_id>', methods=['PUT'])
@jwt_required()
def update(currency_id):
    data = request.json
    name = data.get('name')
    exchange_rate = data.get('exchange_rate')
    updated_currency = currencyTypeRepository.update(id = currency_id, name =  name, exchange_rate = exchange_rate)

    if updated_currency:
        return jsonify(Responses.success(updated_currency))
    else:
        return jsonify(Responses.error(f'Rol con ID {currency_id} no encontrado'))

# @currency_bp.route('/eliminar/<int:currency_id>', methods=['DELETE'])
# def delete(currency_id):
#     currency_deleted = currencyTypeRepository.delete(currency_id)
#     if currency_deleted:
#         return jsonify(Responses.success(currency_deleted))
#     else:
#         return jsonify(Responses.error(f'Rol con ID {currency_id} no encontrado'))
    
# @currency_bp.route('/eliminar-permanente/<int:rol_id>', methods=['DELETE'])
# def delete_role_per(rol_id):
#     rol_eliminado = currencyTypeRepository.deletePer(rol_id)
#     if rol_eliminado:
#         return jsonify(Responses.success(rol_eliminado))
#     else:
#         return jsonify(Responses.error(f'Rol con ID {rol_id} no encontrado'))
