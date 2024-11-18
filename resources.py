from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required
from services import UserService

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()

        user = user_service.register_user(data['username'], data['password'])
        if not user:
            return {'message': 'User already exists!'}, 400

        return {'message': 'User created successfully!'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()

        token = user_service.authenticate_user(data['username'], data['password'])
        if token:
            return {'token': token}, 200

        return {'message': 'Invalid credentials'}, 401

class Video(Resource):
    @jwt_required()
    def get(self, video_id):
        return {'message': 'Video fetched successfully!'}, 200
