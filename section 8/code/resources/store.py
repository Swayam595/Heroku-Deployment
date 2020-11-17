import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store is not None:
            return {'Status' : 200, 'Message' : 'Store Found', 'Items' : store.json()}, 200
        return {'Status' : 404, 'Message' : 'Store Not Found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name) is not None:
            return {'Status' : 400, 'Message' : 'Bad Request', 'Details' : f'{name} Store already present in database'}, 400
        new_store = StoreModel(name)
        try:
            new_store.save_to_db()
            return {'Status' : 201, 'Message' : 'Store Added Successfully'}, 201
        except:
            return {'Status' : 500, 'Message' : 'Error: Failed to insert into the database.'}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'Status' : 400, 'Message' : 'Bad Request', 'Details' : f'{name} Store not present in database'}, 400
        store.delete_from_db()
        return {'Status' : 200, 'Message' : 'Item Deleted Successfully'}, 200

class StoreList(Resource):
    def get(self):
        rows = StoreModel.query.all()
        data = list(map(lambda x: x.json(), rows))
        return {'Store' : data}
