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
        self.marcador = Marcador()
        self.local_score = 0
        self.visitor_score = 0
        self.tiempo_espera = 0

        # Jugadores
        for i in range(5):
            self.agregar_jugador_local(Jugador('local'))
        self.agregar_jugador_local(Arquero('local'))
        for i in range(5):
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
        #self.limites.dibujar_hitboxes() #Opcional
        
        # Dibujar la pelota
        self.pelota.dibujar_pelota()  
        #self.pelota.dibujar_hitbox() #Opcional

        for jugador in self.jugadoresLocales + self.jugadoresVisitantes:
            jugador.buscar_pelota(self.pelota)
            jugador.moverse()
            jugador.dibujar_jugador()
            #jugador.dibujar_hitbox() #Opcional

        # Colisiones
        self.chequear_colisiones()
        
        self.mensajeGol()
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
            self.pelota.patear(jugador)

    def chequear_colision_arco(self):
        if (0 <= self.pelota.x <= 147 and 320 <= self.pelota.y <= 480) or \
        (1305 <= self.pelota.x <= 1449 and 320 <= self.pelota.y <= 480):
            if self.tiempo_espera == 0:
                if 0 <= self.pelota.x <= 147:  # Gol visitante
                    self.visitor_score += 1
                else:  # Gol local
                    self.local_score += 1

                self.marcador.actualizar(self.local_score, self.visitor_score)
                self.tiempo_espera = 100  # Establece el tiempo de espera después del gol
        elif (0 <= self.pelota.x <= 147 and 80 <= self.pelota.y <= 718) or \
        (1305 <= self.pelota.x <= 1449 and 80 <= self.pelota.y <= 718):
            if self.tiempo_espera == 0:
                self.tiempo_espera = 100  # Establece el tiempo de espera después del tiro

    def mensajeGol(self):
        mensaje_grande = "GOL DE LOCAL!" if 0 <= self.pelota.x <= 147 else "GOL DE VISITANTE!"
        if (0 <= self.pelota.x <= 147 and 320 <= self.pelota.y <= 480) or \
        (1305 <= self.pelota.x <= 1449 and 320 <= self.pelota.y <= 480):
            # Mostrar el mensaje en la posición deseada
            font_grande = pygame.font.Font(None, 70)  # Definir una fuente grande
            if mensaje_grande == "GOL DE LOCAL!":
                mensaje_renderizado = font_grande.render(mensaje_grande, True, (255, 0, 0))
            else:
                mensaje_renderizado = font_grande.render(mensaje_grande, True, (0, 0, 255))
            screen.blit(mensaje_renderizado, (525, 12))  # Mostrar el mensaje en la posición (x, y) (coordenadas de ejemplo)

    def reiniciar_posiciones(self):
        # Reinicia la posición de la pelota al centro
        self.pelota.x = self.width / 2
        self.pelota.y = self.height / 2
        self.pelota.rect.x = self.pelota.x - self.pelota.radius
        self.pelota.rect.y = self.pelota.y - self.pelota.radius
        # Reinicia la posición de los jugadores
        for jugador in self.jugadoresLocales + self.jugadoresVisitantes:
            jugador.dibujarPrimeraVez()

        self.tiempo_espera = 0

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
        self.hitbox2 = pygame.Rect(self.width * 0.1, self.height * 0.60, 2, 241 )
        self.hitbox3 = pygame.Rect(self.width * 0.1, self.height * 0.1, 1160, 2 )
        self.hitbox4 = pygame.Rect(self.width * 0.1, self.height * 0.9, 1160, 2 )
        self.hitbox5 = pygame.Rect(self.width * 0.9, self.height * 0.1, 2, 250 )
        self.hitbox6 = pygame.Rect(self.width * 0.9, self.height * 0.60, 2, 241 )

    def dibujar_limites(self):
        pygame.draw.rect(self.screen, self.line_color, (self.width * 0.1, self.height * 0.1, self.width * 0.8, self.height * 0.8), 3)
        #self.dibujar_hitboxes() #opcional

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
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox1, 2)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox2, 2)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox3, 2)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox4, 2)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox5, 2)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox6, 2)  


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
        self.velocidad = 10
        self.direccion_x = 0
        self.direccion_y = 0
        self.limites = LimitesCancha() 
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius) # Rectángulo para colisiones

    def dibujar_pelota(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

    def patear(self, jugador):
            jugador.obtener_pelota()
            self.direccion_x = jugador.direccion_x
            self.direccion_y = jugador.direccion_y
            #Si el proximo movimiento se va fuera de la cancha cambia la direccion
            if (self.x + (self.direccion_x * self.velocidad)) <= self.limites.limite_izquierdo() or (self.x + (self.direccion_x * self.velocidad)) >= self.limites.limite_derecho():
                self.direccion_x *= -1
            if (self.y + (self.direccion_y * self.velocidad)) <= self.limites.limite_superior() or (self.y + (self.direccion_y * self.velocidad)) >= self.limites.limite_inferior():
               self.direccion_y *= -1

            self.x += self.direccion_x  * self.velocidad
            self.y += self.direccion_y * self.velocidad

            jugador.patear_arco_rival(self)
            jugador.mover_area_contraria()

            jugador.perder_pelota()

            self.rect.x = self.x - self.radius
            self.rect.y = self.y - self.radius

    def dibujar_hitbox(self): #Opcional
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)  # Dibujar la hitbox de la pelota
        
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
        self.tiene_pelota = False
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

    def moverse(self):
            # Cambiar de dirección aleatoriamente
            if random.random() < 0.02:  # Probabilidad de cambio de dirección
                self.direccion_x = random.choice([-1, 1])
                self.direccion_y = random.choice([-1, 1])

            # Revisar límites y cambiar dirección si se sale de los límites
            if (self.x + self.direccion_x * self.velocidad) <= self.limite_izquierdo or (self.x + self.direccion_x * self.velocidad) >= self.limite_derecho:
                self.direccion_x *= -1
            if (self.y + self.direccion_y * self.velocidad) <= self.limite_superior or (self.y + self.direccion_y * self.velocidad) >= self.limite_inferior:
                self.direccion_y *= -1

            # Mover en la dirección actual
            self.x += self.direccion_x * self.velocidad
            self.y += self.direccion_y * self.velocidad

            
            self.rect = pygame.Rect(self.x-5, self.y-5, 10, 10)

    def mover_area_contraria(self):
        if self.equipo == 'local':
            if self.x < 400:
                self.x += 1
        else:
            if self.x > 1050:
                self.x -= 1

    def dibujar_hitbox(self): #Opcional
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)  # Dibujar la hitbox del jugador

    def buscar_pelota(self, pelota):
        # Calcular la distancia entre el jugador y la pelota
        distancia_x = pelota.x - self.x
        distancia_y = pelota.y - self.y
        distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5

        # Si el jugador está lejos de la pelota, moverse hacia ella con velocidad constante
        if distancia > 20:  # Ejemplo: 20 es la distancia mínima para que el jugador inicie el movimiento
            # Calcular la dirección hacia la pelota
            direccion_x = distancia_x / distancia
            direccion_y = distancia_y / distancia

            # Mover en la dirección de la pelota con una velocidad constante
            self.x += direccion_x * self.velocidad
            self.y += direccion_y * self.velocidad

            # Actualizar la posición del rectángulo de colisión
            self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

    def obtener_pelota(self):
        self.tiene_pelota = True

    def perder_pelota(self):
        self.tiene_pelota = False

    def verificar_si_tiene_pelota(self):
        return self.tiene_pelota
    
    
    def patear_arco_rival(self, pelota):
        if self.tiene_pelota:
            if (self.equipo == 'local' and self.x > 1120 and 250 < self.y < 500) or \
                    (self.equipo == 'visitante' and self.x < 330 and 250 < self.y < 500):
                if self.equipo == 'local':
                    pelota.direccion_x = 1  # Dirección hacia el arco rival (simulación de patear)
                else:
                    pelota.direccion_x = -1  # Dirección hacia el arco rival (simulación de patear)
                
                # Ajustar la velocidad de la pelota hacia adelante
                pelota.direccion_y = random.uniform(-1, 1)  # Cambio en la dirección vertical
                pelota.velocidad = 100  # Incremento en la velocidad

                # Mover la pelota en la dirección y velocidad establecidas
                pelota.x += pelota.direccion_x * pelota.velocidad
                pelota.y += pelota.direccion_y * pelota.velocidad

                # Actualizar la posición del rectángulo de colisión de la pelota
                pelota.rect.x = pelota.x - pelota.radius
                pelota.rect.y = pelota.y - pelota.radius

                # Perder la posesión de la pelota después de patear
                self.perder_pelota()
                pelota.velocidad = 10  # Restaurar la velocidad de la pelota

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

    def dibujarPrimeraVez(self):
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
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)

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
        campo.chequear_colision_arco()

        if campo.tiempo_espera > 0:
            campo.tiempo_espera -= 1
            if campo.tiempo_espera == 0:
                campo.reiniciar_posiciones()

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
#Chequear bordes de la cancha DONE
#Strategy de movimiento (Una posible hecha)