from ..models import (
    linea_subte,
    estacion_subte,
    movil_subte
)
# from Backend.schemas.db_client import clientDB
import json


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
    

if __name__ == "__main__":
    file = "Backend/db/lineaA.json"

    subte = json_to_SubteObject(file)

    # print(subte)

    print(subte['Linea'].__listar__())

    subte['Linea'].direccion = 1

    print("\n", subte['Linea'].__listar__())