from Views import *
from Limites import Limites
import threading
from Pelota import Pelota
from Jugador import Jugador
from Equipo import Equipo
from ContenedorPelota import Contenedor
import random

class Juego:
    def __init__(self):
        self.equipo1 = None
        self.equipo2 = None
        pass

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
        coordenadas = [210, 310, 410, 510, 610]
        self.equipo1 = Equipo('4-3-3', 'estrategia')
        self.equipo2 = Equipo('4-3-3', 'estrategia')
        jugadorViews = []
        for i in range(3):
            jugador = Jugador(coordenadas[i], 'delantero', pelota, 'local')
            jugadorView = JugadorView('local', i + 1)
            jugador.suscribir(jugadorView)
            self.equipo1.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        for i in range(0):
            jugador = Jugador(coordenadas[i], 'delantero', pelota, 'visitante')
            jugadorView = JugadorView('visitante',i + 1)
            jugador.suscribir(jugadorView)
            self.equipo2.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        while running[0]:
            campo.actualizar(jugadorViews, pelotaView, running, marcador)
            self.chequear_colisiones(pelota,contenedor)
            if limites.verificar_gol(pelota.coordenadas, marcador):
                #Reiniciar jugadores y pelota (incompleto)
                self.reiniciar_posiciones(pelota, coordenadas)
                contenedor.desasociar()

        campo.quit() #terminar visualizacion
        self.quit() #terminar modelo
        
    def quit(self):
        for i in self.equipo1.jugadores:
            i.quit()
        for i in self.equipo2.jugadores:
            i.quit()

    def reiniciar_posiciones(self, pelota, coordenadas):
        # Lógica para reiniciar las posiciones de la pelota y los jugadores
        i = 0
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.primeraPosicion(coordenadas[i % 5])
            i+=1
            pass #Logica de primera posicion para jugadores def, medio, del, arq

        pelota.coordenadas = [725, 400]  # Reiniciar posición de la pelota

    #este chequeo se va a tener q hacer en views ya que se necesita de un bucle que chequee constantemente
    def chequear_colisiones(self, pelota, contenedor):
        # Check for collisions between the ball and the players
        jugadores = self.equipo2.jugadores + self.equipo1.jugadores
        random.shuffle(jugadores)  # Randomly shuffle the players array

        for jugador in jugadores:
            if jugador.obtenerHitbox().colliderect(pelota.obtenerHitbox()):
                contenedor.asociar(jugador)


jugar = Juego()
jugar.Jugar()
