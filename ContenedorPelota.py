class ContenedorPelota:
    #_instancia = None

    #def __new__(cls):
    #    if not cls._instancia:
    #        cls._instancia = super(ContenedorPelota, cls).__new__(cls)
    #    return cls._instancia

    #def __init__(self):
    #    if not hasattr(self, 'inicializado'):
    #        self.inicializar()
    #        self.inicializado = True
            
    def __init__(self):
        self.jugador_actual = None

    def asociar_pelota(self, jugador):
        if self.jugador_actual is not None:
            self.jugador_actual.desasociar_pelota()
        self.jugador_actual = jugador
        jugador.asociar_pelota(self)


    
