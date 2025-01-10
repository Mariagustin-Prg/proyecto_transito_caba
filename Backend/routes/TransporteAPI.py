from fastapi import APIRouter, HTTPException
import requests, json
from dotenv import load_dotenv

load_dotenv()


api_client = load_dotenv("API_CLIENT")
api_secret = load_dotenv("API_SECRET")

router = APIRouter(prefix= "/getData",
                   tags= "getActualData"
                   )


def forecastGTFS():
    response = requests.get(
        f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}")

    return None