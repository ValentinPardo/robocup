from Jugador import *

class Equipo:
    def __init__(self, strategy, bando):
        self.jugadores = []
        self.strategy = strategy
        self.bando = bando

    def crearJugadores(self, coordenada, pelota, contenedor, i):
        formacion = self.strategy.formacion()
        clase_jugador = formacion[i]

        # Mapear el tipo de jugador a la clase correspondiente
        tipos_clases_jugador = {
            'Arquero': Arquero,
            'Defensor': Defensor,
            'Mediocampista': Mediocampista,
            'Delantero': Delantero
        }
        
        tipo_jugador = tipos_clases_jugador[clase_jugador]
        return tipo_jugador(coordenada, pelota, self.bando, self, contenedor)


    def agregarJugador(self, jugador):
        self.jugadores.append(jugador)
    
    def jugadores(self):
        return self.jugadores
    
    def cantidadJugadores(self):
        return len(self.jugadores)
    
class Strategy:
    def formacion(self):
        # Método a implementar por cada estrategia
        pass

class StrategyDefensiva(Strategy):
    def formacion(self):
        return ['Arquero', 'Defensor', 'Defensor', 'Mediocampista', 'Delantero']


class StrategyOfensiva(Strategy):
    def formacion(self):
        return ['Arquero', 'Defensor', 'Mediocampista', 'Mediocampista', 'Delantero']

