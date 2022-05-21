import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    
    # Define the arguments for the parser
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        get_query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(get_query, (name,))
        row = results.fetchone()

        connection.close()

        if row:
            return {'item': { 'name': row[0], 'price': row[1] }}

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404


    def post(self, name):
        if self.find_by_name(name):
            return {"message": f"An item with {name} already exists."}, 400

        # request_data = request.get_json()
        request_data = Item.parser.parse_args()
        item = { 
                "name": name,
                "price": request_data["price"]
        }
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        create_query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(create_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return {
            "message": "Item added",
            "data": item
        }, 201
        

    def delete(self, name):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM items WHERE name=?"
        cursor.execute(delete_query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}


    # It is expected that this method is idempotent
    # i.e It must always do the same thing every time it is used.
    def put(self, name):
        # request_data = request.get_json()

        # Instead of using request.get_json(), we use the parser's 
        # parse_args method which parses the request data and
        # sends along the fields that match the arguments requirements
        # above along with their value to request_data variable
        # If we add any other field in the JSON payload, they will
        # get erased and we won't see them in  request_data
        request_data = Item.parser.parse_args()

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