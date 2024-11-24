from myapp import db
from datetime import datetime

class UserRole(db.Model):
    __tablename__='user_role'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key = True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),primary_key = True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones definidas en User y Role
    user_roles = db.relationship('User', back_populates='roles')
    role_users = db.relationship('Role', back_populates='users')

    def serialize(self):
        return {
            'user':self.user_roles.name if self.user_roles else None,
            'user_id': self.user_id,
            'role':self.role_users.name if self.role_users else None,
            'role_id': self.role_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
