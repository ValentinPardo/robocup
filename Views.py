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
        self.marcador = Marcador()

    def actualizar(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 128, 0))
            self.dibujar_campo()
            
            # Mostrar las coordenadas del mouse en la ventana
            mouse_x, mouse_y = pygame.mouse.get_pos()
            text = font.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, (255,255,255))
            screen.blit(text, (1100, 10))  # Mostrar en la esquina superior derecha
            #Actualizacion de pantalla
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

    #Separo el dibujar el campo en un metodo aparte para que sea mas legible
    def dibujar_campo(self):
        #Linea del medio
        pygame.draw.line(screen, (255, 255, 255), (width / 2, height * 0.1), (width / 2, height * 0.9), 3)
        #Lineas de los laterales
        pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.laterales_x[0], self.dimensiones.lateralSuperior_y) ,( self.dimensiones.laterales_x[1],self.dimensiones.lateralSuperior_y), 3)
        pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.laterales_x[0], self.dimensiones.lateralInferior_y) ,( self.dimensiones.laterales_x[1],self.dimensiones.lateralInferior_y), 3)
        pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.fondoDerecho_x,self.dimensiones.fondos_y[0]) ,(self.dimensiones.fondoDerecho_x,self.dimensiones.fondos_y[1]), 3)
        pygame.draw.line(screen, (255, 255, 255), (self.dimensiones.fondoIzquierdo_x,self.dimensiones.fondos_y[0]) ,( self.dimensiones.fondoIzquierdo_x,self.dimensiones.fondos_y[1]), 3)
        #Circulo central
        pygame.draw.circle(screen, (255, 255, 255), (int(width / 2), int(height / 2)), 73, 3)
        pygame.draw.circle(screen, (255, 255, 255), (int(width / 2), int(height / 2)), 5)
        # Dibujar las Areas
        pygame.draw.rect(screen, (255,255,255), (self.dimensiones.fondoIzquierdo_x -2, height * 0.25, 250, height * 0.5), 3)
        pygame.draw.rect(screen, (255,255,255), (self.dimensiones.fondoDerecho_x - 248, height * 0.25, 250, height * 0.5), 3)
        # Dibujar el punto penal
        pygame.draw.circle(screen, (255,255,255), (int(width * 0.25), int(height / 2)), 5)
        pygame.draw.circle(screen, (255,255,255), (int(width * 0.75), int(height / 2)), 5)
        #Dibujar Arcos
        pygame.draw.line(screen, (0,128,0), (width * 0.1, height * 0.40),(width * 0.1, height * 0.60), width=15)
        pygame.draw.line(screen, (0,128,0), (width * 0.9, height * 0.40),(width * 0.9, height * 0.60), width=15)
        #Dibujar Marcador
        self.marcador.mostrar_marcador()

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


class Marcador:
    def __init__(self):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
        self.local_score = 0
        self.visitor_score = 0

    def actualizar(self, local_score, visitor_score):
        self.local_score = local_score
        self.visitor_score = visitor_score
        self.mostrar_marcador()

    def mostrar_marcador(self):
        marcador_texto = f"Local {self.local_score} - Visitante {self.visitor_score}"
        texto_renderizado = self.font.render(marcador_texto, True, (0,0,0))
        self.screen.blit(texto_renderizado, (10, 10))