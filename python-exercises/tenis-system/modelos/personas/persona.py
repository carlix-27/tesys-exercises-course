from abc import ABC, abstractmethod


class Persona(ABC):
    """
    Clase abstracta base para todas las personas del sistema.
    Define atributos comunes: nombre, edad, país.
    """

    def __init__(self, nombre: str, edad: int, pais: str):
        # TODO: validar que nombre no esté vacío → ValueError("El nombre no puede estar vacío")
        # TODO: validar que edad sea un entero positivo → ValueError
        # TODO: validar que pais no esté vacío → ValueError("El país no puede estar vacío")
        self._nombre = nombre
        self._edad = edad
        self._pais = pais

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def edad(self) -> int:
        return self._edad

    @property
    def pais(self) -> str:
        return self._pais

    @abstractmethod
    def get_descripcion(self) -> str:
        pass
