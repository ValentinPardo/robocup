class Limites:
    def __init__(self, lateralInferior, lateralSuperior, fondoIzquierdo, fondoDerecho):
        self.lateralInferior = lateralInferior
        self.lateralSuperior = lateralSuperior
        self.fondoIzquierdo = fondoIzquierdo
        self.fondoDerecho = fondoDerecho

    def getLatSup(self):
        return self.lateralSuperior

    def getLatInf(self):
        return self.lateralInferior

    def getFonIzq(self):
        return self.fondoIzquierdo

    def getFonDer(self):
        return self.fondoDerecho
