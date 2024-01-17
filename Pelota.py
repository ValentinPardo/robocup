class Pelota:
    def __init__(self ):
        self.direccion = None
        self.coordenadas = [725,400]
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

    def setPos(self, nueva_posicion):
        # Implementación del método setPos
        pass

    def suscribir(self, pelota_view):
        # Implementación del método suscribir
        self.pelota_view = pelota_view
        pass

    def notificar(self):
        # Implementación del método notificar
        self.pelota_view.actualizar(self.coordenadas)
        pass
