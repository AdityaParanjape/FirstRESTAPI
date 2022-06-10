from models.user import UserModel
import hmac

# users = [
#     {
#         'id' : 1,
#         'Username': 'Bob',
#         'Password': 'asdf'
#     }
# ]

# username_mapping = {
#     'bob' :     
#     {
#         'id' : 1,
#         'Username': 'Bob',
#         'Password': 'asdf'
#     }
# }

# userid_mapping = {
#     1 : 
#     {
#         'id' : 1,
#         'Username': 'Bob',
#         'Password': 'asdf'
#     }
# }


'''
Since we created a class for user, the above code is replaced by 
the following:
'''

# users = [
#     User(1, 'bob', 'asdf')
# ]

# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}


# def authenticate(username, password):

#     '''
#     .get is a dict method, similar to username_mapping['user']
#     Can pass None here, not possible in [] notation
#     '''
#     user = username_mapping.get(username, None)
    
#     if user and hmac.compare_digest(user.password, password):
#         return user

# '''
# 1)Payload is the contents of the JWT-token and that we will extract from the user_id 

# 2)Essentially a JWT contains a few different fields. One of those is 'identity', which 
# Flask-JWT populates with the user's id field.

# 3)When we send the JWT to any endpoint, Flask-JWT will get the 'id' value that is 
# encoded within the JWT, and use it to find our user data
# '''
# def identity(payload):

#     user_id = payload['identity']
#     return userid_mapping.get(user_id, None)


'''
Since we created a sqlite database, we no longer need a local database,
hence above code gets modified as follows:
'''

def authenticate(username, password):

    '''
    .get is a dict method, similar to username_mapping['user']
    Can pass None here, not possible in [] notation
    '''
    user = UserModel.find_by_username(username)
    
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):

    user_id = payload['identity']
    return UserModel.find_by_id(user_id)