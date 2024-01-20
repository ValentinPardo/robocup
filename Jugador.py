import math
import pygame

class Jugador:
    def __init__(self, coordenadas, posicion,pelota ,bando):
        self.angulo = 0
        self.velocidad = 0.001
        self.velocidadRotacion = 0.5
        self.posicion = posicion
        self.tienePelota = False
        self.pelota = pelota
        self.bando = bando
        if self.bando == 'local':
            self.coordenadas = [400,coordenadas]
        else:
            self.coordenadas = [1050,coordenadas]
        self.jugador_view = None
        self.juegoActivo = True
        self.hitbox = pygame.Rect(self.coordenadas[0] - 10, self.coordenadas[1] - 10, 20, 20)

    def comportamiento(self):
        # Logica de lo que hace el jugador en cada situacion
        while self.juegoActivo:
            # Si no tiene la pelota
            if not self.tienePelota: #and equipoNoTienePelota
                self.sinPelota()
            # Si su equipo tiene la pelota
            elif not self.tienePelota: #and equipoTienePelota
                self.equipoConPosesion()
            # Si tiene la pelota
            else:
                self.conPelota()
            try:
                self.notificar()
            except:
                pass

    def correr(self,angulo_radianes):
        # Implementación del método correr
        if self.tienePelota:
            self.pelota.setPos(self.coordenadas,angulo_radianes)
        #Calculo la nueva posicion del jugador
        self.coordenadas[0] += math.cos(angulo_radianes) * self.velocidad
        self.coordenadas[1] += math.sin(angulo_radianes) * self.velocidad
        self.hitbox = pygame.Rect(self.coordenadas[0] - 10, self.coordenadas[1] - 10, 20, 20)
        
    def patear(self):
        # Implementación del método patear
        pass

    def rotar(self):
        # Implementación del método rotar
        pass

    def obtenerPelota(self):
        # Implementación del método obtenerPelota
        self.tienePelota = True

    def sinPelota(self):

        #Calculo la distancia entre el jugador y la pelota
        distancia_x = self.pelota.coordenadas[0] - self.coordenadas[0]
        distancia_y = self.pelota.coordenadas[1] - self.coordenadas[1]
        angulo_radianes = math.atan2(distancia_y, distancia_x)
        distancia = math.sqrt(distancia_x**2 + distancia_y**2)

        if distancia < self.pelota.radio:
            self.obtenerPelota()
        #Roto al jugador con la velocidad de rotacion y el angulo para que mire hacia la pelota
        #self.angulo += self.velocidadRotacion * angulo_radianes

        self.correr(angulo_radianes)
        

    def conPelota(self):
        # Implementación del método conPelota
        self.correr(self.angulo)

    def equipoConPosesion(self):
        # Implementación del método equipoConPosesion
        pass

    def getPos(self):
        # Implementación del método getPos
        pass

    def obtenerHitbox(self):
        # Implementación del método obtenerHitbox
        return self.hitbox

    def obtenerPelota(self):
        self.tienePelota = True

    def suscribir(self, jugadorView):
        # Implementación del método suscribir
        self.jugador_view = jugadorView
        pass

    def notificar(self):
        # Implementación del método notificar
        self.jugador_view.actualizar_coordenadas(self.coordenadas)
        pass

    def quit(self):
        self.juegoActivo = False
        

class Arquero(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Arquero
        pass

    def atajar(self):
        # Implementación específica del método atajar para Arquero
        pass

class Defensor(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Defensor
        pass

    def defender(self):
        # Implementación específica del método defender para Defensor
        pass

class Mediocampista(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Mediocampista
        pass

    def distribuirBalon(self):
        # Implementación específica del método distribuirBalon para Mediocampista
        pass

class Delantero(Jugador):
    def comportamiento(self):
        # Implementación específica del comportamiento para Delantero
        pass

    def marcarGol(self):
        # Implementación específica del método marcarGol para Delantero
        pass
