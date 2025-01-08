from fastapi import APIRouter, HTTPException
import requests, json
from Backend.routes.credentials import api_client, api_secret



router = APIRouter(prefix= "/getData",
                   tags= "getActualData"
                   )


def forecastGTFS():
    response = requests.get(
        f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}")

    if response.status_code == 200:
        try:
            return response.json()
        except:
            return {"error": "Ha habido un problema con la librería JSON."}
    else:
        HTTPException(404)
        return {}