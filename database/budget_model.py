from datetime import datetime
from typing import Optional, List, Dict, Any
from bson.objectid import ObjectId
from .database_manager import DatabaseManager
import config
from utils import handler_datetime


# Collection name from config
collection_name = config.COLLECTIONS['budget']

class BudgetModel:
    def __init__(self, user_id: Optional[str] = None):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name)
        self.user_id = ObjectId(user_id) if user_id else None


    def set_user_id(self, user_id: Optional[str]):
        self.user_id = ObjectId(user_id) if user_id else None

    # ----------------------------------------
    # Create new budget
    # ----------------------------------------

    def create_budget(
                    self,
                    category: str,
                    type_: str,
                    limit_amount: float,
                    month: int,
                    year: int,
                    budget_date:datetime,
                    description: str = ""
                    ) -> Optional[str]:

        if not isinstance(budget_date, datetime):
            budget_date = handler_datetime(budget_date)

        budget_doc = {
        "user_id": self.user_id,
        "category": category,
        "type": type_, # Expense / Income
        "limit_amount": limit_amount,
        "month": month,
        "year": year,
        "date": budget_date,
        "description": description,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
        }
        try:
            result = self.collection.insert_one(budget_doc)
            return str(result.inserted_id)
        except Exception as e:
            print("Error creating budget:", e)
            return None

    # ----------------------------------------
    # Get all budgets for a user
    # ----------------------------------------    
    def get_all_budgets(self, month: Optional[int] = None, year: Optional[int] = None) -> List[Dict[str, Any]]:
        query = {"user_id": self.user_id}

        if month:
            query["month"] = month
        if year:
            query["year"] = year

        cursor = self.collection.find(query).sort("created_at", -1)
        return list(cursor)

    # ----------------------------------------
    # Get a budget by ID
    # ----------------------------------------

    def get_budget_by_id(self, budget_id: str) -> Optional[Dict[str, Any]]:
        try:
            return self.collection.find_one({
            "_id": ObjectId(budget_id),
            "user_id": self.user_id
            })
        except Exception as e:
            print("Error fetching budget:", e)
            return None

        # ----------------------------------------
        # Update budget
        # ----------------------------------------

    def update_budget(
                        self,
                        budget_id: str,
                        **kwargs
                        )-> bool:
        try:
            if "updated_at" not in kwargs:
                kwargs["updated_at"] = datetime.now()


            result = self.collection.update_one(
            {"_id": ObjectId(budget_id), "user_id": self.user_id},
            {"$set": kwargs}
            )
            return result.modified_count > 0
        except Exception as e:
            print("Error updating budget:", e)
            return False

        # ----------------------------------------
        # Delete budget
        # ----------------------------------------

    def delete_budget(self, budget_id: str) -> bool:
        try:
            result = self.collection.delete_one({
                                                "_id": ObjectId(budget_id),
                                                "user_id": self.user_id
                                                })
            return result.deleted_count > 0
        except Exception as e:
            print("Error deleting budget:", e)
            return False

        # ----------------------------------------
        # Calculate total spent for a category in a specific month
        # ----------------------------------------

    def calculate_spent(self, transaction_model, category: str, month: int, year: int) -> float:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        transactions = transaction_model.get_transactions({
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "transaction_type": "Expense"
            })

        return sum(t.get("amount", 0) for t in transactions)

        # ----------------------------------------
        # Helper: Get budget with spent + remaining
        # ----------------------------------------

    def get_budget_with_status(self, transaction_model, month: int, year: int) -> List[Dict[str, Any]]:
        budgets = self.get_budgets(month, year)
        enriched = []

        for b in budgets:
            spent = self.calculate_spent(transaction_model, b["category"], b["month"], b["year"])
            remaining = b["limit_amount"] - spent
            over = spent > b["limit_amount"]

            enriched.append({
                **b,
                "spent": spent,
                "remaining": remaining,
                "is_over": over
                })
        return enriched

    def reassign_category(
            self,
            category_type: str,
            old_category_name: str,
            new_category_name: str
        ):
        """
        Update all budgets when category name is renamed
        """
        return self.collection.update_many(
            {
                "category": old_category_name,
                "type": category_type,
                "user_id": self.user_id
            },
            {
                "$set": {
                    "category": new_category_name,
                    "updated_at": datetime.now()
                }
            }
        )    