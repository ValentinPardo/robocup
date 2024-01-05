import pygame
import sys
import random

pygame.init()

width, height = 1450, 800

white = (255, 255, 255)
green = (0, 128, 0)
black = (0, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fútbol 5')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class CampoFutbol:
    _instancia = None  # Almacenar la instancia única

    def __new__(cls):
        if not cls._instancia:
            cls._instancia = super(CampoFutbol, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self.inicializar()
            self.inicializado = True

    def inicializar(self):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cesped = green  
        self.line_color = white  
        self.limites = LimitesCancha()
        self.pelota = Pelota()
        self.jugadoresLocales = []
        self.jugadoresVisitantes = []
        # Jugadores
        self.agregar_jugador_local(Jugador('local'))
        self.agregar_jugador_local(Arquero('local'))
        self.agregar_jugador_visitante(Jugador('visitante'))
        self.agregar_jugador_visitante(Arquero('visitante'))
        self.dibujar_campo()

    def dibujar_campo(self):
        self.screen.fill(self.cesped)
        
        pygame.draw.line(self.screen, self.line_color, (self.width / 2, self.height * 0.1), (self.width / 2, self.height * 0.9), 3)
        pygame.draw.circle(self.screen, self.line_color, (int(self.width / 2), int(self.height / 2)), 73, 3)
        pygame.draw.circle(self.screen, self.line_color, (int(self.width / 2), int(self.height / 2)), 5)
        
        # Dibujar las líneas del campo
        self.limites.dibujar()
        
        # Dibujar la pelota
        self.pelota.dibujar_pelota()  

        for jugador in self.jugadoresLocales + self.jugadoresVisitantes:
            jugador.moverse()
            jugador.dibujar_jugador()   
            

    def agregar_jugador_local(self, jugador):
        self.jugadoresLocales.append(jugador)

    def agregar_jugador_visitante(self, jugador):
        self.jugadoresVisitantes.append(jugador)
    


class LimitesCancha:
    _instancia = None  # Almacenar la instancia única

    def __new__(cls):
        if not cls._instancia:
            cls._instancia = super(LimitesCancha, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self.inicializar()
            self.inicializado = True

    def inicializar(self):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.line_color = white

    def dibujar_limites(self):
        pygame.draw.rect(self.screen, self.line_color, (self.width * 0.1, self.height * 0.1, self.width * 0.8, self.height * 0.8), 3)
        # Dibujar las Areas
        pygame.draw.rect(self.screen, self.line_color, (self.limite_izquierdo() -2, self.height * 0.25, 250, self.height * 0.5), 3)
        pygame.draw.rect(self.screen, self.line_color, (self.limite_derecho() - 248, self.height * 0.25, 250, self.height * 0.5), 3)
        # Dibujar el punto penal
        pygame.draw.circle(self.screen, self.line_color, (int(self.width * 0.25), int(self.height / 2)), 5)
        pygame.draw.circle(self.screen, self.line_color, (int(self.width * 0.75), int(self.height / 2)), 5)

    #Dibujar arcos
    def dibujar_arcos(self):
        pygame.draw.line(self.screen, green, (self.width * 0.1, self.height * 0.40),(self.width * 0.1, self.height * 0.60), width=10)
        pygame.draw.line(self.screen, green, (self.width * 0.9, self.height * 0.40),(self.width * 0.9, self.height * 0.60), width=10)

    #devolver el limite izquierdo de la cancha
    def limite_izquierdo(self):
        return self.width * 0.1 + 3
    
    #devolver el limite derecho de la cancha
    def limite_derecho(self):
        return self.width * 0.9 - 3 

    def dibujar(self):
        self.dibujar_limites()
        self.dibujar_arcos()

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
        texto_renderizado = self.font.render(marcador_texto, True, black)
        self.screen.blit(texto_renderizado, (10, 10))

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

    # Constructor
    def inicializar(self):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.color = black
        self.radius = 10
        self.x = self.width / 2
        self.y = self.height / 2
        self.velocidad =2.5
        self.direccion_x = 10
        self.direccion_y = 0
        self.limites = LimitesCancha() 
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def dibujar_pelota(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

    def mover(self):
        # Mover en la dirección actual
        self.x += self.direccion_x * self.velocidad
        self.y += self.direccion_y * self.velocidad
        self.rect.center = (int(self.x), int(self.y))

class Jugador:
    def __init__(self, equipo):
        self.screen = screen
        self.color = black
        self.x = 0
        self.y = 0
        self.equipo = equipo
        self.velocidad = 2.5
        self.direccion_x = random.choice([-1, 1])  # Dirección inicial aleatoria en el eje x
        self.direccion_y = random.choice([-1, 1])  # Dirección inicial aleatoria en el eje y
        self.limite_superior = 80
        self.limite_inferior = 716
        self.limite_izquierdo = 145
        self.limite_derecho = 1300
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.dibujarPrimeraVez()

    
    def dibujarPrimeraVez(self):
        self.color = (0, 0, 255) if self.equipo == 'local' else (255, 0, 0)  # Color diferente para cada equipo
        if self.equipo  == 'local':
            self.x=random.randint(250,700)
            self.y=random.randint(100,700)
            pygame.draw.circle(self.screen, self.color, (self.x,self.y), 10)
        else:
            self.x=random.randint(800,1300)
            self.y=random.randint(80,716)
            pygame.draw.circle(self.screen, self.color, (self.x,self.y), 10)
    
    def dibujar_jugador(self):
        pygame.draw.circle(self.screen, self.color, (self.x,self.y), 10)

    def moverse(self):
            # Cambiar de dirección aleatoriamente
            if random.random() < 0.02:  # Probabilidad de cambio de dirección
                self.direccion_x = random.choice([-1, 1])
                self.direccion_y = random.choice([-1, 1])

            # Mover en la dirección actual
            self.x += self.direccion_x * self.velocidad
            self.y += self.direccion_y * self.velocidad

            # Revisar límites y cambiar dirección si se sale de los límites
            if self.x <= self.limite_izquierdo or self.x >= self.limite_derecho:
                self.direccion_x *= -1
            if self.y <= self.limite_superior or self.y >= self.limite_inferior:
                self.direccion_y *= -1

class Arquero(Jugador):
    def __init__(self, equipo):
        super().__init__(equipo)
        self.limite_superior = int(height * 0.40)
        self.limite_inferior = int(height * 0.60)
        self.limite_izquierdo = int(width * 0.1)
        self.limite_derecho = int(width * 0.2)
        self.direccion = 'DOWN'  # Dirección inicial de movimiento
        self.dibujarPrimeraVez()

    def dibujarPrimeraVez(self):
        self.color = (128,0,128)
        if self.equipo  == 'local':
            pygame.draw.circle(self.screen, self.color, (3000,3000), 10) #error de dibujo de los arqueros
        else:
            pygame.draw.circle(self.screen, self.color, (3000,3000), 10)

    def moverse(self):
            if self.direccion == 'DOWN':
                if self.y + self.velocidad <= self.limite_inferior:
                    self.y += self.velocidad
                else:
                    self.direccion = 'UP'
            elif self.direccion == 'UP':
                if self.y - self.velocidad >= self.limite_superior:
                    self.y -= self.velocidad
                else:
                    self.direccion = 'DOWN'
def main():
    campo = CampoFutbol()
    #pelota = Pelota()
    marcador = Marcador()
    running = True
    local_score = 0
    visitor_score = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #if jugador.rect.colliderect(pelota.rect):
            #    pelota.mover()
            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_SPACE:
                #    pelota.mover()
                if event.key == pygame.K_l:
                    local_score += 1
                    marcador.actualizar(local_score, visitor_score)
                elif event.key == pygame.K_v:
                    visitor_score += 1
                    marcador.actualizar(local_score, visitor_score)

        # Dibujar en un búfer
        
        screen.fill(white)
        campo.dibujar_campo()

        # Dibujar el marcador en el búfer
        marcador.mostrar_marcador()

        # Obtener las coordenadas del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Mostrar las coordenadas en la ventana
        text = font.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, white)
        screen.blit(text, (1100, 10))  # Mostrar en la esquina superior izquierda

        # Actualizar la pantalla una vez al final del ciclo
        pygame.display.flip()
        clock.tick(60)  # Limitar la velocidad de actualización de pantalla a 60 FPS

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()