from modelos.equipamiento.equipamiento import Equipamiento


class Raqueta(Equipamiento):
    """
    Componente de Jugador (composición).
    Una raqueta tiene marca, modelo, peso y balance.

    Rangos válidos:
      - peso:    280–340 gramos
      - balance: 30.0–38.0 cm desde el mango
    """

    PESO_MIN = 280
    PESO_MAX = 340
    BALANCE_MIN = 30.0
    BALANCE_MAX = 38.0

    def __init__(self, marca: str, modelo: str, peso: int, balance: float, material_cuerda: str):
        super().__init__("Raqueta")
        # TODO: validar que peso esté entre PESO_MIN y PESO_MAX
        #       lanzar ValueError con mensaje claro si no cumple
        # TODO: validar que balance esté entre BALANCE_MIN y BALANCE_MAX
        self._marca = marca
        self._modelo = modelo
        self._peso = peso
        self._balance = balance
        self._material_cuerda = material_cuerda

    @property
    def marca(self) -> str:
        return self._marca

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def peso(self) -> int:
        return self._peso

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def material_cuerda(self) -> str:
        return self._material_cuerda

    def get_descripcion(self) -> str:
        # TODO: retornar string descriptivo
        # Ejemplo: "Wilson Blade | 340g | balance: 31.5cm | cuerda: Synthetic"
        pass
