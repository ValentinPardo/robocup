import math
import pygame


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
        self.radio = 10
        self.hitbox = pygame.Rect(self.coordenadas[0] - self.radio, self.coordenadas[1] - self.radio, 2 * self.radio, 2 * self.radio)

    def obtenida(self, jugador):
        # Implementación del método obtenida
        if self.jugador == None:
            self.jugador = jugador
            self.jugador.obtenerPelota()

    def esPateada(self):
        # Implementación del método esPateada
        pass

    def getPos(self):
        # Implementación del método getPos
        pass

    def setPos(self, posJugador, angulo_radianes):
        # Calcula la nueva posición de la pelota
        nueva_pos_x = posJugador[0] + math.cos(angulo_radianes) * (self.radio + 10)
        nueva_pos_y = posJugador[1] + math.sin(angulo_radianes) * (self.radio + 10)

        # Actualiza las coordenadas de la pelota
        self.coordenadas = [nueva_pos_x, nueva_pos_y]
        #Actualizar hitbox
        self.hitbox = pygame.Rect(self.coordenadas[0] - self.radio, self.coordenadas[1] - self.radio, 2 * self.radio, 2 * self.radio)
        try:
            self.notificar()
        except:
            pass

    def obtenerHitbox(self):
        # Devuelve un rectángulo que representa la hitbox de la pelota
        return self.hitbox

    def suscribir(self, pelota_view):
        # Implementación del método suscribir
        self.pelota_view = pelota_view
        pass

    def notificar(self):
        # Implementación del método notificar
        self.pelota_view.actualizar_coordenadas(self.coordenadas,self.hitbox)
        pass
