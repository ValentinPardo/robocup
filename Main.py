import pygame
import sys
import random
from ContenedorPelota import ContenedorPelota

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
        self.marcador = Marcador()
        self.local_score = 0
        self.visitor_score = 0

        # Jugadores
        for i in range(2):
            self.agregar_jugador_local(Jugador('local'))
        self.agregar_jugador_local(Arquero('local'))
        for i in range(2):
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
        self.pelota.dibujar_hitbox() #Opcional

        for jugador in self.jugadoresLocales + self.jugadoresVisitantes:
            jugador.jugar(self.pelota)
            #jugador.moverse()
            #jugador.buscar_pelota(self.pelota)
            jugador.dibujar_jugador()
            #jugador.dibujar_hitbox() #Opcional

        # Colisiones
        self.chequear_colisiones()

        self.marcador.mostrar_marcador()

    def agregar_jugador_local(self, jugador):
        self.jugadoresLocales.append(jugador)

    def agregar_jugador_visitante(self, jugador):
        self.jugadoresVisitantes.append(jugador)

    def chequear_colisiones(self):
        colisiones = []
        for jugador in self.jugadoresLocales + self.jugadoresVisitantes:
            if jugador.rect.colliderect(self.pelota.rect):
                colisiones.append(jugador)

        for jugador in colisiones:
            self.pelota.llevar_en_los_pies(jugador)

    def chequear_colision_arco(self):
        if self.limites.rect.collidepoint(int(self.pelota.getX), int(self.pelota.getY())): #Si la pelota está dentro del arco
            if self.pelota.x < self.width / 2:
                self.marcador.actualizar(self.local_score + 1, self.visitor_score)  # Gol para el equipo visitante
            else:
                self.marcador.actualizar(self.local_score, self.visitor_score + 1)  # Gol para el equipo local

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
        #self.rect = pygame.Rect(self.width * 0.1, self.height * 0.1, self.width * 0.8, self.height * 0.8 ) # Rectángulo para colisiones
        self.hitbox1 = pygame.Rect(self.width * 0.1, self.height * 0.1, 2, 250 )
        self.hitbox2 = pygame.Rect(self.width * 0.9, self.height * 0.60, 2, 241 )
        self.hitbox3 = pygame.Rect(self.width * 0.1, self.height * 0.1, 1160, 10 )
        self.hitbox4 = pygame.Rect(self.width * 0.1, self.height * 0.9, 1180, 10 )
        self.hitbox5 = pygame.Rect(self.width * 0.9, self.height * 0.1, 2, 250 )
        self.hitbox6 = pygame.Rect(self.width * 0.1, self.height * 0.60, 2, 241)

    def dibujar_limites(self):
        pygame.draw.rect(self.screen, self.line_color, (self.width * 0.1, self.height * 0.1, self.width * 0.8, self.height * 0.8), 3)
        self.dibujar_hitboxes() #opcional

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

    def limite_izquierdo(self):
        return self.width * 0.1 + 3
    
    def limite_derecho(self):
        return self.width * 0.9 - 3 
    
    def limite_superior(self):  
        return self.height * 0.1 + 3
    
    def limite_inferior(self):
        return self.height * 0.9 - 3
    
    def dibujar_hitboxes(self): #Opcional
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox1, 10)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox2, 10)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox3, 10)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox4, 10)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox5, 10)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox6, 10)  

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
        self.velocidad = 2
        self.direccion_x = 0
        self.direccion_y = 0
        self.limites = LimitesCancha() 
        self.contenedorPelota = ContenedorPelota()
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius) # Rectángulo para colisiones

    def dibujar_pelota(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

    def llevar_en_los_pies(self, jugador):
            # Si hay colisión, establecemos la dirección de la pelota
            self.contenedorPelota.asociar_pelota(jugador)

            if jugador.verificar_si_tiene_pelota() and not (self.x > 1120 and 250 < self.y < 500) or (self.x < 330 and 250 < self.y < 500):
                self.setX(jugador.x + jugador.direccion_x * (jugador.velocidad + 10))
                self.setY(jugador.y + jugador.direccion_y * (jugador.velocidad))
            

            #self.direccion_x = jugador.direccion_x
            #self.direccion_y = jugador.direccion_y
            #self.velocidad = jugador.velocidad + 1
            #Si el proximo movimiento se va fuera de la cancha cambia la direccion

            if self.rect.colliderect(self.limites.hitbox1) or self.rect.colliderect(self.limites.hitbox2) or self.rect.colliderect(self.limites.hitbox3) or self.rect.colliderect(self.limites.hitbox4) or self.rect.colliderect(self.limites.hitbox5) or self.rect.colliderect(self.limites.hitbox6):
                self.direccion_x *= -1
                self.direccion_y *= -1
                #Esto hay q chequearlo                             <--------------------------------------
                self.x += self.direccion_x  * self.velocidad
                self.y += self.direccion_y * self.velocidad

            #self.x += self.direccion_x  * self.velocidad
            #self.y += self.direccion_y * self.velocidad

            self.rect.x = self.x - self.radius
            self.rect.y = self.y - self.radius

            


    def dibujar_hitbox(self): #Opcional
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)  # Dibujar la hitbox de la pelota

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y): 
        self.y = y
        
class Jugador:
    def __init__(self, equipo):
        self.screen = screen
        self.color = black
        self.x = 0
        self.y = 0
        self.equipo = equipo
        self.velocidad = 1.5
        self.direccion_x = random.choice([-1, 1])  # Dirección inicial aleatoria en el eje x
        self.direccion_y = random.choice([-1, 1])  # Dirección inicial aleatoria en el eje y
        self.limite_superior = 80
        self.limite_inferior = 716
        self.limite_izquierdo = 145
        self.limite_derecho = 1300
        self.pelota = None
        self.rect = pygame.Rect(self.x, self.y, 10, 10) # Rectángulo para colisiones
        self.limites = LimitesCancha()
        self.dibujarPrimeraVez()

    def dibujarPrimeraVez(self):
        self.color = (0, 0, 255) if self.equipo == 'local' else (255, 0, 0)  # Color diferente para cada equipo
        if self.equipo  == 'local':
            self.x=random.randint(250,700)
            self.y=random.randint(100,700)
        else:
            self.x=random.randint(800,1300)
            self.y=random.randint(100,700)
    
    def dibujar_jugador(self):
        pygame.draw.circle(self.screen, self.color, (self.x,self.y), 10)

    def jugar(self, pelota):
        if self.verificar_si_tiene_pelota():
            self.patear_arco_rival(pelota)
        else:
            self.buscar_pelota(pelota)

    def hacer_un_paso(self,direccion_x, direccion_y):
        # Mover en la dirección de la pelota con una velocidad constante
        self.x += direccion_x * self.velocidad
        self.y += direccion_y * self.velocidad

        # Actualizar la posición del rectángulo de colisión
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

    def moverse(self):
            # Cambiar de dirección aleatoriamente
            if random.random() < 0.02:  # Probabilidad de cambio de dirección
                self.direccion_x = random.choice([-1, 1])
                self.direccion_y = random.choice([-1, 1])

            if self.rect.colliderect(self.limites.hitbox1) or self.rect.colliderect(self.limites.hitbox2) or self.rect.colliderect(self.limites.hitbox3) or self.rect.colliderect(self.limites.hitbox4) or self.rect.colliderect(self.limites.hitbox5) or self.rect.colliderect(self.limites.hitbox6):
                self.direccion_x *= -1
                self.direccion_y *= -1

            self.hacer_un_paso(self.direccion_x, self.direccion_y)

    def dibujar_hitbox(self): #Opcional
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)  # Dibujar la hitbox del jugador

    def buscar_pelota(self, pelota):
        # Calcular la distancia entre el jugador y la pelota
        distancia_x = pelota.x - self.x
        distancia_y = pelota.y - self.y
        distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5

        # Calcular la dirección hacia la pelota
        direccion_x = distancia_x / distancia
        direccion_y = distancia_y / distancia

        self.hacer_un_paso(direccion_x, direccion_y)

    def patear_arco_rival(self, pelota):
        distancia_y = 375 - self.y #ambos deben calcular la distancia al arco rival (en Y es sobre la misma linea para ambos)

        #Si es local va hacia un lado, sino hacia el otro
        if (self.equipo == 'local'):
            distancia_x = 1400 - self.x
        else:
            distancia_x = 50 - self.x

        distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5
        direccion_x = distancia_x / distancia
        direccion_y = distancia_y / distancia

        self.hacer_un_paso(direccion_x, direccion_y)

        if (self.equipo == 'local' and self.x > 1120 and 250 < self.y < 500):
            pelota.x = 1400  # Coordenadas x del arco rival (simulación de un tiro) # NO SE DEBERIA PODER ACCEDER A LAS COORDENADAS DE LA PELOTA DESDE EL JUGADOR
            pelota.setY(random.randint(300, 500)) # Altura aleatoria dentro del arco
        if (self.equipo == 'visitante' and self.x < 330 and 250 < self.y < 500):
            pelota.x = 50  # Coordenadas x del arco rival (simulación de un tiro)
            pelota.setY(random.randint(300, 500)) # Altura aleatoria dentro del arco
                
            

    def asociar_pelota(self, pelota):
        self.pelota = pelota

    def desasociar_pelota(self):
        self.pelota = None

    def verificar_si_tiene_pelota(self):
        return self.pelota is not None
    
    

class Arquero(Jugador):
    def __init__(self, equipo):
        super().__init__(equipo)
        self.limite_superior = int(height * 0.40)
        self.limite_inferior = int(height * 0.60)
        self.limite_izquierdo = int(width * 0.1)
        self.limite_derecho = int(width * 0.2)
        self.direccion = 'DOWN'  # Dirección inicial de movimiento
        self.color = (128,0,128)
        self.velocidad = 2.5
        self.inicializar_posicion()

    def inicializar_posicion(self):
        if self.equipo == 'local':
            self.x = int(width * 0.10)  # Posición inicial arquero local
            self.y = int(height * 0.5)
        else:
            self.x = int(width * 0.90)  # Posición inicial arquero visitante
            self.y = int(height * 0.5)

    def dibujar_jugador(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 10)
        # Actualizar la posición de la hitbox
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

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

    def dibujar_hitbox(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2) # Dibujar la hitbox del arquero

    def buscar_pelota(self, pelota):
        pass

def main():
    campo = CampoFutbol()
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(white)
        campo.dibujar_campo()

        # Mostrar las coordenadas del mouse en la ventana
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = font.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, white)
        screen.blit(text, (1100, 10))  # Mostrar en la esquina superior derecha

        # Actualizar la pantalla una vez al final del ciclo
        pygame.display.flip()
        clock.tick(60)  # Limitar la velocidad de actualización de pantalla a 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

#TODO
#Que el jugador busque la pelota DONE
#Que el jugador agarre la pelota DONE
    #Que el jugador cuando tenga la pelota no vaya a su propio arco
    #Que el jugador cuando tenga la pelota vaya al arco contrario
    #Que el jugador patee la pelota al arco rival
#Chequear bordes de la cancha
#Strategy de movimiento (Una posible hecha)