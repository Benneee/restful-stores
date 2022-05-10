from flask import Flask, request
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
                return {"data": item}

        return {
            "message": 'Item not found!',
            "data": None
        }, 404


    def post(self, name):
        request_data = request.get_json()
        item = { 
                "name": name,
                "price": request_data["price"]
        }
        items.append(item)
        return {
            "message": "Item added",
            "data": item
        }, 201


class ItemList(Resource):
    def get(self):
        return {"data": items}

api.add_resource(Item, '/item/<string:name>') # example URL: http://localhost:5000/item/benneee
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)