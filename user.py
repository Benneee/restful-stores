from flask_restful import Resource, reqparse
import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # We need methods that will interact with the database to find users
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_query, (username,))  # The parameters always have to be in a tuple
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


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

        user = User.find_by_username(data['username'])
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