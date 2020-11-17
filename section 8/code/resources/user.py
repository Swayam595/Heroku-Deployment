import sqlite3
from flask_restful import Resource, reqparse
from flask import jsonify
from models.user import UserModel

class UserList(Resource):
    def get(self):
        rows = UserModel.get_all()
        data = list(map(lambda x:{'ID':x.id, 'Username':x.username, 'Password':x.password}, rows))
        return jsonify({'Users': data})

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username field cannot be left blank.')
    parser.add_argument('password', type=str, required=True, help='Password field cannot be left blank.')

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']) is not None:
            return {'Status': 400, 'Message': 'User Already Exists'}, 400
        new_user = UserModel(data['username'], data['password'])
        try:
            new_user.save_to_db()
            return {'Status': 201, 'Message': 'User Create Successfully', 'New User': new_user.username}, 201
        except:
            return {'Status' : 500, 'Message' : 'Error: Failed to insert into the database.'}, 500
        return {'Status': 201, 'Message': 'User Create Successfully'}, 201
