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
        limites = Limites((150,1300),80,720, (80,720), 150, 1300)
        campo = CampoView(limites,self)
        pelota = Pelota()
        pelotaView = PelotaView()
        pelota.suscribir(pelotaView)
        coordenadas = [210, 310, 410, 510, 610]
        self.equipo1 = Equipo('4-3-3', 'estrategia')
        self.equipo2 = Equipo('4-3-3', 'estrategia')
        for i in range(5):
            jugador = Jugador(coordenadas[i], 'delantero', pelota, 'local')
            jugadorView = JugadorView()
            jugador.suscribir(jugadorView)
            self.equipo1.agregarJugador(jugador)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        for i in range(5):
            jugador = Jugador(coordenadas[i], 'delantero', pelota, 'visitante')
            jugadorView = JugadorView()
            jugador.suscribir(jugadorView)
            self.equipo2.agregarJugador(jugador)
            thread = threading.Thread(target=jugador.comportamiento, args=())
            thread.start()
        campo.actualizar()
    
    def quit(self):
        for i in self.equipo1.jugadores:
            i.quit()
        for i in self.equipo2.jugadores:
            i.quit()

jugar = Juego()
jugar.Jugar()
