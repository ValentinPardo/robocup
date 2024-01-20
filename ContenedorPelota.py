class Contenedor:
    def __init__(self, pelota):
        self.pelota = pelota
        self.jugador = None

    def asociar(self, jugador):
        if self.jugador == None:
            self.jugador = jugador
            jugador.obtenerPelota()
        else:
            self.jugador.perderPelota()
            self.desasociar()
            self.jugador = jugador
            jugador.obtenerPelota()

    def desasociar(self):
        self.jugador = None
