import sqlite3
from db import db

class ItemModel(db.Model):
    
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(80))
    Price = db.Column(db.Float(precision = 2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    '''
    Since our model deals with all the internal working of the code and the resources
    deal with the external part of the code ie, the code with which user interacts,
    we are moving all our functions and methods which are internal into models folder.
    '''

    def __init__(self, Name, Price, store_id):
        self.Name = Name
        self.Price = Price
        self.store_id = store_id

    def json(self):
        return {"Name": self.Name, "Price": self.Price}
    
    @classmethod
    def find_by_name(cls, Name):

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = "SELECT * FROM Items WHERE name = ?"
        # result = cursor.execute(query, (Name, ))
        # # Returns first instance
        # row = result.fetchone()
        # connection.close()

        # if row: 
        #     return cls(*row)   

        '''
        Since we are now using SQLAlchemy we can use its inbuilt functions
        Chaining possible : filter_by().filter_by().filter_by().....
        Multiple args possible: filter_by(Name = Name, id = 1)
        Avoids having to manually establish connection cursor etc
        '''
        return ItemModel.query.filter_by(Name = Name).first()
    
    def save_to_db(self):

        # Previously was the insert method

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO Items VALUES (?, ?)"
        # cursor.execute(query, (self.Name, self.Price))

        # connection.commit()
        # connection.close()

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):

        # Previously was the update method

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # # Where clause crucial, else all data might get deleted
        # query = "UPDATE Items SET Price = ? WHERE Name = ?"
        # cursor.execute(query, (self.Price , self.Name))

        # connection.commit()
        # connection.close()

        db.session.delete(self)
        db.session.commit()