import math

class Pelota:
    _instancia = None  # Almacenar la instancia única

    def __new__(cls):
        if not cls._instancia:
            cls._instancia = super(Pelota, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self.inicializar()
            self.inicializado = True
    
    def inicializar(self):
        self.direccion = None
        self.coordenadas = [725, 400]
        self.velocidad = 0
        self.jugador = None

    def obtenida(self):
        # Implementación del método obtenida
        pass

    def esPateada(self):
        # Implementación del método esPateada
        pass

    def getPos(self):
        # Implementación del método getPos
        pass

    def setPos(self, posJugador, angulo_radianes):
        self.coordenadas[0] += posJugador[0] + math.cos(angulo_radianes) * 10
        self.coordenadas[1] += posJugador[1] + math.sin(angulo_radianes) * 10

    def suscribir(self, pelota_view):
        # Implementación del método suscribir
        self.pelota_view = pelota_view
        pass

    def notificar(self):
        # Implementación del método notificar
        self.pelota_view.actualizar(self.coordenadas)
        pass
