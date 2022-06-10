# Importing necessary libraries
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# sqlite can be replaced by MySQL Oracle etc any other QL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'Adityaaaa'

# Creating instance of app API
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

'''
Creates an endpoint /auth and sends username and password to authenticate function
Authenticate function returns JWT Token if auth successful.
Then the JWT Token is sent to the next request which is to be made
If the next request can prove(uses identity function) it has same JWT Token, only then it is executed.
'''
jwt = JWT(app, authenticate, identity)

# Instead of adding decorator, this adds decorator for us
api.add_resource(Store, '/store/<string:Name>')

api.add_resource(StoreList, '/stores')

api.add_resource(Item, '/item/<string:Name>') 

api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/register')



# To avoid running app.run for imports, but only when we actually run through terminal
if __name__ == '__main__':

    db.init_app(app)
# debug = True gives simpler interface for error messages
    app.run(port = 5000, debug = True)