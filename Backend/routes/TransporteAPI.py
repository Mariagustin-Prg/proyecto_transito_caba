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
router = APIRouter(prefix= "/api-transporte",
                    tags= "API-Transporte"
                    # responses= {status.HTTP_204: {"message": "No content"}}
                   )


# -------------------------------------------------------------------


# Definir una función que haga una llamada al API para conocer si está disponible.
def status_forecastGTFS() -> int:
    '''
    Hace una llamada a la API y retorna el status en el que se encuentra.
    '''

    # La request necesaria para el API
    response = requests.get(
        f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}")

    # Retorna el status de la respuesta del API
    return response.status_code()



# -------------------------------------------------------------------


# Endpoint de la API, especialmente para la parte de test y debuggeo.
@router.get("/debug/enable_api/{security_key}")
async def enable_api(security_key: str | None = None):
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
    

# -------------------------------------------------------------------


# Función que obtiene la información de la API.
def get_forecastGTFS(id: str) -> dict | HTTPException:
    '''
    Llama a la función forecastGTFS del API de transporte, específicamente de la sección de subtes.
    '''
    
    # La petición que se le hace al API
    response = requests.get(
                            f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}"

    )
    # Que intente retornar el diccionario del resultado de la petición.
    try:
        info = response.json()
        info["id"] = id
        return info
    
    # Si ocurre un error con el servidor.
    except HTTPException as e:
        raise HTTPException(status_code=503, detail="La solicitud no pudo realizarse con éxito")
    
    # Si la conversión a diccionario falla.
    except json.JSONDecodeError:
        raise HTTPException(status_code=204, detail= "El contenido de la petición no es válido.")
    

# -------------------------------------------------------------------


# Una función que registre los llamados de get_forecastGTFS exitosos.
def new_call_forecast(id: str) -> None:
    '''
    Crea un registro en el json con la fecha y el status de la conexión con el API.
    '''
    # Obtiene el momento en que se hace llamada a esta función.
    now = datetime.datetime.now()

    # Se crea el registro 
    call = {
        "id": id,
        "time": now, # Con el momento en que se registra
        "status": status_forecastGTFS(), # El estado del API en el momento
    }

    # Que intente leer el json que ya existe:
    try:
        with open("../db/__calls__.json", "rt", encodign= "UTF-8") as file:
            data = json.loads(file)

    # En caso de no existir el json, que trabaje a partir del siguiente diccionario
    except FileNotFoundError:
        data = {
            "__name__": "__calls__.json",
            "calls": []
        }

    # Agrega el registro a la lista
    data["calls"].append(call)

    # Modifica el archivo json con la nueva información.
    with open("../db/__calls__.json", "wt", encoding="UTF-8") as file:
        json.dumb(data, file, indent=4)

    # Retorna un None para acabar con la ejecución de la función.
    return None


# -------------------------------------------------------------------


# La función que obtiene el último llamado exitoso al API.
def last_conection_forecast() -> dict | None | HTTPException:

    '''
    Verifica el último status_code 200.
    '''
    # Que lea el archivo json:
    try:
        with open("../db/__calls__.json", "rt", encoding="UTF-8") as file:
            data = json.loads(file)

    # Si no existe, retorna un None
    except FileNotFoundError:
        return None

    # Obtenemos el último registro exitoso
    calls = data["calls"]

    for d in calls:
        if d["status"] == 200:
            return d

    # En caso de no encontrar un registro, retorna un NotFound status.
    raise HTTPException(status_code=404, detail= "No se encontró la última conexión exitosa con el API")


# -------------------------------------------------------------------


# La función que crea los registros en los json de /db.
async def post_forecast() -> None:
    '''
    Postea en __data__ el resultado de ForecastGTFS del API y también guarda el llamado en __calls__
    '''
    # Crea un ID único con el método de datetime
    id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Para evitar errores declaramos un bloque Try.
    try:
        # Llamar a la función get_forecastGTFS().
        forecast_dicc = get_forecastGTFS(id= id)

    # En caso de errores en el funcionamiento interno de la función, trabaja este Except.
    except HTTPException | json.JSONDecodeError:
        # Retorna un InternalServerError con el siguiente detalle:
        raise HTTPException(status_code=500, detail= "El servidor no ha respondido a la solicitud")

    # Si la operación anterior funciona correctamente, continúa con el código.

    # Crea el registro en el json de __calls__ con la función new_call_forecast().
    new_call_forecast(id= id)

    # Con este fragmento modificamos el json de __data__.json
    with open("../db/__data__.json", encoding="UTF-8") as file:
        # Leemos el archivo
        data = json.loads(file)

        # Si la lista contenida en el json contiene 5 o más elementos.
        if len(data) >= 5:
            # Eliminamos el último elemento de la lista.
            data.pop()
            # Insertamos en la primer posición el diccionario con la respuesta del API.
            data.insert(0, forecast_dicc)
        
        # Si no, que inserte en la primer posición el diccionario.
        else:
            data.insert(0, forecast_dicc)

        # Que modifique el archivo con la nueva información.
        json.dumb(file, data, indent=4)


