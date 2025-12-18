# MỤC ĐÍCH CỦA category_models.py: Xử lý toàn bộ CRUD (Create, Read, Update, Delete) cho Category
# backend cho các nút: Add Category, Get Category, Delete Category, Update Category trên App

from .database_manager import DatabaseManager
from datetime import datetime
import config
import pandas as pd
from typing import Optional
from bson.objectid import ObjectId
from .transaction_model import TransactionModel #Đạt thêm budbet
from .budget_model import BudgetModel

collection_name = config.COLLECTIONS['category'] # Lay ten collection tu config

UNCATEGORIZED_NAME = "Uncategorized" #Topic 2


# Class xử lý CRUD cho CategoryModel
class CategoryModel:

    # Tạo instance DatabaseManager (singleton → 1 kết nối duy nhất)
    def __init__(self,user_id:Optional[str] = None):
        self.db_manager = DatabaseManager() # tạo instance DatabaseManager (instance = 1 đối tượng của Class)
        self.collection = self.db_manager.get_collection(collection_name=collection_name) # lấy collection từ DatabaseManager
    #    self.__initialize_default_categories__() # Chỉ gọi chạy khởi tạo lần đầu duy nhất, lần sau ko gọi nữa
        #init:
        self.user_id = user_id

    def set_user_id(self,user_id:str):
        self.user_id = ObjectId(user_id) if user_id is not None else None
        #after we have user_id, initialize their default category
        self.__initialize_user_default_categories__()
        # ensure system Uncategorized
        self.__ensure_system_categories__() #Topic 2

    # Khoi tao category mac dinh
    def __initialize_user_default_categories__(self):
        """Initialize categories if they dont exist"""

        if not self.user_id:
            return
        # EXPENSE
        for cate in config.DEFAULT_CATEGORIES_EXPENSE:
            #Calling by paras order
            #self.upsert_category("Expense",cate)
            #Calling by paras keywords
            self.upsert_category(category_type = "Expense", category_name =cate)
        # Lặp từng Key trong Expense (Shopping, Transportation, ...)
        # Mỗi 1 Key (Shopping, Transportation, ...) tạo 1 item với cấu trúc phía dưới, gọi là document (tuong đương row trong SQL)
        
        #    item = { 
        #        "category_type": "Expense",
        #        "name": cate,
        #        "created_at": datetime.now(),
        #        "last_modified": datetime.now() 
        #    }
        #    self.collection.update_one( # code này để update nếu có rồi, nếu tìm thấy → Mongo không chèn mới, chỉ bỏ qua
        #        {"name": cate, "category_type": "Expense"},
        #        {"$setOnInsert": item}, # → Nhờ "$setOnInsert" nên update cũng không ghi đè => Không bị trùng category.
        #        upsert=True #
        #    )
        #    print(f"Initialize {cate} success, category_type Expense!!")
        # Hàm này chủ yếu tạo header row cho từng category của EXPENSE (Shopping, Transportation, ...)

        ''' # Giải thích cách hoạt động của update_one
            update_one(filter, update) → Nếu tìm thấy document → UPDATE / Nếu không thấy → KHÔNG LÀM GÌ (KHÔNG INSERT)
            update_one(filter, update, upsert=True) → Nếu tìm được document → UPDATE Nếu KHÔNG tìm được → TẠO Document MỚI
            (Upsert = update + insert)
        '''

        ''' # Giải thích $setOnInsert
            $setOnInsert = chỉ chạy khi INSERT xảy ra → Còn nếu là UPDATE thì không chạy.
            Nếu document đã tồn tại → Upsert chọn UPDATE → $setOnInsert KHÔNG chạy → Không ghi đè dữ liệu cũ → Không tạo mới
            Nếu document không tồn tại → Upsert chọn INSERT → $setOnInsert: item sẽ tạo document mới với item
        '''

        ''' # Giải thích tại sao phải có upsert=True + $setOnInsert cùng lúc
            Nếu thiếu upsert=True, thì sẽ không có insert 
                → $setOnInsert KHÔNG BAO GIỜ chạy, vì phải có insert mới chạy dc
                → Dữ liệu MẶC ĐỊNH không bao giờ được chèn vào DB.

            # Hai cái này phải đi chung:
                upsert=True → Cho phép insert nếu cần
                $setOnInsert → Gán giá trị chỉ khi insert
        '''

        # INCOME
        for cate in config.DEFAULT_CATEGORIES_INCOME:
            #Calling by paras order
            #self.upsert_category("Income",cate)
            #Calling by paras keywords
            self.upsert_category(category_type = "Income", category_name= cate)
        #    item = { 
        #        "category_type": "Income",
        #        "name": cate,
        #        "created_at": datetime.now(),
        #        "last_modified": datetime.now() 
        #    }
        #    self.collection.update_one(
        #        {"name": cate, "category_type": "Income"},
        #        {"$setOnInsert": item},
        #        upsert=True #
        #    )

    # Nút thêm category
    
#    def add_category(self, category_type: str, category_name: str):

        # tạo dict item bằng cấu trúc phía dưới, đây là cấu trúc document phải theo mẫu __initialize_default_categories__ ở trên
        # mục đích tạo dict để dễ check tồn tại chưa, 
        # nhưng chỉ add trước 2 cột giá trị category_type, name, còn 2 cột time thì xử lý phía dưới
#        item_add = {
#            "category_type": category_type,
#            "name": category_name,
#        } 

        # Kiểm tra category name có tồn tại ko
#        item_existing = self.collection.find_one({"category_type": category_type, "name": category_name})

#        if item_existing: # Nếu tìm thấy category name (có tồn tại)          

#            item_add['last_modified'] = datetime.now() # thêm cót giá trị last_modified (vì đã có cột created_at rồi)
        
#        else: # Nếu không tìm thấy category name (chưa tạo)
#            item_add['created_at'] = datetime.now() # thêm cột giá trị created_at
#            item_add['last_modified'] = datetime.now() # thêm cót giá trị last_modified

#            self.collection.insert_one(item_add)
#        self.collection.update_one( # code này giống ở trên, tìm thấy thì chỉ update, không thì insert
#            {"name": category_name, "category_type": category_type},
#            {"$setOnInsert": item_add},
#            upsert=True
#        )
       
#Add category (update + Insert)
    def upsert_category(self,category_type:str, category_name:str):
        #define filter
        filter_ = {
            "type":category_type,
            "name":category_name,
            "user_id": self.user_id
        } 

        #define update_doc
        update_doc ={
            "$set":{
                "last_modified":datetime.now()
            },
            "$setOnInsert":{
                "created_at":datetime.now()
            }
        }

        result = self.collection.update_one(
            filter_,
            update_doc,
            upsert=True
        )
        return result.upserted_id

    #Topic 2:
    # Nút xóa category
    # def delete_category(self, category_type: str, category_name: str):
    #     result = self.collection.delete_one({"type": category_type, "name": category_name,"user_id": self.user_id}) # add user_id condition
    #     return result.deleted_count
    
    def delete_category(self, category_type: str, category_name: str):
        if category_name == UNCATEGORIZED_NAME:
            raise Exception("System category cannot be deleted")

        if not self.user_id:
            raise Exception("User not set")

        # 1️⃣ Ensure Uncategorized exists
        self.ensure_uncategorized_category(category_type)

        # 2️⃣ Move transactions → Uncategorized
        transaction_model = TransactionModel(self.user_id)
        transaction_model.collection.update_many(
            {
                "category": category_name,
                "type": category_type,
                "user_id": self.user_id
            },
            {
                "$set": {
                    "category": UNCATEGORIZED_NAME,
                    "last_modified": datetime.now()
                }
            }
        )

        # 3️⃣ DELETE related budgets (IMPORTANT – Budget Integrity)
        budget_model = BudgetModel(self.user_id)
        budget_model.collection.delete_many(
            {
                "category": category_name,
                "type": category_type,
                "user_id": self.user_id
            }
        )

        # 4️⃣ Delete category
        result = self.collection.delete_one(
            {
                "type": category_type,
                "name": category_name,
                "user_id": self.user_id
            }
        )

        return result.deleted_count > 0

    # Nút tim kiếm category theo category_type
    def get_category_by_type(self, category_type: str):
        #    result = self.collection.find({"type": category_type})
        #    result = list(result)
        #    return result
        #Hoac dung ben duoi
        return list(self.collection.find({"type":category_type,"user_id":self.user_id}).sort("created_at",-1)) # bang 3 dong tren
        
    def get_total_dataframe(self):
    #    data = list(self.collection.find({}, {"_id": 0}))  # bỏ _id cho sạch
        
        data = list(self.collection.find({"user_id":self.user_id}))
        df = pd.DataFrame(data)
        df.insert(0, "STT", range(1, len(df) + 1)) #Chèn cột stt
        return df  
    def get_total(self):
        result = self.collection.find({"user_id":self.user_id})
        result = list(result)
        return result

    # Đat: Thêm hàm cập nhật budget limit cho category
    def update_category_budget(self, category_name: str, new_limit: float) -> bool:
        """Update budget limit for a category."""
        try:
            filter_ = {"name": category_name, "user_id": self.user_id}
            update = {"$set": {"budget_limit": new_limit}}
            result = self.collection.update_one(filter_, update)
            return result.modified_count > 0
        except Exception as e:
            print("update_category_budget ERROR:", e)
            return False  

    def get_category_budget(self, category_name: str):
        """Return category: limit, spent, remaining, is_over."""
        month = datetime.now().month
        year = datetime.now().year

        category = self.collection.find_one({"name": category_name, "user_id": self.user_id})
        if not category:
            return None

        limit = category.get("budget_limit", 0)

        
        tmodel = TransactionModel(self.user_id)

        spent = tmodel.get_total_spent_by_category(category_name, month, year)
        remaining = limit - spent
        over = remaining < 0

        return {
            "limit": limit,
            "spent": spent,
            "remaining": remaining,
            "is_over": over
        }   

    # Topic 2: Ensure system category 'Uncategorized' exists for user
    def ensure_uncategorized_category(self, category_type: str):
        if not self.user_id:
            return

        self.collection.update_one(
            {
                "type": category_type,
                "name": UNCATEGORIZED_NAME,
                "user_id": self.user_id
            },
            {
                "$setOnInsert": {
                    "created_at": datetime.now(),
                    "system": True
                },
                "$set": {
                    "last_modified": datetime.now()
                }
            },
            upsert=True
        )

    def __ensure_system_categories__(self):
        for category_type in config.TRANSACTION_TYPES: #["Expense", "Income"]:
            self.ensure_uncategorized_category(category_type)
            
    # def update_category_name(
    #                         self,
    #                         category_type: str,
    #                         old_name: str,
    #                         new_name: str
    #                     ) -> bool:
    #     """
    #     Update category name and sync all related transactions
    #     """
    #     if not self.user_id:
    #         raise Exception("User not set")
    #     if old_name == UNCATEGORIZED_NAME:
    #         raise Exception("System category cannot be renamed")

    #     # 1️⃣ Update category name
    #     result = self.collection.update_one(
    #         {
    #             "type": category_type,
    #             "name": old_name,
    #             "user_id": self.user_id
    #         },
    #         {
    #             "$set": {
    #                 "name": new_name,
    #                 "last_modified": datetime.now()
    #             }
    #         }
    #     )

    #     if result.modified_count == 0:
    #         return False

    #     # 2️⃣ Sync transactions
    #     transaction_model = TransactionModel(self.user_id)
    #     transaction_model.reassign_category(
    #         old_category_name=old_name,
    #         new_category_name=new_name
    #     )

    #     return True

    def update_category_name(
                    self,
                    category_type: str,
                    old_name: str,
                    new_name: str
                ) -> bool:
        """
        Update category name and sync:
        - transactions
        - budgets
        """
        if not self.user_id:
            raise Exception("User not set")

        if old_name == UNCATEGORIZED_NAME:
            raise Exception("System category cannot be renamed")

        # ❌ Prevent duplicate category
        existed = self.collection.find_one({
            "type": category_type,
            "name": new_name,
            "user_id": self.user_id
        })
        if existed:
            raise Exception("Category name already exists")

        # 1️⃣ Update category
        result = self.collection.update_one(
            {
                "type": category_type,
                "name": old_name,
                "user_id": self.user_id
            },
            {
                "$set": {
                    "name": new_name,
                    "last_modified": datetime.now()
                }
            }
        )

        if result.modified_count == 0:
            return False

        # 2️⃣ Sync transactions
        transaction_model = TransactionModel(self.user_id)
        transaction_model.collection.update_many(
            {
                "category": old_name,
                "type": category_type,
                "user_id": self.user_id
            },
            {
                "$set": {
                    "category": new_name,
                    "last_modified": datetime.now()
                }
            }
        )

        # 3️⃣ Sync budgets 
        budget_model = BudgetModel(self.user_id)
        budget_model.reassign_category(
            category_type=category_type,
            old_category_name=old_name,
            new_category_name=new_name
        )

        return True


       
'''
if __name__== "__main__":
    print("Init category collection")
    cate = CategoryModel() 
    # gán cate chỉ dùng khi test file 1 mình, cate là 1 object (instance) của class CategoryModel, để xem class có lỗi hay không
    # gán cate để dễ debug (có thể mở Python REPL hay debug và kiểm tra) -> ví dụ lấy cate print(cate.collection) để kiểm tra
#   item = {
#       "category_type": "Expense",
#       "name": "Rent"
#   }

#   result = cate.add_category(category_type = "Expense", category_name="Rent")
'''
