import sqlite3

from sqlalchemy import PrimaryKeyConstraint
from resources.item import Item
from db import db

# Since this class does not use resources, removed from resources folder and added here.

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


    '''
    Creating a class method to get user from sqlite3 instead of using a
    local database.
    '''

    def save_to_db(self):
        db.session.add(self)      
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE username = ?"

        # # Pass query plus TUPLE to cursor, hence (field, ) a must for single field
        # result = cursor.execute(query, (username, ))

        # row = result.fetchone()
        # if row:
        #     # user = cls(row[0], row[1], row[2])
        #     # Instead of passing individual args, pass as *args, posn args
        #     user = cls(*row)
        # else:
        #     user = None

        # connection.close()
        # return user

        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls, _id):

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE id = ?"
        # result = cursor.execute(query, (_id, ))
        # row = result.fetchone()
        # if row:
        #     # user = cls(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None

        # connection.close()
        # return user

        return cls.query.filter_by(id = _id).first()