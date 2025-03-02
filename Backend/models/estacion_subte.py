# estacion_subte.py
'''
Encoding: UTF-8

estacion_subte.py
------

Este módulo contiene la clase `EstacionSubte`, que se utiliza para organizar, guardar y obtener fácilmente la información de las estaciones de subte.

Clases:
- `EstacionSubte`: Representa una estación de subte, con métodos para establecer la línea principal, conectar con otras líneas, definir coordenadas, interrumpir y activar el servicio, establecer la siguiente y anterior estación.

Ejemplo de uso:
---------------
"Estación A"
>>> estacion = EstacionSubte("Estación A")
"Estación A"
>>> estacion.establecer_linea(linea)
"Estación A"
>>> estacion.conectar_lineas(linea)
>>> estacion.definir_coordenadas(12.345, 67.890)
>>> estacion.interrupcion_de_servicio()
>>> estacion.actividad
False
>>> estacion.activacion_de_servicio()
>>> estacion.actividad
True
'''

from Backend.models.linea_subte import LineaSubte

class EstacionSubte:
    '''
    Establece los parámetros y recopila los elementos de las estaciones en un único objeto. \n

    Parámetros
    ---------
        `nombre_estacion` (str): El nombre de la estación.\n
        `latitud` (float | None): Latitud en que se encuentra la estación. \n
        `longitud` (float | None): Longitud en la que se encuentra la estación. \n
        `linea_principal` (LineaSubte | None): Linea de subte en la esta estación se encuentra incluída. \n
        `conexion` (bool): Indicador si la estación puede hacer conexión con otras líneas. \n
        `terminal` (bool): Indicador si es una estación terminal. \n
        `actividad` (bool): Estado del servicio de la estación. \n
        `anden_central` (bool): Indicador si la estación tiene andén central. \n

    Métodos
    -------
        `establecer_linea(linea_, posicion_intermedia)`: Incluye a la línea indicada la estación ya creada. De ser necesario puede indicarse la posición de la estación dentro de la línea.
    '''
    def __init__(self,
                 nombre_estacion: str,
                 latitud: float | None = None,
                 longitud: float | None = None,
                 linea_principal: LineaSubte | None = None,
                 conexion: bool = False,
                 terminal: bool = False,
                 actividad: bool = True,
                 anden_central: bool = False) -> None:
        self.nombre_estacion = nombre_estacion
        self.latitud = latitud
        self.longitud = longitud
        self.linea_principal = linea_principal
        self.conexion = conexion
        self.terminal = terminal
        self.actividad = actividad
        self.anden_central = anden_central

        self.special_case = None

    def __str__(self) -> None:
        return f"{self.nombre_estacion}"
    
    def __repr__(self) -> str:
        return self.nombre_estacion

    def establecer_linea(self, 
                linea_: LineaSubte,
                posicion_en_la_linea: int | None = None) -> None:
        '''
        Establece la línea principal de la estación.

        args:
            linea_ (LineaSubte): La línea en la que se desea incluir la estación.
            posicion_en_la_linea (int | None): Posición en la que se encuentra la estación dentro de la línea.

        '''
        linea_.agregar_estacion(self, posicion_en_la_linea)
        self.linea_principal = linea_
        self.posicion = posicion_en_la_linea

    def conectar_lineas(self,
                        nueva_linea: LineaSubte) -> None:
        '''
        Relaciona la estación con las otras lineas con las que hace conexión.

        Parametros
        ----------
        nueva_linea: LineaSubte
            Relaciona la estación de una línea con otra línea con la que puede hacer conexión dentro del sistema de subtes.
        '''
        pass

    def definir_coordenadas(self,
                            x: float,
                            y: float) -> None:
        '''
        Define las coordenadas de la estación

        Parametros
        ----------
        x: Latitud.
        y: Longitud.
        '''
        self.latitud = x
        self.longitud = y

    def status(self) -> str:
        '''
        Retorna un texto con la información de la actividad de la estación.
        '''
        if self.actividad:
            return f"Actividad en Estación {self.nombre_estacion}: Normal."
        else:
            return f"Actividad en Estación {self.nombre_estacion}: Interrumpida."
            
    def interrupcion_de_servicio(self) -> None:
        '''
        Interrumpe el estado de actividad de la estación
        '''
        self.actividad = False

    def activacion_de_servicio(self) -> None:
        '''
        Activa el estado de actividad de la estación.
        '''
        self.actividad = True

    def siguiente_estacion(self, 
                siguiente) -> None:
        '''
        Establece la relación de orden con la siguiente estación.
        
        args:
            siguiente (EstacionSubte): La próxima estación de la línea.
        '''
        if siguiente != self: 
            self.siguiente = siguiente

    def anterior_estacion(self,
                anterior) -> None:
        '''Establece la relación de orden con la estación anterior.'''
        if anterior != self:
            self.anterior = anterior


    def to_json(self) -> dict:
        return {
            k[5:]: va
            for k, va in self.__dict__.values()
        }