from pymongo import MongoClient

client = MongoClient("mongodb+srv://zhannakiselova:QHrX7et6MhUDSaF@cluster0.qotqw.mongodb.net")

db = client.test
print(db.list_collection_names())

