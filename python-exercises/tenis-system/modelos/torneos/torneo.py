from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from modelos.personas.jugador import Jugador

if TYPE_CHECKING:
    from modelos.partido import Partido


class Torneo(ABC):
    """
    Clase abstracta Torneo.
    Define el contrato que todas las subclases deben cumplir.

    HERENCIA + POLIMORFISMO:
      Cada subclase implementa sus propias reglas de puntos,
      límite de participantes y tipo de jugador permitido.

    Superficies válidas: Pasto | Arcilla | Cemento Duro
    Formato de fecha:    YYYY-MM-DD
    """

    SUPERFICIES_VALIDAS = {"Pasto", "Arcilla", "Cemento Duro"}

    def __init__(self, nombre: str, pais: str, superficie: str, fecha: str):
        # TODO: validar superficie en SUPERFICIES_VALIDAS → ValueError("La superficie debe ser: ...")
        # TODO: validar formato de fecha YYYY-MM-DD con regex → ValueError("El formato de fecha debe ser YYYY-MM-DD")
        self._nombre = nombre
        self._pais = pais
        self._superficie = superficie
        self._fecha = fecha
        self._participantes: list[Jugador] = []
        self._partidos: list["Partido"] = []

    # -------------------------------------------------------------------------
    # Propiedades
    # -------------------------------------------------------------------------

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def pais(self) -> str:
        return self._pais

    @property
    def superficie(self) -> str:
        return self._superficie

    @property
    def fecha(self) -> str:
        return self._fecha

    def get_participantes(self) -> list:
        return self._participantes

    # -------------------------------------------------------------------------
    # Gestión de participantes
    # -------------------------------------------------------------------------

    def agregar_jugador(self, jugador: Jugador) -> None:
        # TODO (en orden):
        #   1. Llamar a validar_jugador(jugador) — lanza excepción si no aplica
        #   2. Verificar que jugador no esté ya en _participantes → ValueError("El jugador ya está registrado")
        #   3. Verificar que no se supere get_max_participantes() → ValueError("Máximo X jugadores...")
        #   4. Agregar a _participantes
        self._participantes.append(jugador)

    def registrar_partido(self, partido: "Partido") -> None:
        self._partidos.append(partido)

    # -------------------------------------------------------------------------
    # Métodos concretos
    # -------------------------------------------------------------------------

    def generar_reporte(self) -> str:
        # TODO: retornar string con:
        #   nombre, tipo, país, superficie, fecha, cantidad de participantes
        # Ejemplo:
        #   === Roland Garros ===
        #   Tipo: Grand Slam | País: Francia | Superficie: Arcilla
        #   Fecha: 2024-05-26 | Participantes: 2
        pass

    # -------------------------------------------------------------------------
    # Métodos abstractos — contrato para subclases
    # -------------------------------------------------------------------------

    @abstractmethod
    def get_tipo(self) -> str:
        """Retorna el nombre del tipo de torneo."""
        pass

    @abstractmethod
    def get_puntos_para_ganador(self) -> int:
        """Puntos ATP/WTA que recibe el campeón."""
        pass

    @abstractmethod
    def get_puntos_para_finalista(self) -> int:
        """Puntos ATP/WTA que recibe el subcampeón."""
        pass

    @abstractmethod
    def get_max_participantes(self) -> int:
        """Límite máximo de jugadores en el torneo."""
        pass

    @abstractmethod
    def validar_jugador(self, jugador: Jugador) -> None:
        """
        Verifica si el jugador puede participar en este torneo.
        Lanza ValueError si no cumple las condiciones.
        """
        pass
