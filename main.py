from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_bcrypt import Bcrypt
from services import UserService
from resources import UserRegistration, UserLogin, Video
from config import Config
from models import db


app = Flask(__name__)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)
bcrypt = Bcrypt(app)
limiter = Limiter(app)

app.config.from_object(Config)
user_service = UserService(db, bcrypt, jwt_manager)
api = Api(app)
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
    app.run(debug=True)
