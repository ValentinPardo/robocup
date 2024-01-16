from Views import *
from Limites import Limites
import threading
from Pelota import Pelota
from Jugador import Jugador
from Equipo import Equipo

class Juego:
    def __init__(self):
        pass

    def Jugar(self):
        # Lógica para jugar el juego
        limites = Limites((150,1300),80,720, (80,720), 150, 1300)
        campo = CampoView(limites)
        pelota = Pelota()
        pelotaView = PelotaView()
        pelota.suscribir(pelotaView)
        coordenadas = (550, 550)
        equipo1 = Equipo('4-3-3', 'estrategia')
        equipo2 = Equipo('4-3-3', 'estrategia')
        for i in range(5):
            jugador = Jugador(coordenadas, 'delantero')
            jugadorView = JugadorView()
            jugador.suscribir(jugadorView)
            equipo1.agregarJugador(jugador)
            thread = threading.Thread(target=jugador.comportamiento, args=())  # Quitamos los paréntesis de comportamiento
            thread.start()
        for i in range(5):
            jugador = Jugador(coordenadas, 'delantero')
            jugadorView = JugadorView()
            jugador.suscribir(jugadorView)
            equipo2.agregarJugador(jugador)
            thread = threading.Thread(target=jugador.comportamiento, args=())  # Quitamos los paréntesis de comportamiento
            thread.start()

        campo.actualizar()

jugar = Juego()
jugar.Jugar()
