from myapp import db
from models.User.userrole import UserRole


class UserRoleRepository:
    def get_all(self):
        user_roles = UserRole.query.all()
        return [user_role.serialize() for user_role in user_roles]

    def get_by_user_id(self,user_id):
        user_roles = UserRole.query.filter_by(user_id = user_id).all()
        return [user_role.serialize() for user_role in user_roles]
    
    def get_by_role_id(self, role_id):
        user_roles = UserRole.query.filter_by(role_id = role_id).all()
        return [user_role.serialize() for user_role in user_roles]
  
    def create(self, user_id, role_id):
        user_role = UserRole(
            user_id = user_id,
            role_id = role_id
        )
        db.session.add(user_role)
        db.session.commit()
        return user_role.serialize()
    
     # Modifica un rol especifico
    def update(self, user_id, role_id):
        user = UserRole.query.filter_by(user_id = user_id, role_id = role_id).first()
        if user:
            user.role_id=role_id
            db.session.commit()
            return user.serialize()
        else:
            return None
        
    # Modifica todos los roles de un usuario
    def update(self, user_id, role_id):
        user = UserRole.query.filter_by(user_id = user_id).first()
        
        if user:
            user.role_id=role_id
            db.session.commit()
            return user.serialize()
        else:
            return None

