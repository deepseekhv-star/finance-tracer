from database.database_manager import DatabaseManager
from database.transaction_model import TransactionModel
from datetime import datetime,date
import config

if __name__=="__main__":
    #Test add transaction ##########################
    #init model
    #transaction_model = TransactionModel()
    #Define paras
    #transaction_type = "Income"
    #category = "Shopping"
    #amount = 234
    #transaction_date = date.today()

    #new_transaction = transaction_model.add_new_transaction(
    #    transaction_type= transaction_type,
    #    category = category,
    #    amount = amount,
    #    transaction_date=transaction_date,
    #    description =None

    #)
    #print(f"New transaction created !! {new_transaction}")
    #####################################################
    transaction_model = TransactionModel()
    delete_transaction = transaction_model.delete_transaction(transaction_id="6925af27774f498d7fd72b9d")
    print(f"Delete transaction created !! {delete_transaction}")