from modelos.personas.jugador import Jugador
from modelos.equipamiento.superficie import Superficie
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelos.torneos.torneo import Torneo


class Partido:
    """
    Representa un enfrentamiento entre dos jugadores.

    COMPOSICIÓN: Partido TIENE dos Jugadores y una Superficie.
    ASOCIACIÓN:  Partido pertenece a un Torneo.

    Un partido sin jugadores no tiene sentido → validar en constructor.
    """

    MAX_SETS = 5

    def __init__(
        self,
        jugador1: Jugador,
        jugador2: Jugador,
        superficie: Superficie,
        torneo: "Torneo",
        fecha: str,
    ):
        # TODO: validar que jugador1 is not jugador2 → ValueError("Los dos jugadores deben ser diferentes")
        # TODO: validar formato de fecha YYYY-MM-DD  → ValueError("El formato de fecha debe ser YYYY-MM-DD")
        self._jugador1 = jugador1
        self._jugador2 = jugador2
        self._superficie = superficie
        self._torneo = torneo
        self._fecha = fecha
        # Cada elemento: {"juegos1": int, "juegos2": int}
        self._resultados: list[dict] = []
        self._aces = 0
        self._errores_no_forzados = 0
        self._tiros_ganadores = 0

    # -------------------------------------------------------------------------
    # Getters
    # -------------------------------------------------------------------------

    def get_jugador1(self) -> Jugador:
        return self._jugador1

    def get_jugador2(self) -> Jugador:
        return self._jugador2

    def get_superficie(self) -> Superficie:
        return self._superficie

    def get_torneo(self) -> "Torneo":
        return self._torneo

    def get_resultados(self) -> list:
        return self._resultados

    def get_aces(self) -> int:
        return self._aces

    def set_aces(self, aces: int) -> None:
        self._aces = aces

    def get_errores_no_forzados(self) -> int:
        return self._errores_no_forzados

    def set_errores_no_forzados(self, errores: int) -> None:
        self._errores_no_forzados = errores

    def get_tiros_ganadores(self) -> int:
        return self._tiros_ganadores

    def set_tiros_ganadores(self, tiros: int) -> None:
        self._tiros_ganadores = tiros

    # -------------------------------------------------------------------------
    # Lógica principal
    # -------------------------------------------------------------------------

    def registrar_set(self, juegos1: int, juegos2: int) -> None:
        # TODO: validar que len(_resultados) < MAX_SETS → ValueError("Máximo 5 sets permitidos")
        # TODO: agregar {"juegos1": juegos1, "juegos2": juegos2} a _resultados
        pass

    def finalizar_partido(self) -> None:
        """
        TODO — implementar en este orden:
          1. Validar que haya al menos 1 set registrado → ValueError("Debe registrar al menos un set")
          2. Contar sets ganados por cada jugador
             (gana el set quien tiene más juegos en ese set)
          3. El jugador con más sets ganados es el ganador
          4. Llamar a registrar_victoria / registrar_derrota en cada jugador
          5. Llamar a registrar_estadistica_por_superficie en cada jugador
             usando self._superficie.tipo
        """
        pass

    def get_resumen(self) -> str:
        # TODO: retornar string legible del partido
        # Ejemplo: "Nadal vs Djokovic | Arcilla | 6-4, 7-5"
        pass
