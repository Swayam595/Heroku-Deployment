from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authentication, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret_key'
api = Api(app)

jwt = JWT(app, authentication, identity)   # JWT creates a new end point i.e. /auth


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
