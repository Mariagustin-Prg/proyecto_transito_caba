from fastapi import APIRouter, HTTPException
import requests, json, os
from dotenv import load_dotenv


load_dotenv()
api_client = os.getenv("API_CLIENT")
api_secret  = os.getenv("API_SECRET")

router = APIRouter(prefix= "/getData",
                   tags= "getActualData"
                   )


def forecastGTFS():
    response = requests.get(
        f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}")

    return None