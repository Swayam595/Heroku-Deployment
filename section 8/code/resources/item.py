import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=str, required=True, help='This field cannot be left blank.')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item is not None:
            return {'Status' : 200, 'Message' : 'Item Found', 'Item' : item.json()}, 200
        return {'Status' : 404, 'Message' : 'Item Not Found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {'Status' : 400, 'Message' : 'Bad Request', 'Details' : f'{name} Item already present in database'}, 400
        request_data = Item.parser.parse_args()
        new_item = ItemModel(name, request_data['price'])
        try:
            new_item.save_to_db()
            return {'Status' : 201, 'Message' : 'Item Added Successfully', 'Item Details' : new_item.json()}, 201
        except:
            return {'Status' : 500, 'Message' : 'Error: Failed to insert into the database.'}, 500

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'Status' : 400, 'Message' : 'Bad Request', 'Details' : f'{name} Item not present in database'}, 400
        item.delete_from_db()
        return {'Status' : 200, 'Message' : 'Item Deleted Successfully'}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        try:
            item.save_to_db()
            return {'Status' : 200, 'Message' : 'Item Updated Successfully', 'Item Details' : updated_item.json()}, 200
        except:
            return {'Status' : 500, 'Message' : f'Error: Failed to update {name} price in the database.'}, 500

class ItemList(Resource):
    def get(self):
        rows = ItemModel.get_all()
        data = list(map(lambda x: {'name': x.name, 'price': x.price}, rows))
        return jsonify({'Items' : data})
