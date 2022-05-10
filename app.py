from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


# class Student(Resource):
#     def get(self, name):
#         return {'student': name}


# api.add_resource(Student, '/student/<string:name>') # example URL: http://localhost:5000/student/benneee

if __name__ == '__main__':
    app.run(debug=True)