from ..models import (
    linea_subte,
    estacion_subte,
    movil_subte
)
# from Backend.schemas.db_client import clientDB
import json, time, datetime


def create_LineaSubte(dict_linea: dict) -> linea_subte.LineaSubte:
    '''
    method:
    create_LineaSubte(dict_linea):
        Crea un objeto LineaSubte.

    args:
        `dict_linea`: Diccionario con los datos de la línea.

    return:
        Objeto `LineaSubte`.
    '''
    try:
        linea_create = linea_subte.LineaSubte(
            nombre_linea= dict_linea['nombre_linea'],
            codigo= dict_linea['codigo'],
            direccion= bool(dict_linea['direccion']),
            actividad= bool(dict_linea['actividad']),
        )

    except KeyError as e:
        raise KeyError(f"Error en la clave: {e}")
    
    return linea_create




def dict_to_EstacionObject(dict_info: dict, linea: linea_subte.LineaSubte) -> estacion_subte.EstacionSubte:
    '''
    method:
    dict_to_EstacionObject(dict_linea):
        Convierte un diccionario en un objeto EstacionSubte.

    args:
        `dict_linea`: Diccionario con los datos de la Estacion.

    return:
        Objeto `EstacionSubte`.
    '''
    try:
        if dict_info["anden_central"] == -1:
            dict_info["anden_central"] = False
            special_case = True

        else: 
            special_case = False

        estacion_create = estacion_subte.EstacionSubte(
            nombre_estacion= dict_info['nombre_estacion'],
            latitud= dict_info['latitud'],
            longitud= dict_info['longitud'],
            linea_principal= linea,
            conexion= bool(dict_info['conexion']),
            terminal= bool(dict_info['terminal']),
            actividad= bool(dict_info["actividad"]),
            anden_central= bool(dict_info["anden_central"]),
        )

        if special_case:
            estacion_create.special_case = True
    
        return estacion_create
    
    except KeyError as e:
        raise KeyError(f"Error en la clave: {e}")
    

def set_list_stations(lista_estaciones: list, linea: linea_subte.LineaSubte):
    '''
    method:
    set_list_stations(lista_estaciones):
        Establece las estaciones de la línea.

    args:
        `lista_estaciones`: Lista de diccionarios con los datos de las estaciones.
        `linea`: Objeto LineaSubte.

    return:
        None.
    '''
    if not isinstance(lista_estaciones, list):
        raise TypeError("El argumento debe ser una lista.")
    
    for index, estacion in enumerate(lista_estaciones):
        if estacion.special_case == True:
            
            if estacion.nombre_estacion == "Alberti":
                estacion.siguiente_estacion(lista_estaciones[index + 2])
                estacion.anterior_estacion(lista_estaciones[index - 1])

            elif estacion.nombre_estacion == "Pasco":
                estacion.siguiente_estacion(lista_estaciones[index + 1])
                estacion.anterior_estacion(lista_estaciones[index - 2])

        else:
            if estacion.terminal == True:
                
                if index == 0:
                    estacion.siguiente_estacion(lista_estaciones[index + 1])
                    estacion.anterior_estacion(None)
                    start = estacion

                else:
                    estacion.siguiente_estacion(None)
                    estacion.anterior_estacion(lista_estaciones[index - 1])
                    end = estacion

            else:
                estacion.siguiente_estacion(lista_estaciones[index + 1])
                estacion.anterior_estacion(lista_estaciones[index - 1])

    linea.set_terminales(start= start, end= end)


def json_to_SubteObject(route_file: str) -> dict:
    '''
    method:
    json_to_SubteObject(route_file):
        Convierte un archivo json en un objeto Subte.

    args:
        `route_file`: Ruta del archivo json.

    return:
        Diccionario con los objetos `LineaSubte` y `EstacionSubte`.
    '''
    try:
        with open(route_file, "r", encoding="UTF-8") as file:
            data = json.load(file)
        
        __linea = data["__init__"]
        estaciones = data["Estaciones"]

        subte = {}
        linea = create_LineaSubte(__linea)
        subte['Linea'] = linea

        subte['Estaciones'] = [dict_to_EstacionObject(estacion, linea) for estacion in estaciones]
        
        set_list_stations(subte["Estaciones"], linea)
        
        return subte

    except FileNotFoundError:
        raise FileNotFoundError("El archivo no se encuentra en la ruta indicada.")
    
    except KeyError as e:
        raise KeyError(f"Error en la clave: {e}")


def transform_forecast(forecast_dict: dict) -> movil_subte.MovilSubte:
    try:
        list_to_return = []

        response: list = forecast_dict['Entity']

        for line_info in response:
            _ID_ = line_info['ID']
            line: dict = line_info['Linea']

            ObjLinea = linea_subte.LineaSubte(
                nombre_linea= line['Route_Id'],
                codigo= _ID_,
                direccion= line['Direction_ID']
                )
            
            ObjLinea.activacion_servicio()

            start_time = datetime.time(hour= int(line['start_time'][:2]),
                                       minute= int(line['start_time'][3:5]),
                                       second= int(line['start_time'][6:]))

            start_date = datetime.date(year= int(line['start_date'][:4]),
                                       month= int(line['start_date'][4:6]),
                                       day= int(line['start_date'][6:]))
            
            timestamp_as_datetime = datetime.datetime.fromtimestamp(line['Estaciones'][-1]['arrival']['time'])

            vehiculo = movil_subte.MovilSubte(
                fecha_inicio = start_date,
                linea_de_viaje= ObjLinea,
                horario_programado_salida = start_time,
                fecha_fin= (
                    start_date 
                    if start_time < timestamp_as_datetime.time()
                    else start_date + datetime.timedelta(days=1)
                ),
                horario_programado_llegada= timestamp_as_datetime.time(),
                codigo_vehiculo= line["Trip_Id"]
                )

            for station in line['Estaciones']:
                station_name = station['stop_name']

                ObjStation = movil_subte.EstacionTemp(station_name)
                ObjStation.set_schedule(
                                        _arrivo = station['arrival']["time"],
                                        _salida = station['departure']['time'],
                                        _retraso = station['departure']['delay']
                                        )
                
                list_to_return.append(
                    {
                        "Vehiculo_Id": vehiculo.codigo_vehiculo,
                        "Vehiculo_Info": vehiculo.to_dict(),
                        "Linea": ObjLinea.__dict__,
                        "Estacion": station_name,
                        "Estacion_Info": ObjStation.__dict__
                    }
                )


        return list_to_return
                




    except KeyError as k:
        raise KeyError(f"No se encontró la clave: {k}")

if __name__ == "__main__":
    # file = "Backend/db/lineaA.json"

    # subte = json_to_SubteObject(file)

    # # print(subte)

    # print(subte['Linea'].__listar__())

    # subte['Linea'].direccion = 1

    # print("\n", subte['Linea'].__listar__())


    import requests as rq
    import pprint, os
    from dotenv import load_dotenv

    load_dotenv(dotenv_path="../config/.env")

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    
    response = rq.get(f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}")

    response_json : dict = response.json()

    json_test = {'Entity': [
        {
        "ID": "LineaA_A11",
        "Linea": {
            "Trip_Id": "A11",
            "Route_Id": 'LineaA',
            "Direction_Id": 1,
            "start_time": "10:07:00",
            "start_date": "20250110",
            "Estaciones": [
                {
                    "stop_id": "1059N",
                    "stop_name": "San Pedrito",
                    "arrival": {
                        "time": 1738078935,
                        "delay": 504
                    },
                    "departure": {
                        "time": 1738078959,
                        "delay": 542
                    }
                }
            ]
            }
        }
    ]}

    try:
        result_test = def_movils(response_json)

    except KeyError as e:
        # print(response_json.keys())
        raise KeyError(e)
    # finally:
        # print(response_json)

    pprint.pprint(result_test)