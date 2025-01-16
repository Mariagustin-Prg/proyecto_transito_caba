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
        '''
        method:
        __init__(nombre_linea, codigo, direccion, actividad):
            Inicializa el objeto LineaSubte.

        args:
            `nombre_linea`: Nombre de la línea de subte.
            `codigo`: Código identificador de la línea.
            `direccion`: Dirección de la línea.
            `actividad`: Estado de la línea.

        return:
            None

        example:
        >>> linea = LineaSubte("Linea A", "A", direccion=0, actividad=True)        
        '''
        
        self.nombre_linea = nombre_linea
        self.codigo = codigo
        self.direccion = direccion
        self.actividad = actividad
        self.estaciones = []
        self.conexiones = []

    def __str__(self) -> str:
        '''
        >>> linea = LineaSubte("Linea A", "A")
        >>> print(linea)
        "Linea A"
        '''
        return f"{self.nombre_linea}"

    def agregar_estacion(self,
                         nueva_estacion: EstacionSubte,
                         estacion_terminal: bool = False,
                         posicion_intermedia: int | None = None) -> None | IndexError:
        '''
        method
        ------ 
        agregar_estacion(nueva_estacion, estacion_terminal, posicion_intermedia):
            Agrega una nueva estación a la línea de subte.

        args:
            `nueva_estacion`: Estación a agregar.
            `estacion_terminal`: Indica si la estación es terminal.
            `posicion_intermedia`: Posición en la que se desea agregar la estación.

        return:
            None

        raises:
            IndexError: Si el índice indicado en la posición de la Línea es inválido.

        Example
        -------
        >>> linea = LineaSubte("Linea A", "A")
        >>> estacion = EstacionSubte("Estación A", 0, 0)
        >>> linea.agregar_estacion(estacion)

        '''

    # Agrega la estación a la línea de subte.
        try:
            # Verifica si la estación se debe agregar en una posición intermedia.
            if posicion_intermedia is not None:
                # La inserta en la posición indicada.
                self.estaciones.insert(posicion_intermedia, nueva_estacion)
            # Si no se indica una posición, la agrega al final de la lista.
            else:
                self.estaciones.append(nueva_estacion)
                # En caso de ser una estación terminal, convierte la lista en una tupla.
                if estacion_terminal:
                    self.estaciones = tuple(self.estaciones)
        # Captura el error en caso de que el índice sea inválido. Es decir, cuando la posición indicada no existe.
        except IndexError:
            # Lanza una excepción.
            raise IndexError("El índice indicado en la posición de la Línea es inválido.")

    def __listar__(self) -> str:
        '''
        Devuelve un string con el nombre de las estaciones de la línea. 

        Example
        ------

        >>> linea = LineaSubte("Linea A", "A")
        >>> estacion = EstacionSubte("Estación A", 0, 0)
        >>> linea.agregar_estacion(estacion)
        >>> estacion_2 = EstacionSubte("Estación B", 0, 0)
        >>> linea.agregar_estacion(estacion_2)
        >>> linea.__listar__()
        "Estación A -> Estación B"
        '''
        return f"{" -> ".join(self.estaciones)}"
    
    def invertir_dirección(self) -> None:
        '''
        Invierte el orden de las estaciones en la línea.
        '''
        self.estaciones = self.estaciones[::-1]

    def conexion_otras_lineas(self,
                              linea_subte_conexion,
                              estacion_conectada: EstacionSubte) -> None:
        '''
        `method` conexion_otras_lineas(linea_subte_conexion, estacion_conectada):
            Establece la conexión entre dos líneas de subte.

        args:
            `linea_subte_conexion`: Línea de subte a la que se conecta la línea principal.
            `estacion_conectada`: Estación en la que se realiza la conexión.

        return:
            None

        raises:
            None
        
        '''
        self.conexion.append( 
            {"Linea conectada": linea_subte_conexion,
            "Estación de conexión": estacion_conectada}
            )
        
    def interrupcion_servicio(self) -> None:
        '''Cambia el estado de la línea a inactiva.'''
        self.actividad = False

    def activacion_servicio(self) -> None:
        '''Cambia el estado de la línea a activa.'''
        self.actividad = True