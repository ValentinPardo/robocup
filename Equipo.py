class Equipo:
    def __init__(self, formacion, strategy):
        self.formacion = formacion
        self.jugadores = []
        self.strategy = strategy

    def estrategia(self):
        # Implementa aquí la lógica de la estrategia del equipo
        pass

    def agregarJugador(self, jugador):
        # Implementa aquí la lógica para agregar un jugador al equipo
        self.jugadores.append(jugador)
    
    def jugadores(self):
        return self.jugadores