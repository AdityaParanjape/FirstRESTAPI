import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    '''
    Since parser will be reused, declare as Class entity
    Increases reusability, reduces errors
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('Price', 
    type = float, 
    required = True,
    help = "This field cannot be kept blank")

    parser.add_argument('store_id', 
    type  = int, 
    required = True,
    help = "Every item needs a store id")

    
    '''
    Creating get method which is routed to the get request created on Postman
    i.e on calling get request, this function is executed
    '''

    @jwt_required()
    def get(self, Name):
        
        # for i in Items:
        #     if i['Name'] == Name:
        #         return i       

        #  Instead of returning only None, this ensures data transferred as JSON format
        # return {'item' : None}, 404

        '''
        1)Instead of writing for loop use filter function with lambda
        2)filter function applies lambda on each item in items, returns filter object
        3)This filter object can then be used with methods like list or next for easy access  
        4)Next returns first instance in Items, if no instance or empty database, returns None
        '''
        # item = next(filter(lambda x: x["Name"] == Name, Items), None)
        # return {"Item" : item} , 200 if item else 404


        '''
        Since we are no longer using a local database, we will connect to sqlite
        '''
        item = ItemModel.find_by_name(Name)
        if item: 
            return item.json()

        return {'Message': f'An item with name {Name} does not exist!'}, 404

        
    def post(self, Name):

        '''
        If user creates a bad request, 400 status code
        That means user posts for item which already exists
        '''

        # Error first approach, removing error first, then performing operations
        # if next(filter(lambda x: x["Name"] == Name, Items), None):
        #     return {"Message": f"Item with name '{Name}' already exists"}, 400

        '''
        Since no longer using local database:
        '''

        if(ItemModel.find_by_name(Name)):
            return {"Message": f"Item with name '{Name}' already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(Name, **data)
        # Items.append(item)

        try:
            item.save_to_db()
        except:
            return {"Message" : "An error ocurred inserting into database"}, 500
        
        return item.json(), 201


    def delete(self, Name):

        # global Items
        # Remove item whose name matches
        # Items = list(filter(lambda x: x['Name'] != Name, Items))

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # # Where clause crucial, else all data might get deleted
        # query = "DELETE FROM Items WHERE Name = ?"
        # cursor.execute(query, (Name, ))

        # connection.commit()
        # connection.close()

        # return {"Message":"Item has been deleted"}

        '''
        Since now we are using SQLAlchemy, no need to manually establish connection and query
        '''
        item = ItemModel.find_by_name(Name)
        if item:
            item.delete_from_db()

        return {"Message":"Item has been deleted"}


    def put(self, Name):

        '''
        Filters the arguments and requests which are passed
        Here we have only defined Price, hence any other argument passed will be rejected
        Also checks data type
        '''

        # data = request.get_json()
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x["Name"] == Name, Items))

        item = ItemModel.find_by_name(Name)
        # updated_item = ItemModel(Name, data['Price'])

        if item:
            # item = {"Name": Name, "Price" : data["Price"]}
            # Items.append(item)
            # try:
            #     updated_item.insert()
            # except:
            #     return {"Message" : "An error ocurred inserting into database"}, 500

            item.Price = data["Price"]

        else:
            #.update is a dict method
            # item.update(data)
            # try:
            #     updated_item.update()
            # except:
            #     return {"Message" : "An error ocurred inserting into database"}, 500
            
            
            item = ItemModel(Name, **data)
        
        item.save_to_db()

        return item.json()


class ItemList(Resource):

    def get(self):
            
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # # Where clause crucial, else all data might get deleted
        # query = "SELECT * FROM Items"
        # result = cursor.execute(query)
        # items = []

        # for row in result:
        #     items.append({'Name':row[0], 'Price':row[1]})

        # connection.close()
            
        # return {'items': items}

        return {'items': [x.json() for x in ItemModel.query.all()]}