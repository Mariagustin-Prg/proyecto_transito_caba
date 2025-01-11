# TransporteAPI.py
# Encode UTF-8
# Instancia del proyecto en la se hace conexión entre el API pública de Transportes de CABA y la 
# Base de Datos interna del proyecto


# Librerías necesarias para el script
from fastapi import APIRouter, HTTPException, status
import requests, datetime, json
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

api_client = load_dotenv("API_CLIENT")
api_secret = load_dotenv("API_SECRET")
security_code_env = load_dotenv("SECURITY_CODE")


# Crear una instancia de APIRouter
router = APIRouter(prefix= "/getData",
                #    tags= "getActualData"
                    responses= {status.HTTP_204: {"message": "No content"}}
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
async def enable_api(security_key: str = None):
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
    

# Función que obtiene la información de la API.
@router.get("/forecast_gtfs")
async def get_forecastGTFS() -> dict | HTTPException:
    '''
    Llama a la función forecastGTFS del API de transporte, específicamente de la sección de subtes.
    '''
    
    # La petición que se le hace al API
    response = requests.get(
                            f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}"

    )
    # Que intente retornar el diccionario del resultado de la petición.
    try:
        return response.json()
    
    # Si ocurre un error con el servidor.
    except HTTPException as e:
        raise HTTPException(status_code=503, detail="La solicitud no pudo realizarse con éxito")
    
    # Si la conversión a diccionario falla.
    except json.JSONDecodeError:
        raise HTTPException(status_code=204, detail= "El contenido de la petición no es válido.")
    




