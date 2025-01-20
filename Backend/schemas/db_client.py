from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DB_USER = load_dotenv("DB_USER")
DB_PWORD = load_dotenv("DB_PWORD")

# Connection string
connection_string = "mongodb+srv://{DB_USER}:{DB_PWORD}@transito-caba.mongodb.net/"

# Create a MongoClient
clientDB = MongoClient(connection_string)

# Access a specific database
db = clientDB.get_database('transito_caba')

