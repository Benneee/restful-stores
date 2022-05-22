# This file will contain a few important functions
from werkzeug.security import safe_str_cmp
from user import User

# The mappings below gives us a way to easily find users and not have to iterate over the users list everytime
users = [
    User(1, 'bob', 'asdf')
]

username_mapping = { u.username: u for u in users }

user_id_mapping = { u.id: u for u in users }


# Authenticate Method
def authenticate(username, password):
    # We can add a default value here because we are using the 'get' method
    # user = username_mapping.get(username, None) 
    user = User.find_by_username(username) # Now using a class method that works with the DB
    if user and safe_str_cmp(user.password, password):
        return user

    
def identity(payload):
    user_id  = payload['identity']
    # return user_id_mapping.get(user_id, None)
    return User.find_by_id(user_id)
