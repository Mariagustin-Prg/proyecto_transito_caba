# linea_subte.py
# Encoding: UTF-8

# Las clases utilizadas para organizar, guardar y obtener fácilmente la información de los subtes.

from Backend.models.estacion_subte import EstacionSubte

class LineaSubte:
    def __init__(self,
                nombre_linea: str, 
                codigo: str, 
                direccion: int = 0,
                actividad: bool | None = None) -> None:
        
        self.nombre_linea = nombre_linea
        self.codigo = codigo
        self.direccion = direccion
        self.actividad = actividad
        self.estaciones = []
        self.conexiones = []

    def __str__(self):
        return f"{self.nombre_linea}."

    def agregar_estacion(self,
                         nueva_estacion: EstacionSubte,
                         estacion_terminal: bool = False,
                         posicion_intermedia: int | None = None) -> None | IndexError:
        try:
            if posicion_intermedia == None:
                self.estaciones.append(nueva_estacion)
            elif posicion_intermedia != None:
                self.estaciones.insert(posicion_intermedia, nueva_estacion)
            elif estacion_terminal is True:
                self.estaciones.append(nueva_estacion)
                self.estaciones = tuple(self.estaciones)
        except IndexError:
            raise IndexError("El índice indicado en la posición de la Línea es inválido.")

    def __listar__(self):
        return f"{" -> ".join(self.estaciones)}"
    
    def invertir_dirección(self) -> None:
        self.estaciones = self.estaciones[::-1]

    def conexion_otras_lineas(self,
                              linea_subte_conexion,
                              estacion_conectada: EstacionSubte) -> None:
        self.conexion.append( 
            {"Linea conectada": linea_subte_conexion,
            "Estación de conexión": estacion_conectada}
            )
        
    def interrupcion_servicio(self) -> None:
        self.actividad = False

    def activacion_servicio(self) -> None:
        self.actividad = True