from .database_manager import DatabaseManager
from datetime import datetime
import config
from bson.objectid import ObjectId

collection_name = config.COLLECTIONS['user'] # Lay ten collection tu config

class UserModel:

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name = collection_name)

    def create_user(self, email:str) -> str:
        """create new user"""
        user = {
            "email": email,
            "created_at": datetime.now(),
            "last_modified": datetime.now(),
            "is_activate": True
        }

        result = self.collection.insert_one(user)
        return str(result.inserted_id)


    def login(self, email: str) -> str:
        #check user exists (use find_one)
        user = self.collection.find_one({'email':email})

        # case1:user not exists:
        #create:call create_user(email)
        if not user:
            return self.create_user(email)


        #case 2: user exist but deactivate
        # raise error
        if user.get("is_activate") is not True:
            raise ValueError("This account is deactivated! Please connect to CS")

        #All checking passed
        return str(user.get("_id"))    

    def deactivate_user(self,user_id:str) -> bool:
        #find and update
        user = self.collection.find_one({
            "_id": ObjectId(user_id),
            "is_activate": True
        })

        #Case: not exist user
        if not user:
            raise ValueError("User not found")

        # user is validate and ready to deactivate -> update them    
        result = self.collection.update_one(
            { "_id": ObjectId(user_id)},
            {"$set": {"is_activate": False}}
            
        )    
        return result.modified_count >0
