# TransporteAPI.py
# Encode UTF-8
# Instancia del proyecto en la se hace conexión entre el API pública de Transportes de CABA y la 
# Base de Datos interna del proyecto


# Librerías necesarias para el script
from fastapi import APIRouter, HTTPException, status
import requests, datetime, json, os
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv(dotenv_path= "../config/.env", encoding='UTF-8')

api_client = os.getenv("api_client")
api_secret = os.getenv("api_secret")
security_code_env = os.getenv("SECURITY_CODE")


# Crear una instancia de APIRouter
router = APIRouter(prefix= "/api-transporte",
                    tags= ["API-Transporte"]
                    # responses= {status.HTTP_204: {"message": "No content"}}
                   )


# -------------------------------------------------------------------

@router.get("/")
def main():
    return {
        "status": "success"
    }


# Definir una función que haga una llamada al API para conocer si está disponible.
# @router.get("/status")
def status_forecastGTFS():
    '''
    Hace una llamada a la API y retorna el status en el que se encuentra.
    '''

    # La request necesaria para el API
    response = requests.get(
        f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={api_client}&client_secret={api_secret}")

    # Retorna el status de la respuesta del API
    try:    
        return {
            "status_code": response.status_code}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=503, detail={"message": "La solicitud no pudo realizarse con éxito"})



# -------------------------------------------------------------------


# Endpoint de la API, especialmente para la parte de test y debuggeo.
@router.get("/debug/enable_api")
async def enable_api(security_key: str | None = None):
    '''
    Endpoint para verificar la disponibilidad del API de transporte. \n
    Necesita una clave de seguridad, establecida en el entorno de desarrollo.
    '''
    # Verifica que se este ingresando la clave de seguridad correcta
    if security_key != security_code_env:
        raise HTTPException(status_code=401, detail= {
            "message": "La clave ingresada es inválida."
        })

    # Obtenemos el status del API
    status = status_forecastGTFS()

    
    if status['status_code'] == 200: # Si retorna 200, el API está activa y funcionando.
        return {
            "API": "Disponible",
            "status_code": status['status_code']
        }
    else:             # el API tiene algún problema al realizar la solicitud.
        return {
            "API": "Error",
            "status_code": status['status_code']
        }
    

# -------------------------------------------------------------------


# Función que obtiene la información de la API.
@router.get("/get-forecastgtfs")
def get_forecastGTFS(id: str):
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
@router.post("/call-forecast")
def new_call_forecast(id: str):
    '''
    Crea un registro en el json con la fecha y el status de la conexión con el API.
    '''
    # Obtiene el momento en que se hace llamada a esta función.
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    # Se crea el registro 
    call = {
        "id": id,
        "time": now, # Con el momento en que se registra
        "status": status_forecastGTFS(), # El estado del API en el momento
    }

    # Que intente leer el json que ya existe:
    try:
        with open(".\db\__calls__.json", "rt", encoding= "UTF-8") as file:
            data = json.load(file)

    # En caso de no existir el json, que trabaje a partir del siguiente diccionario
    except FileNotFoundError:
        data = {
            "__name__": "__calls__.json",
            "calls": []
        }

    # Agrega el registro a la lista
    data["calls"].append(call)

    # Modifica el archivo json con la nueva información.
    with open(".\db\__calls__.json", "wt", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)

    # Retorna un json para acabar con la ejecución de la función.
    return {'detail': 'Succesfull post.', 'data': data}


# -------------------------------------------------------------------


# La función que obtiene el último llamado exitoso al API.
@router.get("/last-conection")
def last_conection_forecast():

    '''
    Verifica el último status_code 200.
    '''
    # Que lea el archivo json:
    try:
        with open(".\db\__calls__.json", "rt", encoding="UTF-8") as file:
            data = json.load(file)

    # Si no existe, retorna un None
    except FileNotFoundError:
        raise HTTPException(status_code= 404, detail="No se encontró el archivo.")

    # Obtenemos el último registro exitoso
    calls = data["calls"][::-1]

    for d in calls:
        if d["status"]['status_code'] == 200:
            return d

    # En caso de no encontrar un registro, retorna un NotFound status.
    raise HTTPException(status_code=404, detail= "No se encontró la última conexión exitosa con el API")


# -------------------------------------------------------------------


# La función que crea los registros en los json de /db.
@router.post("/post-forecast")
async def post_forecast():
    '''
    Postea en __data__ el resultado de ForecastGTFS del API y también guarda el llamado en __calls__
    '''
    # Crea un ID único con el método de datetime
    id = datetime.datetime.now().strftime("<%Y-%m-%d>|<%H:%M:%S>")

    # Para evitar errores declaramos un bloque Try.
    try:
        # Llamar a la función get_forecastGTFS().
        forecast_dicc = get_forecastGTFS(id= id)

    # En caso de errores en el funcionamiento interno de la función, trabaja este Except.
    except HTTPException:
        # Retorna un InternalServerError con el siguiente detalle:
        raise HTTPException(status_code=500, detail= "El servidor no ha respondido a la solicitud")

    except json.JSONDecodeError:
        raise HTTPException(status_code= 204, detail= "No content available")

    # Si la operación anterior funciona correctamente, continúa con el código.

    # Crea el registro en el json de __calls__ con la función new_call_forecast().
    new_call_forecast(id= id)

    # Con este fragmento modificamos el json de __data__.json
    with open(".\db\__data__.json", encoding="UTF-8") as file:
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


    return {"request": "post", "status": "success"}
