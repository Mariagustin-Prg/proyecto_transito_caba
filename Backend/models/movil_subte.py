"""
Este módulo define la clase MovilSubte, la cual se utiliza para recopilar información
relacionada con los viajes de los vehículos en la red de subterráneos, incluyendo horarios,
líneas, retrasos, cancelaciones, entre otros.

Clases:
    MovilSubte: Representa un vehículo en la red de subterráneos y almacena información
                sobre sus viajes y horarios.

Dependencias:
    - Backend.models.linea_subte.LineaSubte
    - Backend.models.estacion_subte.EstacionSubte
    - datetime.date
    - datetime.time
    - datetime.datetime

Ejemplo de uso:
---------------
"Vehiculo(111)"
>>> vehiculo = MovilSubte(date(2021, 10, 1), date(2021, 10, 1), linea, time(8, 0), time(8, 30), retraso=0, codigo_vehiculo="111")
>>> vehiculo.modificar_retraso(300)
>>> vehiculo.retraso
300
>>> print(vehiculo)
"Vehiculo(111)"
"""

from Backend.models.linea_subte import LineaSubte
from Backend.models.estacion_subte import EstacionSubte
from datetime import date, time, datetime

class MovilSubte:
    
    '''
    Objeto con el cual se recopila toda la información de viajes, horarios, líneas, reprogramaciones,
    retrasos, cancelaciones, entre otros.

    Parametros
    ----------
    fecha_inicio: date
        La fecha en que inicia el viaje.
    fecha_fin: date
        La fecha en la que finaliza el viaje.
    linea_de_viaje: LineaSubte
        Linea en la que se moverá el vehículo.
    horario_programado_salida: time
        Horario programado de salida.
    horario_programado_llegada: time
        Horario programada de llegada a la estación terminal.
    retraso: int
        Retraso del vehículo, medido en segundos.
    codigo_vehículo: str
        Código de identificación del vehículo.
    __create__: str
        Fecha y hora de creación del objeto.
    __update__: str
        Fecha y hora de última actualización del objeto.

    Métodos
    -------
    modificar_retraso(nuevo_retraso): None
        Modifica el retraso del vehículo.
    '''
    
    def __init__(self,
                 fecha_inicio: date,
                 fecha_fin: date,
                 linea_de_viaje: LineaSubte,
                 horario_programado_salida: time,
                 horario_programado_llegada: time,
                 retraso: int | None = None,
                 codigo_vehiculo: str | None = None,
                 ) -> None:
        '''
        method __init__:
            Inicializa el objeto MovilSubte.

        args:
            `fecha_inicio`: Fecha en que inicia el viaje.
            `fecha_fin`: Fecha en la que finaliza el viaje.
            `linea_de_viaje`: Linea en la que se moverá el vehículo.
            `horario_programado_salida`: Horario programado de salida.
            `horario_programado_llegada`: Horario programada de llegada a la estación terminal.
            `retraso`: Retraso del vehículo, medido en segundos.
            `codigo_vehículo`: Código de identificación del vehículo.
        '''

        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.linea = linea_de_viaje
        self.time_salida = horario_programado_salida
        self.time_llegada = horario_programado_llegada
        self.retraso = retraso
        self.codigo_vehiculo = codigo_vehiculo
        self.__create__ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__update__ = None

    def modificar_retraso(self, nuevo_retraso: int) -> None:
        '''
        Modifica el retraso del vehículo.

        args:
            `nuevo_retraso`: Nuevo retraso del vehículo.
        '''
        self.retraso = nuevo_retraso
        self.__update__ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        '''
        Imprime el objeto en forma de string.
        '''
        return f"Vehículo({self.codigo_vehiculo})"
    
    # def __repr__(self) -> str:
    #     '''
    #     Permite obtener una representación del objeto.
    #     '''
    #     return f"Vehículo({self.codigo_vehiculo})"
    
    def __eq__(self, other) -> bool:
        '''
        Permite comparar si dos objetos son iguales.
        '''
        return self.codigo_vehiculo == other.codigo_vehiculo
    
    def __ne__(self, other) -> bool:
        '''
        Sirve para comparar si dos objetos son distintos.
        '''
        return self.codigo_vehiculo != other.codigo_vehiculo
    
    def lista_de_estaciones(self) -> list[EstacionSubte]:
        '''
        Devuelve una lista con las estaciones de la línea.
        '''
        return self.linea.estaciones