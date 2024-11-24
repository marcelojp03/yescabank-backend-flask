from myapp import db
from flask import current_app
from models.User.user import User
import base64
import os
from PIL import Image
from io import BytesIO
import hashlib

# user_role_entity=UserRoleEntity


class UserRepository:
    def get_all(self):
        users = User.query.all()
        # usuarios_con_roles=[]
        # for usuario in users:    
        #     usuario_serializado=usuario.serialize()
        #     roles_usuario = user_role_entity.get_by_user_id(self, usuario.id)
        #     print(roles_usuario)
        #     if roles_usuario:
        #             usuario_serializado['roles'] = roles_usuario
        #             # usuario_serializado['rol_id'] = roles_usuario['rol_id']

        #     usuarios_con_roles.append(usuario_serializado)

        # return usuarios_con_roles if users else None
        return [user.serialize() for user in users]

    def get_by_id(self, user_id):
        user = User.query.get(user_id)
        if user:
            usuario_serializado = user.serialize()
            # roles_usuario = user_role_entity.get_by_user_id(self, usuario.id)
            # print(roles_usuario)
            # if roles_usuario:
            #         usuario_serializado['roles'] = roles_usuario
            #         # usuario_serializado['rol_id'] = roles_usuario['rol_id']
            photo = user.photo
            if photo:
                ruta_imagen = os.path.join(current_app.config['IMAGENES_USUARIOS_CARPETA'], photo)
                with open(ruta_imagen, 'rb') as f:
                    imagen_bytes = f.read()
                    imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
                usuario_serializado['photo'] = imagen_base64
            return usuario_serializado
        else:
            return None
    
    def get_by_name(self, name):
        user=User.query.filter_by(name=name).first()
        return user.serialize() if user else None
    
    def get_by_email(self, email):
        usuario = User.query.filter_by(email=email).first()
        return usuario.serialize() if usuario else None

    def create(self, name, lastname, email, password, phone = None, photo=None):
        newUser = User(
            name=name,
            lastname=lastname,
            email=email,
            password=password,
            phone = phone,
            photo=photo        
        )
        db.session.add(newUser)
        db.session.commit()
        return newUser.serialize()

    def update(self, usuario_id, nombre_usuario, contraseña, nombre, correo, foto_base64=None):
        usuario = User.query.get(usuario_id)
        
        if usuario:
            usuario.nombre_usuario = nombre_usuario
            usuario.nombre = nombre
            usuario.correo = correo
            if contraseña:
                usuario.contraseña = contraseña

            if foto_base64:
                foto=self.guardar_imagen_local(foto_base64,usuario_id)
                usuario.foto = foto

            db.session.commit()

        return usuario.serialize() if usuario else None


    # def guardar_imagen_local(self, img_base64, usuario_id):
    #     # Decodificar la imagen base64
    #     starter = img_base64.find(',')
    #     img_data = img_base64[starter + 1:]
    #     #img_data = base64.b64decode(img_data)
    #     img_data = bytes(img_data, encoding="ascii")


    #     # Convertir los datos decodificados en un objeto Image
    #     #im = Image.open(BytesIO(img_data))
    #     im=Image.open(BytesIO(base64.b64decode(img_data))).convert('RGB')
        
    #     # Generar un nombre único para la imagen
    #     hash_object = hashlib.sha256(img_base64.encode())
    #     hash_value = hash_object.hexdigest()[:8]  # Tomar los primeros 8 caracteres del hash
    #     nombre_archivo = f"usuario_{usuario_id}_{hash_value}.png"
        
    #     # Guardar la imagen en el servidor
    #     ruta_archivo = os.path.join(current_app.config['IMAGENES_USUARIOS_CARPETA'], nombre_archivo)
    #     im.save(ruta_archivo)
        
    #     return nombre_archivo
    

    # def eliminar_imagen_usuario(self, usuario_id):
    #     usuario = User.query.filter_by(id=usuario_id).first()
    #     imagen_usuario=usuario.foto
    #     #print("IMAGEN USUARIO ", imagen_usuario)
    #     if not imagen_usuario:
    #         return 
        
    #     # Verificar si la imagen existe en el almacenamiento
    #     ruta_imagen = os.path.join(current_app.config['IMAGENES_USUARIOS_CARPETA'], imagen_usuario)
    #     if os.path.exists(ruta_imagen):
    #         #Eliminar la imagen del almacenamiento
    #         os.remove(ruta_imagen)
    #         usuario.foto=None
    #     else:
    #         return "La imagen no existe en el almacenamiento"

    def delete(self, usuario_id):
        usuario = User.query.get(usuario_id)
        if usuario:
            #db.session.delete(usuario)
            usuario.estado=False
            db.session.commit()

        return usuario.serialize() if usuario else None
    
    def deletePer(self, usuario_id):
        usuario = User.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            #usuario.estado=False
            db.session.commit()

        return usuario.serialize() if usuario else None
