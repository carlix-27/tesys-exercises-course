from modelos.personas.jugador import Jugador
from modelos.equipamiento.raqueta import Raqueta
from modelos.equipamiento.pelota import Pelota


class JugadorAmateur(Jugador):
    """
    Hereda de Jugador.
    No tiene ranking ni ingresos. Solo participa en torneos amateurs.

    Restricciones:
      - edad mínima: 10 años
    """

    EDAD_MINIMA = 10

    def __init__(
        self,
        nombre: str,
        edad: int,
        pais: str,
        superficie_favorita: str,
        raqueta: Raqueta,
        pelota: Pelota,
    ):
        super().__init__(nombre, edad, pais, superficie_favorita, raqueta, pelota)
        # TODO: validar que edad >= EDAD_MINIMA → ValueError("La edad mínima para un amateur es 10 años")

    def get_ranking(self) -> None:
        """Un amateur no tiene ranking oficial."""
        return None

    def get_descripcion(self) -> str:
        return f"{self._nombre} (Amateur)"

    def get_estadisticas(self) -> str:
        # TODO: retornar string con nombre, victorias, derrotas y win rate (sin puntos ni ingresos)
        pass
