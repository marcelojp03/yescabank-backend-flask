
from myapp import db
from models.Role.role import Role

class RoleRepository:
    def get_all(self):
        roles = Role.query.all()
        return [rol.serialize() for rol in roles]

    def get_by_id(self, rol_id):
        role = Role.query.get(rol_id)
        return role.serialize() if role else None

    def create(self, name, description = None):
        new_role = Role(
            name = name,
            description = description
        )
        db.session.add(new_role)
        db.session.commit()
        return new_role.serialize()

    def update(self, id, name, description = None):
        role = Role.query.get(id)
        if role:
            role.name = name
            role.description = description
            db.session.commit()

        return role.serialize() if role else None

    def delete(self, rol_id):
        role = Role.query.get(rol_id)
        if role:
            #db.session.delete(rol)
            role.status = False
            db.session.commit()

        return role.serialize() if role else None
    
    def deletePer(self, rol_id):
        rol = Role.query.get(rol_id)
        if rol:
            db.session.delete(rol)
            #rol.estado=False
            db.session.commit()

        return rol.serialize() if rol else None

    # def get_menu_for_user(self,user_id):
    #     """
    #     Retorna un menú dinámico basado en los roles del usuario.
    #     """
    #     idf = "get_menu_for_user::"
    #     respuesta = {
    #         'user_id': user_id,
    #         'menu': [],
    #         'codigo': 1,
    #         'mensaje': 'OK'
    #     }

    #     try:
    #         engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    #         with engine.connect() as connection:
    #             # 1. Obtener los roles del usuario
    #             sql_roles = f"""
    #                 SELECT role_id FROM user_role WHERE user_id = {user_id}
    #             """
    #             result_roles = connection.execute(text(sql_roles))
    #             roles_ids = [row.role_id for row in result_roles]
    #             if not roles_ids:
    #                 print(idf + "None::Usuario no tiene roles")
    #                 respuesta['mensaje'] = idf + f"El usuario {user_id} no tiene asignado ningún rol"
    #                 raise Exception(idf + f"El usuario {user_id} no tiene asignado ningún rol")

    #             # Convertir la lista de roles en una cadena separada por comas para la consulta SQL
    #             roles_ids_str = ', '.join(map(str, roles_ids))

    #             # 2. Obtener los recursos principales y subrecursos asociados a los roles
    #             sql_recursos = f"""
    #                 SELECT DISTINCT r.id as resource_id, r.name as resource_name, r.description as resource_description,
    #                     sr.id as subresource_id, sr.name as subresource_name, sr.description as subresource_description, sr.url
    #                 FROM role_resource rr
    #                 LEFT JOIN resource r ON rr.resource_id = r.id
    #                 LEFT JOIN subresource sr ON rr.subresource_id = sr.id
    #                 WHERE rr.role_id IN ({roles_ids_str})
    #                 ORDER BY r.id, sr.id
    #             """
    #             result_recursos = connection.execute(text(sql_recursos))

    #             # Construir el menú jerárquico
    #             menu = {}
    #             for row in result_recursos:
    #                 resource_id = row.resource_id
    #                 subresource = {
    #                     'id': row.subresource_id,
    #                     'name': row.subresource_name,
    #                     'description': row.subresource_description,
    #                     'url': row.url
    #                 }

    #                 if resource_id not in menu:
    #                     menu[resource_id] = {
    #                         'id': resource_id,
    #                         'name': row.resource_name,
    #                         'description': row.resource_description,
    #                         'subresources': []
    #                     }
                    
    #                 if subresource['id']:
    #                     menu[resource_id]['subresources'].append(subresource)

    #             respuesta['menu'] = list(menu.values())
    #             respuesta['codigo'] = 0

    #     except Exception as ex:
    #         print(idf + "Exception:" + str(ex))
    #     finally:
    #         print("finally")

    #     return respuesta
    
