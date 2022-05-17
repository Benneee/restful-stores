from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'benedict'
api = Api(app)


# JWT's addition here creates a new endpoint called "/auth" for the app
jwt = JWT(app, authenticate, identity)

items = []

# class Student(Resource):
#     def get(self, name):
#         return {'student': name}


# api.add_resource(Student, '/student/<string:name>') # example URL: http://localhost:5000/student/benneee


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None) 
        # "next" gives us the first item found by the filter function
        return {"data": item}, 200 if item else 404


    def post(self, name):
        parser = reqparse.RequestParser()

        parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank"
        )
        
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {"message": f"An item with {name} already exists."}, 400

        # request_data = request.get_json()
        request_data = parser.parse_args()
        item = { 
                "name": name,
                "price": request_data["price"]
        }
        items.append(item)
        return {
            "message": "Item added",
            "data": item
        }, 
        

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items)) 
        return { 'message': 'Item deleted' }


    # It is expected that this method is idempotent
    # i.e It must always do the same thing every time it is used.
    def put(self, name):
        parser = reqparse.RequestParser()
        
        # Define the arguments for the parser
        parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
        # request_data = request.get_json()

        # Instead of using request.get_json(), we use the parser's 
        # parse_args method which parses the request data and
        # sends along the fields that match the arguments requirements
        # above along with their value to request_data variable
        # If we add any other field in the JSON payload, they will
        # get erased and we won't see them in  request_data
        request_data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item


class ItemList(Resource):
    def get(self):
        return {"data": items}

api.add_resource(Item, '/item/<string:name>') # example URL: http://localhost:5000/item/benneee
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)