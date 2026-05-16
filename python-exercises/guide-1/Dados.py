import random

class Dado:

    def __init__(self, caras):
        self.caras = caras
        self.valorActual = 1

    def lanzar(self):
        self.valorActual = random.randint(1, self.caras)
        return self.valorActual

    def obtenerValor(self):
        return self.valorActual


dado1 = Dado(6)
dado2 = Dado(20)

print("Lanzamiento dado1:", dado1.lanzar())
print("Valor actual dado1:", dado1.obtenerValor())

print("Lanzamiento dado2:", dado2.lanzar())
print("Valor actual dado2:", dado2.obtenerValor())