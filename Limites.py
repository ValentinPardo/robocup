import pygame

class Limites:
    def __init__(self, laterales_x,lateralInferior_y, lateralSuperior_y, fondos_y ,fondoIzquierdo_x, fondoDerecho_x):
        self.laterales_x = laterales_x
        self.lateralInferior_y = lateralInferior_y
        self.lateralSuperior_y = lateralSuperior_y
        self.fondos_y = fondos_y
        self.fondoIzquierdo_x = fondoIzquierdo_x
        self.fondoDerecho_x = fondoDerecho_x
        self.arco_local = pygame.Rect(self.fondoIzquierdo_x - 18, 320, 15, 160)
        self.arco_visitante = pygame.Rect(self.fondoDerecho_x + 5, 320, 15, 160)

    def getLatSup(self):
        return self.lateralSuperior

    def getLatInf(self):
        return self.lateralInferior

    def getFonIzq(self):
        return self.fondoIzquierdo

    def getFonDer(self):
        return self.fondoDerecho

    def verificar_gol(self, coordenadas_pelota, marcador):
        # Verifica si la pelota está dentro de la hitbox de alguno de los arcos
        if self.arco_local.collidepoint(coordenadas_pelota):
            marcador.gol_visitante()
            return True
        elif self.arco_visitante.collidepoint(coordenadas_pelota):
            marcador.gol_local()
            return True
        return False
