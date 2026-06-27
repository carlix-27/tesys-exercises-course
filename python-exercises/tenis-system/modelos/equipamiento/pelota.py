from modelos.equipamiento.equipamiento import Equipamiento


class Pelota(Equipamiento):
    """
    Componente de Jugador (composición).
    Tiene tipo, presión y durabilidad. Se desgasta con el uso.

    Tipos válidos:  ATP | WTA | Recreativa
    Presión válida: 45–65 psi
    """

    TIPOS_VALIDOS = {"ATP", "WTA", "Recreativa"}
    PRESION_MIN = 45
    PRESION_MAX = 65

    def __init__(self, tipo: str, presion: int, durabilidad: int):
        super().__init__("Pelota")
        # TODO: validar que tipo esté en TIPOS_VALIDOS
        # TODO: validar que presion esté entre PRESION_MIN y PRESION_MAX
        self._tipo_pelota = tipo
        self._presion = presion
        self._durabilidad = durabilidad
        self._usos_actuales = 0

    @property
    def tipo(self) -> str:
        return self._tipo_pelota

    @property
    def presion(self) -> int:
        return self._presion

    @property
    def durabilidad(self) -> int:
        return self._durabilidad

    def registrar_uso(self) -> None:
        # TODO: incrementar _usos_actuales en 1
        pass

    def esta_buena_condicion(self) -> bool:
        # TODO: retornar True si _usos_actuales < _durabilidad
        pass

    def get_descripcion(self) -> str:
        return f"Pelota {self._tipo_pelota} ({self._presion} psi)"
