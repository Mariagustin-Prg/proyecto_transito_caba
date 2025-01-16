from Backend.models.linea_subte import LineaSubte

class EstacionSubte:
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

    def __str__(self) -> None:
        return f"Estacion({self.nombre_estacion})"

    def establecer_linea(self, 
                linea_: LineaSubte) -> None:
        self.linea_principal = linea_

    def conectar_lineas(self,
                        nueva_linea: LineaSubte) -> None:
        pass

    def definir_coordenadas(self,
                            x: float,
                            y: float) -> None:
        self.latitud = x
        self.longitud = y

    def status(self) -> str:
        if self.actividad:
            return f"Actividad en Estación {self.nombre_estacion}: Normal."
        else:
            return f"Actividad en Estación {self.nombre_estacion}: Interrumpida."
            
    def interrupcion_de_servicio(self) -> None:
        self.actividad = False

    def reactivacion_de_servicio(self) -> None:
        self.actividad = True

    def siguiente_estacion(self, 
                siguiente) -> None:
        self.siguiente = siguiente

    def anterior_estacion(self,
                anterior) -> None:
        self.anterior = anterior