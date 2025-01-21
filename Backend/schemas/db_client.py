from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path= "./config/.env", encoding="UTF-8")

DB_USER = os.getenv("DB_USER")
DB_PWORD = os.getenv("DB_PWORD")

# Connection string
connection_string = "mongodb+srv://{DB_USER}:{DB_PWORD}@transito-caba.mongodb.net/"

# Create a MongoClient
clientDB = MongoClient(connection_string)

# Access a specific database
db = clientDB.get_database('transito_caba')

