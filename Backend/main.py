# Repositorio: https://www.github.com/Mariagustin-Prg/proyecto-transito-caba
# Encode: UTF-8

# Import libraries
from fastapi import FastAPI, APIRouter
import requests
from routes import TransporteAPI

# Create fastapi instances
app = FastAPI()

# Incluir los routers.
app.include_router(TransporteAPI.router)

# Create main route
@app.get("/")
async def main():
    return {
        "message" : "Welcome to Proyecto-Transito-Caba"
    }


