from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path= "./config/.env", encoding="UTF-8")

DB_USER = os.getenv("DB_USER")
DB_PWORD = os.getenv("DB_PWORD")


uri = f"mongodb+srv://mariagustinprog:{DB_PWORD}@transito-caba.gpoy4.mongodb.net/?retryWrites=true&w=majority&appName=Transito-Caba"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

