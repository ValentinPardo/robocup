import pygame
#import sys
#import random

pygame.init()
width, height = 1450, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fútbol 5')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class CampoView:
    def __init__(self, dimensiones):
        self.dimensiones = dimensiones

    def actualizar(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 128, 0))
        
            pygame.draw.line(screen, (255, 255, 255), (width / 2, height * 0.1), (width / 2, height * 0.9), 3)
            pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.laterales_x[0], self.dimensiones.lateralSuperior_y) ,( self.dimensiones.laterales_x[1],self.dimensiones.lateralSuperior_y), 3)
            pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.laterales_x[0], self.dimensiones.lateralInferior_y) ,( self.dimensiones.laterales_x[1],self.dimensiones.lateralInferior_y), 3)
            pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.fondoDerecho_x,self.dimensiones.fondos_y[0]) ,(self.dimensiones.fondoDerecho_x,self.dimensiones.fondos_y[1]), 3)
            pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.fondoIzquierdo_x,self.dimensiones.fondos_y[0]) ,( self.dimensiones.fondoIzquierdo_x,self.dimensiones.fondos_y[1]), 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(width / 2), int(height / 2)), 73, 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(width / 2), int(height / 2)), 5)

            pygame.display.flip()
            clock.tick(60)

class PelotaView:
    def __init__(self):
        pass

    def actualizar(self,posicion):
        # Implementa la lógica para actualizar la posición de la pelota en la vista
        pygame.draw.circle(screen, (0, 0, 0), posicion, 10)

class JugadorView:
    def __init__(self):
        pass

    def actualizar(self,posicion):
        # Implementa la lógica para actualizar la posición del jugador en la vista
        pygame.draw.circle(screen, (255, 0, 0), posicion, 10)
