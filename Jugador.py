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
        self.pelota.setPos(self.posicion)
        self.notificar()
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
        # Logica de lo que hace el jugador en cada situacion
        # Si su equipo tiene la pelota
        # Si tiene la pelota
        # Si no tiene la pelota
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

class Arquero(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Arquero
        pass

    def atajar(self):
        # Implementación específica del método atajar para Arquero
        pass

class Defensor(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Defensor
        pass

    def defender(self):
        # Implementación específica del método defender para Defensor
        pass

class Mediocampista(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Mediocampista
        pass

    def distribuirBalon(self):
        # Implementación específica del método distribuirBalon para Mediocampista
        pass

class Delantero(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Delantero
        pass

    def marcarGol(self):
        # Implementación específica del método marcarGol para Delantero
        pass
