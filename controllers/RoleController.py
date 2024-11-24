from flask import jsonify, request, Blueprint
from repository.RoleRepository import RoleRepository
from Utils.Responses import Responses
from flask_jwt_extended import jwt_required


role_bp = Blueprint('role', __name__, url_prefix='/api/roles')
roleRepository = RoleRepository()

@role_bp.route('/listar', methods=['GET'])
# @jwt_required()
def get_all_roles():
    roles = roleRepository.get_all()
    response = Responses.success(
            code = 0,
            data = roles,
            description = 'Roles encontrados correctamente'
        )  
    return jsonify(response)

@role_bp.route('/buscar/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id):
    role = roleRepository.get_by_id(role_id)
    if role:
        response = Responses.success(
            code = 0,
            data = role,
            description = 'Rol encontrado correctamente'
        )  
        return jsonify(Responses.success(response))
    else:
        response = Responses.error(
            code = 1,
            description = f'Rol con ID {role_id} no encontrado'
        )  
        return jsonify(response)

@role_bp.route('/registrar', methods=['POST'])
@jwt_required()
def create_role():
    data = request.json

    name = data.get('name')
    description = data.get('description')

    new_role = roleRepository.create(name, description)
    if new_role:
        response = Responses.success(
            code = 0,
            data = new_role,
            description = 'Rol creado con éxito'
        )  
        return jsonify(response)
    else:
        response = Responses.error(
            code = 1,
            description = 'Error al crear el rol'
        )  
        return jsonify(response)   

@role_bp.route('/editar/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    if nombre and descripcion:
        rol_actualizado = roleRepository.update(role_id, nombre,descripcion)
        if rol_actualizado:
            return jsonify(Responses.success(rol_actualizado))
        else:
            return jsonify(Responses.error(f'Rol con ID {role_id} no encontrado'))
    else:
        return jsonify(Responses.error('El nombre y descripcion del rol es obligatorio'))

@role_bp.route('/eliminar/<int:rol_id>', methods=['DELETE'])
def delete_role(rol_id):
    rol_eliminado = roleRepository.delete(rol_id)
    if rol_eliminado:
        return jsonify(Responses.success(rol_eliminado))
    else:
        return jsonify(Responses.error(f'Rol con ID {rol_id} no encontrado'))
    
@role_bp.route('/eliminar-permanente/<int:rol_id>', methods=['DELETE'])
def delete_role_per(rol_id):
    rol_eliminado = roleRepository.deletePer(rol_id)
    if rol_eliminado:
        return jsonify(Responses.success(rol_eliminado))
    else:
        return jsonify(Responses.error(f'Rol con ID {rol_id} no encontrado'))

@role_bp.route('/menu/<int:user_id>', methods=['GET'])
def get_role_by_idusuario(user_id):
    menu = roleRepository.get_menu_for_user(user_id)
    if menu:
        return jsonify(Responses.success(menu))
    else:
        return jsonify(Responses.error(f'Usuario con ID {user_id} no encontrado'))