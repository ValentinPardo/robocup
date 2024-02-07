from Views import *
from Limites import Limites
import threading
from Pelota import Pelota
from Jugador import *
from Equipo import *
from ContenedorPelota import Contenedor
import random

class Juego:
    def __init__(self):
        self.equipo1 = None
        self.equipo2 = None 

    def Jugar(self):
        # Lógica para jugar
        running = [True]
        limites = Limites((150,1300),80,720, (80,720), 150, 1300)
        campo = CampoView(limites)
        pelota = Pelota()
        marcador = Marcador()
        contenedor = Contenedor(pelota)
        pelotaView = PelotaView()
        pelota.suscribir(pelotaView)
        coordenadas = [210, 310, 480, 310, 610]
        self.equipo1 = Equipo(StrategyDefensiva() ,'local')
        self.equipo2 = Equipo(StrategyDefensiva(),'visitante')
        jugadorViews = []
        #EQUIPO LOCAL
        for i in range(5):
            jugador = self.equipo1.crearJugadores(coordenadas[i], pelota, contenedor, i)
            jugadorView = JugadorView('local', i + 1)
            jugador.suscribir(jugadorView)
            self.equipo1.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        #EQUIPO VISITANTE
        for i in range(5):
            jugador = self.equipo2.crearJugadores(coordenadas[i], pelota, contenedor, i)
            jugadorView = JugadorView('visitante',i + 1)
            jugador.suscribir(jugadorView)
            self.equipo2.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        while running[0]:
            campo.actualizar(jugadorViews, pelotaView, running, marcador)
            self.chequear_colisiones(pelota, contenedor, coordenadas)
            if limites.verificar_gol(pelota.coordenadas, marcador):
                #Reiniciar jugadores y pelota (incompleto)
                contenedor.desasociar()
                self.reiniciar_posiciones(pelota, coordenadas, contenedor)
                pelota.notificar()

        campo.quit() #terminar visualizacion
        self.quit() #terminar modelo
        
    def quit(self):
        for i in self.equipo1.jugadores:
            i.quit()
        for i in self.equipo2.jugadores:
            i.quit()

    def reiniciar_posiciones(self, pelota, coordenadas, contenedor):
        # Lógica para reiniciar las posiciones de la pelota y los jugadores
        for i, jugador in enumerate(self.equipo1.jugadores + self.equipo2.jugadores):
            jugador.primeraPosicion(coordenadas[i % 5])
            jugador.perderPelota()
            jugador.hitbox = pygame.Rect(jugador.coordenadas[0] - 10, jugador.coordenadas[1] - 10, 20, 20)
            jugador.notificar()
        
        contenedor.desasociar()

        # Reiniciar posición de la pelota
        pelota.inicializar()

    #este chequeo se va a tener q hacer en views ya que se necesita de un bucle que chequee constantemente
    def chequear_colisiones(self, pelota, contenedor, coordenadas):
        # Check for collisions between the ball and the players
        jugadores = self.equipo2.jugadores + self.equipo1.jugadores
        random.shuffle(jugadores)  # Randomly shuffle the players array

        for jugador in jugadores:
            if jugador.obtenerHitbox().colliderect(pelota.obtenerHitbox()):
                if pelota.tiempoUltimoRobo <= 0 and jugador.tienePelota == False:
                    contenedor.asociar(jugador) 
                else:
                    pelota.tiempoUltimoRobo -= 1

jugar = Juego()
jugar.Jugar()
