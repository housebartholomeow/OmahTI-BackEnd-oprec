from models import UserModel
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

class UserService:
    def __init__(self, db, bcrypt: Bcrypt, jwt_manager):
        self.db = db
        self.bcrypt = bcrypt
        self.jwt_manager = jwt_manager

    def register_user(self, username, password):
        if UserModel.query.filter_by(username=username).first():
            return None

        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        user = UserModel(username=username, password=hashed_password)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def authenticate_user(self, username, password):
        user = UserModel.query.filter_by(username=username).first()
        if user and self.bcrypt.check_password_hash(user.password, password):
            token = create_access_token(identity=user.id)
            return token
        return None
