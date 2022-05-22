from flask_restful import Resource, reqparse
import sqlite3

from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user:
            return {'message': 'A user with that username already exists, pick another'}, 400

        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        # NULL for id since we know it auto-increments in the DB
        create_user_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(create_user_query, (data['username'], data['password'], ))
        
        connection.commit()
        connection.close()

        return {'message': 'User created successfully'}, 201