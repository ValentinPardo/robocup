from Views import *
import Limites
import Jugador
import threading

class Juego:
    def __init__(self, equipo1, equipo2, limites):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.limites = limites

    def Jugar(self):
        # Lógica para jugar el juego
        self.limites = Limites(0, 0, 0, 0)
        Campo = CampoView(Limites)
        Campo.crearCampo()
        Pelota = Pelota()
        PelotaView = PelotaView()
        Pelota.suscribir(PelotaView)
        for i in range(5):
            Jugador = Jugador()
            jugadorView = JugadorView()
            Jugador.suscribir(jugadorView)
            self.equipo1.agregarJugador(Jugador)
            thread = threading.Thread(target=Jugador.comportamiento(), args=())
            thread.start()
        for i in range(5):
            Jugador = Jugador()
            jugadorView = JugadorView()
            Jugador.suscribir(jugadorView)
            self.equipo2.agregarJugador(Jugador)
            thread = threading.Thread(target=Jugador.comportamiento(), args=())
            thread.start()
        
        pass
