from Views import *
from Limites import Limites
import threading
from Pelota import Pelota
from Jugador import *
from Equipo import Equipo
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
        coordenadas = [210, 310, 410, 510, 610]
        self.equipo1 = Equipo('4-3-3', 'estrategia')
        self.equipo2 = Equipo('4-3-3', 'estrategia')
        jugadorViews = []
        #EQUIPO LOCAL
        for i in range(2):
            if i == 0:
                jugador = Arquero(coordenadas[i], pelota, 'local', self.equipo1)
            elif i == 1 or i == 2:
                jugador = Defensor(coordenadas[i], pelota, 'local', self.equipo1)
            elif i == 3:
                jugador = Mediocampista(coordenadas[i], pelota, 'local', self.equipo1)
            elif i == 4:
                jugador = Delantero(coordenadas[i], pelota, 'local', self.equipo1)
            jugadorView = JugadorView('local', i + 1)
            jugador.suscribir(jugadorView)
            self.equipo1.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        #EQUIPO VISITANTE
        for i in range(2):
            if i == 0:
                jugador = Arquero(coordenadas[i], pelota, 'visitante', self.equipo2)
            elif i == 1 or i == 2:
                jugador = Defensor(coordenadas[i], pelota, 'visitante', self.equipo2)
            elif i == 3:
                jugador = Mediocampista(coordenadas[i], pelota, 'visitante', self.equipo2)
            elif i == 4:
                jugador = Delantero(coordenadas[i], pelota, 'visitante', self.equipo2)
            jugadorView = JugadorView('visitante',i + 1)
            jugador.suscribir(jugadorView)
            self.equipo2.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        while running[0]:
            campo.actualizar(jugadorViews, pelotaView, running, marcador)
            self.chequear_colisiones(pelota,contenedor, coordenadas)
            if limites.verificar_gol(pelota.coordenadas, marcador):
                #Reiniciar jugadores y pelota (incompleto)
                contenedor.desasociar()
                self.reiniciar_posiciones(pelota, coordenadas)
            #print(int(pygame.time.get_ticks()/1000)) Metodo para obtener tiempo desde inicio

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
            jugador.notificar()
            jugador.perderPelota()
            i += 1

        # Reiniciar posición de la pelota
        pelota.velocidad = 0
        pelota.setPos([715, 400], 0)


    #este chequeo se va a tener q hacer en views ya que se necesita de un bucle que chequee constantemente
    def chequear_colisiones(self, pelota, contenedor, coordenadas):
        # Check for collisions between the ball and the players
        jugadores = self.equipo2.jugadores + self.equipo1.jugadores
        random.shuffle(jugadores)  # Randomly shuffle the players array

        for jugador in jugadores:
            if jugador.obtenerHitbox().colliderect(pelota.obtenerHitbox()):
                if pelota.tiempoUltimoRobo < 0 and jugador.tienePelota == False:
                    contenedor.asociar(jugador) 
                else:
                    pelota.tiempoUltimoRobo -= 1

jugar = Juego()
jugar.Jugar()
