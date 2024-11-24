from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_bcrypt import Bcrypt
from services2 import UserService
from resources2 import UserRegistration, UserLogin, Video
from config2 import Config
from models2 import db
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)
jwt_manager = JWTManager(app)
bcrypt = Bcrypt(app)
limiter = Limiter(app)

user_service = UserService(db, bcrypt, jwt_manager)
api = Api(app)
api.add_resource(UserRegistration, '/register', resource_class_args=[user_service])
api.add_resource(UserLogin, '/login', resource_class_args=[user_service])
api.add_resource(Video, '/video', '/video/<int:video_id>', resource_class_args=[user_service])

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = user_service.get_user_by_username(username)
    if not user:
        print(f"Authentication failed: User '{username}' not found.")
        return None

    if not bcrypt.check_password_hash(user.password, password):
        print(f"Authentication failed: Incorrect password for user '{username}'.")
        return None

    print(f"Authentication successful for user '{username}'.")
    return username
    

@app.route('/protected')
@auth.login_required
def protected():
    return "This is a protected route, you are authenticated."

if __name__ == "__main__":
    app.run(debug=True)
