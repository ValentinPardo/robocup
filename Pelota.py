import math
import pygame
import random


class Pelota:
    _instancia = None  # Almacenar la instancia única (Singleton)

    def __new__(cls):
        if not cls._instancia:
            cls._instancia = super(Pelota, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self.inicializar()
            self.inicializado = True
    
    def inicializar(self):
        self.coordenadas = [725, 400]
        self.velocidad = 0
        self.radio = 10
        self.hitbox = pygame.Rect(self.coordenadas[0] - self.radio, self.coordenadas[1] - self.radio, 2 * self.radio, 2 * self.radio)

    def esPateada(self,angulo_radianes):
        # Implementación del método esPateada
        self.velocidad = 0.002

        self.coordenadas[0] += math.cos(angulo_radianes ) * self.velocidad
        self.coordenadas[1] += math.sin(angulo_radianes ) * self.velocidad
        self.hitbox = pygame.Rect(self.coordenadas[0] - 10, self.coordenadas[1] - 10, 20, 20)
        

    def getPos(self):
        # Implementación del método getPos
        return self.coordenadas

    def setPos(self, posJugador, angulo_radianes):
        # Calcula la nueva posición de la pelota
        nueva_pos_x = posJugador[0] + math.cos(angulo_radianes) * (self.radio)
        nueva_pos_y = posJugador[1] + math.sin(angulo_radianes) * (self.radio)

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

    def fueraDeLaCancha(self):
        if (0 <= self.coordenadas[0] <= 147 and 80 <= self.coordenadas[1] <= 718) or \
        (1305 <= self.coordenadas[0] <= 1449 and 80 <= self.coordenadas[1] <= 718):
            return True
        return False

    def suscribir(self, pelota_view):
        # Implementación del método suscribir
        self.pelota_view = pelota_view
        pass

    def notificar(self):
        # Implementación del método notificar
        self.pelota_view.actualizar_coordenadas(self.coordenadas,self.hitbox)
        pass
