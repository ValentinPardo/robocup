import math
import pygame
import random

equipoConPelota = ''

class Jugador:
    def __init__(self, coordenadas, pelota, bando, equipo):
        self.velocidad = 0.001
        self.velocidadRotacion = 0
        self.tienePelota = False
        self.pelota = pelota
        self.bando = bando
        self.equipo = equipo
        self.primeraPosicion(coordenadas)
        self.jugador_view = None
        self.juegoActivo = True
        self.hitbox = pygame.Rect(self.coordenadas[0] - 10, self.coordenadas[1] - 10, 20, 20)

    def primeraPosicion(self, coordenadas):
        if self.bando == 'local':
            self.coordenadas = [400, coordenadas]
        else:
            self.coordenadas = [1050, coordenadas]

    def comportamiento(self):
        global equipoConPelota
        # Logica de lo que hace el jugador en cada situacion
        while self.juegoActivo:
            # Si no tiene la pelota
            if not self.tienePelota and equipoConPelota != self.bando:
                self.sinPelota()
            # Si su equipo tiene la pelota
            elif not self.tienePelota and equipoConPelota == self.bando:
                self.equipoConPosesion()
            # Si tiene la pelota
            elif self.tienePelota:
                self.conPelota()
            try:
                self.notificar()
            except:
                pass

    def correr(self,angulo_radianes):
        # Implementación del método correr
        
        #Calculo la nueva posicion del jugador
        self.coordenadas[0] += math.cos(angulo_radianes) * self.velocidad
        self.coordenadas[1] += math.sin(angulo_radianes) * self.velocidad
        self.hitbox = pygame.Rect(self.coordenadas[0] - 10, self.coordenadas[1] - 10, 20, 20)
        
    def patear(self,angulo_radianes):
        # Implementación del método patear
        global equipoConPelota
        pelota = self.pelota
        self.perderPelota()
        variacion_radianes = random.uniform(math.radians(-30),math.radians(30))
        anguloNuevo = angulo_radianes + variacion_radianes
        while equipoConPelota == '':
            pelota.esPateada(anguloNuevo)
            if pelota.coordenadas[0] > 1305: #si la pelota sale de la cancha se asigna a un equipo para terminar el while
                equipoConPelota = 'local'
            if pelota.coordenadas[0] < 132:
                equipoConPelota = 'visitante'
            
    def pasar(self):
        i = random.randint(0,100000)
        if i == 978: #probabilidad de pasar la pelota
            size = self.equipo.cantidadJugadores()-1
            jugadorDestino = self.equipo.jugadores[random.randint(0,size)]
            if self.bando == 'local':
                if jugadorDestino.coordenadas[0] > self.coordenadas[0]:
                    self.perderPelota()
                    jugadorDestino.obtenerPelota()
            elif self.bando == 'visitante':
                if jugadorDestino.coordenadas[0] > self.coordenadas[0]:
                    self.perderPelota()
                    jugadorDestino.obtenerPelota()

    def rotar(self):
        # Implementación del método rotar
        angulo_radianes = math.atan2(self.pelota.coordenadas[1] - self.coordenadas[1], self.pelota.coordenadas[0] - self.coordenadas[0])
        
        self.pelota.setPos(self.coordenadas, angulo_radianes + 0.00001)
    
    def obtenerPelota(self):
        self.tienePelota = True
        global equipoConPelota
        equipoConPelota = self.bando

    def perderPelota(self):
        # Implementación del método perderPelota
        self.tienePelota = False
        global equipoConPelota
        equipoConPelota = ''

    def sinPelota(self):

        #Calculo la distancia entre el jugador y la pelota
        distancia_x = self.pelota.coordenadas[0] - self.coordenadas[0]
        distancia_y = self.pelota.coordenadas[1] - self.coordenadas[1]
        angulo_radianes = math.atan2(distancia_y, distancia_x)
        #distancia = math.sqrt(distancia_x**2 + distancia_y**2)

        self.correr(angulo_radianes)
      
    def conPelota(self):
        # Implementación del método conPelota
        if self.bando == 'local':
            area = (1300, 400)
        else:
            area = (150,400)
        
        distancia_x = area[0] - self.coordenadas[0]
        distancia_y = area[1] - self.coordenadas[1]
        angulo_radianes = math.atan2(distancia_y, distancia_x)

        #si la distancia al arco es menor a 150 patea
        if (math.sqrt(distancia_x**2 + distancia_y**2)) < 150:
            self.patear(angulo_radianes)
        else: 
            self.pelota.setPos(self.coordenadas,angulo_radianes)
            self.correr(angulo_radianes)
            self.pasar()

    def equipoConPosesion(self):
        # Implementación del método equipoConPosesion
        distancia_x = self.pelota.coordenadas[0] - self.coordenadas[0]
        distancia_y = self.pelota.coordenadas[1] - self.coordenadas[1]
        angulo_radianes = math.atan2(distancia_y, distancia_x)

        #calcular hipotenusa
        distancia = math.sqrt(distancia_x**2 + distancia_y**2)
        if ( distancia ) < 100:
            self.correr((-angulo_radianes))
        else:
            self.correr(angulo_radianes)
        
    def setearGlobal(self,equipo):
        global equipoConPelota
        equipoConPelota = equipo


    def getPos(self):
        # Implementación del método getPos
        pass

    def obtenerHitbox(self):
        # Implementación del método obtenerHitbox
        return self.hitbox

    def suscribir(self, jugadorView):
        # Implementación del método suscribir
        self.jugador_view = jugadorView

    def notificar(self):
        # Implementación del método notificar
        self.jugador_view.actualizar_coordenadas(self.coordenadas, self.hitbox)

    def quit(self):
        self.juegoActivo = False
        

class Arquero(Jugador):
    def primeraPosicion(self, coordenadas):
        if self.bando == 'local':
            self.coordenadas = [150, 390]
        else:
            self.coordenadas = [1297, 390]

    def comportamiento(self):
        direccion = 'DOWN'
        while self.juegoActivo:
            if not self.tienePelota:
                self.moverArco(direccion)
                if self.coordenadas[1] == 480:
                    direccion = self.invertirDireccion(direccion)
                if self.coordenadas[1] == 320:
                    direccion = self.invertirDireccion(direccion)
            elif self.tienePelota:
                self.pasar()
            try:
                self.notificar()
            except:
                pass

    def moverArco(self, direccion):
        # Implementación del movimiento automático del arquero de arriba a abajo dentro del arco
        limite_superior = 320
        limite_inferior = 480

        if direccion == 'DOWN':
            if self.coordenadas[1] + self.velocidad <= limite_inferior:
                self.correr(math.radians(90))
            else:
                self.coordenadas[1] = limite_inferior  # Ajusta a la posición límite inferior
        elif direccion == 'UP':
            if self.coordenadas[1] - self.velocidad >= limite_superior:
                self.correr(math.radians(270))
            else:
                self.coordenadas[1] = limite_superior  # Ajusta a la posición límite superior

    def invertirDireccion(self, direccion):
        # Cambia la dirección (de 'UP' a 'DOWN' o viceversa)
        return 'DOWN' if direccion == 'UP' else 'UP'

    def atajar(self):
        # Implementación específica del método atajar para Arquero
        pass

class Defensor(Jugador):
    def primeraPosicion(self, coordenadas):
        if self.bando == 'local':
            self.coordenadas = [300, coordenadas]
        else:
            self.coordenadas = [1150, coordenadas]

    #def comportamiento(self):
    #    # Implementación específica del comportamiento para Defensor
    #    pass

    def defender(self):
        # Implementación específica del método defender para Defensor
        pass

class Mediocampista(Jugador):
    def primeraPosicion(self, coordenadas):
        if self.bando == 'local':
            self.coordenadas = [500, coordenadas]
        else:
            self.coordenadas = [930, coordenadas]

    #def comportamiento(self):
    #    # Implementación específica del comportamiento para Mediocampista
    #    pass

    def distribuirBalon(self):
        # Implementación específica del método distribuirBalon para Mediocampista
        pass

class Delantero(Jugador):
    def primeraPosicion(self, coordenadas):
        if self.bando == 'local':
            self.coordenadas = [651, coordenadas]
        else:
            self.coordenadas = [797, coordenadas]

    #def comportamiento(self):
    #    # Implementación específica del comportamiento para Delantero
    #    pass

    def marcarGol(self):
        # Implementación específica del método marcarGol para Delantero
        pass
