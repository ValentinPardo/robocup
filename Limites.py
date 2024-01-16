class Limites:
    def __init__(self, laterales_x,lateralInferior_y, lateralSuperior_y, fondos_y ,fondoIzquierdo_x, fondoDerecho_x):
        self.laterales_x = laterales_x
        self.lateralInferior_y = lateralInferior_y
        self.lateralSuperior_y = lateralSuperior_y
        self.fondos_y = fondos_y
        self.fondoIzquierdo_x = fondoIzquierdo_x
        self.fondoDerecho_x = fondoDerecho_x

    def getLatSup(self):
        return self.lateralSuperior

    def getLatInf(self):
        return self.lateralInferior

    def getFonIzq(self):
        return self.fondoIzquierdo

    def getFonDer(self):
        return self.fondoDerecho
