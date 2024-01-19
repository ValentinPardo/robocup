from Views import *
from Limites import Limites
import threading
from Pelota import Pelota
from Jugador import Jugador
from Equipo import Equipo

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
        pelotaView = PelotaView()
        pelota.suscribir(pelotaView)
        coordenadas = [210, 310, 410, 510, 610]
        self.equipo1 = Equipo('4-3-3', 'estrategia')
        self.equipo2 = Equipo('4-3-3', 'estrategia')
        jugadorViews = []
        for i in range(2):
            jugador = Jugador(coordenadas[i], 'delantero', pelota, 'local')
            jugadorView = JugadorView('local')
            jugador.suscribir(jugadorView)
            self.equipo1.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        for i in range(2):
            jugador = Jugador(coordenadas[i], 'delantero', pelota, 'visitante')
            jugadorView = JugadorView('visitante')
            jugador.suscribir(jugadorView)
            self.equipo2.agregarJugador(jugador)
            jugadorViews.append(jugadorView)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        while running[0]:
            campo.actualizar(jugadorViews, pelotaView,running)
            self.chequear_colisiones(pelota)

        campo.quit() #terminar visualizacion
        self.quit() #terminar modelo
        
    def quit(self):
        for i in self.equipo1.jugadores:
            i.quit()
        for i in self.equipo2.jugadores:
            i.quit()

    #este chequeo se va a tener q hacer en views ya que se necesita de un bucle que chequee constantemente
    def chequear_colisiones(self, pelota):
        # Implementación del método chequear_colisiones
        for jugador in self.equipo1.jugadores:
            if jugador.obtenerHitbox().colliderect(pelota.obtenerHitbox()):
                pelota.obtenida(jugador)
        for jugador in self.equipo2.jugadores:
            if jugador.obtenerHitbox().colliderect(pelota.obtenerHitbox()):
                pelota.obtenida(jugador)

jugar = Juego()
jugar.Jugar()
