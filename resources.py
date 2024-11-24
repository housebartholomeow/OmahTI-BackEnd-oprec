from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from schemas2 import UserSchema
from models2 import VideoModel
from models2 import db
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()


class UserRegistration(Resource):
    def __init__(self, user_service):
        self.user_service = user_service

    def post(self):
        data = request.get_json()
        print(data)

        user_schema = UserSchema()
        try:
            user_schema.load(data) 
        except ValidationError as err:
            return {"msg": "Invalid input data", "errors": err.messages}, 422
        
        user = self.user_service.register_user(data['username'], data['password'])
        if not user:
            return {'message': 'User already exists!'}, 400

        return {'message': 'User created successfully!'}, 201

class UserLogin(Resource):
    def __init__(self, user_service):
        self.user_service = user_service

    def post(self):
        data = request.get_json()

        token = self.user_service.authenticate_user(data['username'], data['password'])
        if token:
            return {'token': token}, 200

        return {'message': 'Invalid credentials'}, 401

class Video(Resource):
    def __init__(self, user_service):
        self.user_service = user_service

    @auth.login_required
    def get(self, video_id):
        video = VideoModel.query.get(video_id)
        if not video:
            return {'message': 'Video not found'}, 404
        
        return {
            'id': video.id,
            'name': video.name,
            'views': video.views,
            'likes': video.likes
        }, 200
    
    @auth.login_required
    def post(self):
        print(f"Headers: {request.headers}")
        print(f"Data: {request.get_json()}")
        data = request.get_json()

        if not data or not data.get('name') or not data.get('views') or not data.get('likes'):
            return {'message': 'Missing required fields'}, 400

        new_video = VideoModel(
            name=data['name'],
            views=data['views'],
            likes=data['likes']
        )
        db.session.add(new_video)
        db.session.commit()

        return {'message': 'Video uploaded successfully', 'video_id': new_video.id}, 201

    @auth.login_required
    def put(self, video_id):
    
        data = request.get_json()

        video = VideoModel.query.get(video_id)
        if not video:
            return {'message': 'Video not found'}, 404

        if 'name' in data:
            video.name = data['name']
        if 'views' in data:
            video.views = data['views']
        if 'likes' in data:
            video.likes = data['likes']

        db.session.commit()
        return {'message': 'Video updated successfully'}, 200

    @auth.login_required
    def delete(self, video_id):
       
        video = VideoModel.query.get(video_id)
        if not video:
            return {'message': 'Video not found'}, 404

        db.session.delete(video)
        db.session.commit()
        return {'message': 'Video deleted successfully'}, 200
