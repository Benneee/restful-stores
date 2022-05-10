from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# class Student(Resource):
#     def get(self, name):
#         return {'student': name}


# api.add_resource(Student, '/student/<string:name>') # example URL: http://localhost:5000/student/benneee


class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return {"item": item}

        return {
            "message": 'Item not found!',
            "item": None
        }, 404


    def post(self, name):
        item = { "name": name, "price": 12.00 }
        items.append(item)
        return {
            "message": "Item added",
            "item": item
        }, 201

api.add_resource(Item, '/item/<string:name>') # example URL: http://localhost:5000/item/benneee

if __name__ == '__main__':
    app.run(debug=True)