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
    
    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        create_query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(create_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (item['price'], item['name'])) # The items in the tuple have to be in the order of their appearance in the query above

        connection.commit()
        connection.close()

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

        try:
            # Extracted the insertion logic
            self.insert_item(item)
        except:
            return {"message": "An error occurred while inserting the item"}, 500 # Internal server error

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
        request_data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': request_data['price']}

        if item is None:
            try:
                self.insert_item(updated_item)
            except:
                return {"message": "An error occurred while inserting the item"}, 500
        else:
            try:
                self.update_item(updated_item)
            except:
                return {"message": "An error occurred while updating the item"}, 500
        return updated_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        get_query = "SELECT * FROM items"
        results = cursor.execute(get_query)

        items = []
        for row in results:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {"items": items}