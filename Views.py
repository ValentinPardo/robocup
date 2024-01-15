import pygame

class CampoView:
    def __init__(self, dimensiones):
        self.dimensiones = dimensiones

    def crearCampo(self):
        # Implementa la lógica para crear el campo en la vista
        pass

class PelotaView:
    def __init__(self, ):
        pass

    def actualizar(self,posicion):
        # Implementa la lógica para actualizar la posición de la pelota en la vista
        pygame.draw.circle(screen, (255, 255, 255), posicion, 10)
        pass

class JugadorView:
    def __init__(self):
        pass

    def actualizar(self,posicion):
        # Implementa la lógica para actualizar la posición del jugador en la vista
        pygame.draw.circle(screen, (255, 0, 0), posicion, 10)
        pass
