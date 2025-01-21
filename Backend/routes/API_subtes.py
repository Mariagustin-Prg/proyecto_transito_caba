from fastapi import APIRouter, HTTPException, status
# from schemas.db_client import clientDB
from dotenv import load_dotenv

load_dotenv()

# Crear una instancia de APIRouter
router = APIRouter(prefix="/subtes",
                    tags=["API-Subtes"]
                    )

@router.get('/')
def main():
    return {
        "message": "Welcome to the Subtes API"
    }