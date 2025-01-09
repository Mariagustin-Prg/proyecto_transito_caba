# Repositorio: https://www.github.com/Mariagustin-Prg/proyecto-transito-caba
# Encode: UTF-8

# Import libraries
from fastapi import FastAPI, APIRouter
import requests, os
from dotenv import load_dotenv


# Create fastapi instances
app = FastAPI()


# Create main route
@app.get("/")
async def main():
    return {
        "message" : "Welcome to Proyecto-Transito-Caba"
    }


