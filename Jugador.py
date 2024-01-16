class Jugador:
    def __init__(self, coordenadas, posicion):
        self.direccion = 0
        self.velocidad = 2.5
        self.posicion = posicion
        self.pelota = None
        self.coordenadas = coordenadas
        self.jugador_view = None

    def correr(self):
        # Implementación del método correr
        self.pelota.setPos(self.coordenadas)
        pass

    def patear(self):
        # Implementación del método patear
        
        pass

    def rotar(self):
        # Implementación del método rotar
        pass

    def obtenerPelota(self):
        # Implementación del método obtenerPelota
        pass

    def comportamiento(self):
        # Implementación del método comportamiento
        pass

    def sinPelota(self):
        # Implementación del método sinPelota
        pass

    def conPelota(self):
        # Implementación del método conPelota
        pass

    def equipoConPosesion(self):
        # Implementación del método equipoConPosesion
        pass

    def getPos(self):
        # Implementación del método getPos
        pass

    def suscribir(self, jugadorView):
        # Implementación del método suscribir
        self.jugador_view = jugadorView
        pass

    def notificar(self):
        # Implementación del método notificar
        self.jugador_view.actualizar(self.posicion)
        pass
