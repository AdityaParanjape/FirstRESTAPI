from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    
    def get(self, Name):

        store = StoreModel.find_by_name(Name)
        if store:
            return store.json()

        return {"Message" : "Store not found"} , 404
    
    def post(self, Name):

        if StoreModel.find_by_name(Name):
            return {"Message" : f"A store with name {Name} already exists!!"}

        store = StoreModel(Name)

        try:
            store.save_to_db()

        except:
            return {"Message": "An error occurred while creating the store"}, 500

        return store.json(), 201

    def delete(self, Name):
        store = StoreModel.find_by_name(Name)
        if store:
            store.delete_from_db()

        return {"Message" : "Store deleted!"}
        

class StoreList(Resource):
    
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}