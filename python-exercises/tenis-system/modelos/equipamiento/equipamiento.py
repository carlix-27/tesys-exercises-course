from abc import ABC, abstractmethod


class Equipamiento(ABC):
    """Clase abstracta base para todo equipamiento de tenis."""

    def __init__(self, tipo: str):
        self._tipo = tipo

    @property
    def tipo(self) -> str:
        return self._tipo

    @abstractmethod
    def get_descripcion(self) -> str:
        pass
