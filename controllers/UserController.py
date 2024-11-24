from flask import Blueprint, request, jsonify
from repository.UserRepository import UserRepository
from repository.UserRoleRepository import UserRoleRepository
from Utils.Responses import Responses
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt

user_bp = Blueprint('user', __name__, url_prefix='/api/users')
userRepository = UserRepository()
userRoleRepository = UserRoleRepository()
bcrypt = Bcrypt()

@user_bp.route('/listar', methods=['GET'])
# @jwt_required()
def get_all_users():
    users = userRepository.get_all()
    response = Responses.success(
        code = 0,
        data = users,
        description = 'Usuarios listados correctamente'
    )
    return jsonify(response)

@user_bp.route('/buscar/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_user_by_id(user_id):
    user = userRepository.get_by_id(user_id)
    if user:
        response = Responses.success(
            code = 0,
            data = user,
            description = 'Usuario encontrado'
        )
        return jsonify(response)
    else:
        response = Responses.error(
            code = 0,
            description = f'Usuario con ID {user_id} no encontrado'
        )
        return jsonify(response)

@user_bp.route('/registrar', methods=['POST'])
# @jwt_required()
def create_user():
    data = request.json
    
    name = data.get('name')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('contraseña')
    #password_hashed=generate_password_hash(password)
    password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    phone = data.get('phone')
    photo = data.get('photo')
    role_id = data.get('role_id')
    
    if name and lastname and email and password_hashed:
        newUser = userRepository.create(
            name=name,
            lastname=lastname,
            email=email,
            password=password_hashed, 
            phone=phone,
            photo=photo,
        )
        if not newUser:
            response = Responses.error(
                code = 1,
                description = 'Error al crear el usuario'
            )   
            return jsonify(response)
        if role_id:

            nuevo_registro = userRoleRepository.create(user_id=newUser['id'],role_id = role_id)

            if not nuevo_registro:
                response = Responses.error(
                    code = 1,
                    description = 'Error al asignar el rol al usuario'
                    )    
                return jsonify(response)
            
            response = Responses.success(
                code = 0,
                data = newUser,
                description = 'Usuario creado correctamente'
            )   
            return jsonify(response)
    else:
        response = Responses.error(
                code = 1,
                description = 'Nombre de usuario, contraseña, nombre y correo son obligatorios'
            )   
        return jsonify(response)

@user_bp.route('/eliminar-permanente/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def delete_user_per(usuario_id):
    usuario_eliminado = userRepository.deletePer(usuario_id)
    if usuario_eliminado:
        return jsonify(Responses.success(usuario_eliminado))
    else:
        return jsonify(Responses.error(f'Usuario con ID {usuario_id} no encontrado'))
    
@user_bp.route('/asignar-rol', methods=['POST'])
@jwt_required()
def assign_role():
    data = request.json

    user_id = data.get('user_id')
    role_id = data.get('role_id')

    if  role_id and user_id:
        nuevo_registro = userRoleRepository.create(user_id, role_id)
        return jsonify(Responses.success(nuevo_registro))
    else:
        return jsonify(Responses.error('rol_id y usuario_id son obligatorios'))
    
@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    current_user_id = get_jwt_identity()  # Obtener la identidad del token
    return jsonify(message=f"This is a protected route. Current user ID: {current_user_id}")
    

# @user_bp.route('/usuario-rol', methods=['GET'])
# def get_all():
#     response = userRoleRepository.get_all()
#     return jsonify(Responses.success(response))

# @user_bp.route('/buscar/usuario/<int:usuario_id>', methods=['GET'])
# def get_by_user_id(usuario_id):
#     response = userRoleRepository.get_by_user_id(usuario_id)
#     if response:
#         return jsonify(Responses.success(response))
#     else:
#         return jsonify(Responses.error(f'Rol con userid {usuario_id} no encontrado'))
    
# @user_bp.route('/buscar/<int:rol_id>', methods=['GET'])
# def get_by_id(rol_id):
#     response = userRoleRepository.get_by_role_id(rol_id)
#     if response:
#         return jsonify(Responses.success(response))
#     else:
#         return jsonify(Responses.error(f'Rol con ID {rol_id} no encontrado'))
    


    # @user_bp.route('/editar/<int:usuario_id>', methods=['POST'])
# def update_user(usuario_id):
#     data = request.json

#     nombre_usuario = data.get('nombre_usuario')
#     contraseña = data.get('contraseña')   
#     nombre = data.get('nombre')
#     correo = data.get('correo')
#     rol_id=data.get('rol_id')
#     foto = data.get('foto')

#     if contraseña:
#         contraseña_hash=generate_password_hash(contraseña)
#     else:
#         contraseña_hash=None

#     user_entity.eliminar_imagen_usuario(usuario_id)

#     if nombre_usuario and nombre and correo:
#         usuario_actualizado = user_entity.update(usuario_id, nombre_usuario, contraseña_hash, nombre, correo, foto)
#         if usuario_actualizado:
#             rol_usuario_update=user_role_entity.update(rol_id,usuario_id)
#             if rol_usuario_update:
#                 return jsonify(Responses.success(usuario_actualizado))
#         else:
#             return jsonify(Responses.error(f'Usuario con ID {usuario_id} no encontrado'))
#     else:
#         return jsonify(Responses.error('Nombre de usuario, contraseña, nombre y correo son obligatorios'))



