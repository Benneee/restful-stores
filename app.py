from flask_restful import Api
from flask import Flask
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.secret_key = 'benedict'
api = Api(app)


# JWT's addition here creates a new endpoint called "/auth" for the app
jwt = JWT(app, authenticate, identity)

# class Student(Resource):
#     def get(self, name):
#         return {'student': name}


# api.add_resource(Student, '/student/<string:name>') # example URL: http://localhost:5000/student/benneee

api.add_resource(Item, '/item/<string:name>') # example URL: http://localhost:5000/item/benneee
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)