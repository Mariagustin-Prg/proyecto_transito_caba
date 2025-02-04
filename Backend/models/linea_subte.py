# linea_subte.py
"""
linea_subte.py
--------------
Este módulo contiene la clase `LineaSubte`, que se utiliza para organizar, guardar y obtener fácilmente la información de las líneas de subte.
Clases:
- `LineaSubte`: Representa una línea de subte, con métodos para agregar estaciones, listar estaciones, invertir la dirección de la línea, establecer conexiones con otras líneas y cambiar el estado de actividad de la línea.

Ejemplo de uso:
---------------
"Estación A"
>>> linea.invertir_dirección()
"Estación A"
>>> linea.interrupcion_servicio()
>>> linea.actividad
False
>>> linea.activacion_servicio()
>>> linea.actividad
True
"""

# from Backend.models.estacion_subte import EstacionSubte

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

        self.conexiones = []

    def __str__(self) -> str:
        '''
        >>> linea = LineaSubte("Linea A", "A")
        >>> print(linea)
        "Linea A"
        '''
        return f"{self.nombre_linea}"
    
    def __repr__(self):
        return self.nombre_linea

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
        str_estaciones = ""

        ctrl = self.terminal_inicio if self.direccion == 0 else self.terminal_fin
        while ctrl != None:
            str_estaciones += f"{ctrl} -> "
            ctrl = ctrl.siguiente if self.direccion == 0 else ctrl.anterior

        return str_estaciones[:-4]
        
    def interrupcion_servicio(self) -> None:
        '''Cambia el estado de la línea a inactiva.'''
        self.actividad = False

    def activacion_servicio(self) -> None:
        '''Cambia el estado de la línea a activa.'''
        self.actividad = True

    def set_terminales(self, start, end) -> None:
        '''
        Establece las estaciones terminales de la línea.
        '''
        self.terminal_inicio = start
        self.terminal_fin = end

    def estaciones(self) -> list:
        '''
        Devuelve una lista con las estaciones de la línea.
        '''
        
        estaciones = []
        ctrl = self.terminal_inicio if self.direccion == 0 else self.terminal_fin
        while ctrl != None:
            estaciones.append(ctrl)
            ctrl = ctrl.siguiente if self.direccion == 0 else ctrl.anterior

        return estaciones

        