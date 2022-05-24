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
            item.save_item_to_db()
        except:
            return {"message": "An error occurred while inserting the item"}, 500 # Internal server error

        return {
            "message": "Item added",
            "data": item.json()
        }, 201
        

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()

        return {'message': 'Item deleted'}


    # It is expected that this method is idempotent
    # i.e It must always do the same thing every time it is used.
    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, request_data['price'])
        else:
            item.price = request_data['price']
        item.save_item_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {"items": [item.json() for item in items]}