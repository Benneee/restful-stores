import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    
    # Define the arguments for the parser
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() # Since find_by_name now returns an object and not a dictionary anymore
        return {"message": "Item not found"}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with {name} already exists."}, 400

        # request_data = request.get_json()
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'])

        try:
            # Extracted the insertion logic
            item.insert_item()
        except:
            return {"message": "An error occurred while inserting the item"}, 500 # Internal server error

        return {
            "message": "Item added",
            "data": item.json()
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

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])

        if item is None:
            try:
                updated_item.insert_item()
            except:
                return {"message": "An error occurred while inserting the item"}, 500
        else:
            try:
                updated_item.update_item()
            except:
                return {"message": "An error occurred while updating the item"}, 500
        return updated_item.json()


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