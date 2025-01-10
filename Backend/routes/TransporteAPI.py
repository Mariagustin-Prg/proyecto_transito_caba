# TransporteAPI.py
# Created 09/01/25
# Instancia del proyecto en la se hace conexión entre el API pública de Transportes de CABA y la 
# Base de Datos interna del proyecto


# Librerías necesarias para el script
from fastapi import APIRouter, HTTPException
import requests, json
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

api_client = load_dotenv("API_CLIENT")
api_secret = load_dotenv("API_SECRET")
security_code_env = load_dotenv("SECURITY_CODE")


# Crear una instancia de APIRouter
router = APIRouter(prefix= "/getData",
                   tags= "getActualData"
                   )


# Definir una función que haga una llamada al API para conocer si está disponible.
def status_forecastGTFS():
    '''
    Hace una llamada a la API y retorna el status en el que se encuentra.
    '''

    # La request necesaria para el API
    response = requests.get(
        f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}")

    # Retorna el status de la respuesta del API
    return response.status_code()



# Endpoint de la API, especialmente para la parte de test y debuggeo.
@router.get("/debug/enable_api/{security_key}")
def enable_api(security_key: str):
    '''
    Endpoint para verificar la disponibilidad del API de transporte. \n
    Necesita una clave de seguridad, establecida en el entorno de desarrollo.
    '''
    # Verifica que se este ingresando la clave de seguridad correcta
    if security_key != security_code_env:
        return {
            "message": "La clave ingresada es inválida."
        }

    # Obtenemos el status del API
    status = status_forecastGTFS()

    
    if status == 200: # Si retorna 200, el API está activa y funcionando.
        return {
            "API": "Disponible",
            "status_code": status
        }
    else:             # el API tiene algún problema al realizar la solicitud.
        return {
            "API": "Error",
            "status_code": status
        }