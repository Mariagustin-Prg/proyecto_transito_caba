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
        

        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.linea = linea_de_viaje
        self.time_salida = horario_programado_salida
        self.time_llegada = horario_programado_llegada
        self.retraso = retraso
        self.codigo_vehiculo = codigo_vehiculo