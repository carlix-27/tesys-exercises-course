"""
Tests de torneos: GrandSlam, MastersSeries, TorneoChallengerATP, TorneoAmateur.
Cubre: herencia, polimorfismo en puntos y validaciones, restricciones por tipo de jugador.
"""
import pytest
from modelos.equipamiento import Raqueta, Pelota
from modelos.personas import JugadorProfesional, JugadorAmateur
from modelos.torneos import GrandSlam, MastersSeries, TorneoChallengerATP, TorneoAmateur


# --- Fixtures ---

@pytest.fixture
def raqueta():
    return Raqueta("Wilson", "Blade", 340, 31.5, "Synthetic")

@pytest.fixture
def pelota():
    return Pelota("ATP", 60, 8)

@pytest.fixture
def nadal(raqueta, pelota):
    return JugadorProfesional("Rafael Nadal", 36, "España", 10, "Arcilla", raqueta, pelota)

@pytest.fixture
def juan(raqueta):
    return JugadorAmateur("Juan Pérez", 22, "Argentina", "Cemento Duro", raqueta, Pelota("Recreativa", 55, 5))

@pytest.fixture
def roland_garros():
    return GrandSlam("Roland Garros", "Francia", "Arcilla", "2024-05-26")

@pytest.fixture
def torneo_amateur():
    return TorneoAmateur("Open Local", "Argentina", "Cemento Duro", "2024-07-01")


# =============================================================================
# Polimorfismo: cada tipo tiene sus propios puntos y límites
# =============================================================================

class TestPolimorfismoTorneos:

    def test_grand_slam_retorna_2000_puntos(self, roland_garros):
        assert roland_garros.get_puntos_para_ganador() == 2000

    def test_masters_retorna_1000_puntos(self):
        masters = MastersSeries("Masters Madrid", "España", "Arcilla", "2024-04-28")
        assert masters.get_puntos_para_ganador() == 1000

    def test_challenger_retorna_80_puntos(self):
        challenger = TorneoChallengerATP("Challenger BA", "Argentina", "Cemento Duro", "2024-07-01")
        assert challenger.get_puntos_para_ganador() == 80

    def test_torneo_amateur_retorna_0_puntos(self, torneo_amateur):
        assert torneo_amateur.get_puntos_para_ganador() == 0

    def test_tipo_grand_slam(self, roland_garros):
        assert roland_garros.get_tipo() == "Grand Slam"

    def test_tipo_torneo_amateur(self, torneo_amateur):
        assert torneo_amateur.get_tipo() == "Torneo Amateur"


# =============================================================================
# Validaciones de construcción
# =============================================================================

class TestValidacionesTorneo:

    def test_superficie_invalida_lanza_error(self):
        with pytest.raises(ValueError, match="superficie"):
            GrandSlam("Test", "Test", "Arena", "2024-01-01")

    def test_fecha_invalida_lanza_error(self):
        with pytest.raises(ValueError, match="fecha"):
            GrandSlam("Test", "Test", "Arcilla", "01-01-2024")


# =============================================================================
# Restricciones por tipo de jugador (polimorfismo en validar_jugador)
# =============================================================================

class TestRestriccionesDeParticipacion:

    def test_profesional_puede_entrar_al_grand_slam(self, roland_garros, nadal):
        roland_garros.agregar_jugador(nadal)
        assert len(roland_garros.get_participantes()) == 1

    def test_amateur_no_puede_entrar_al_grand_slam(self, roland_garros, juan):
        with pytest.raises(ValueError):
            roland_garros.agregar_jugador(juan)

    def test_amateur_puede_entrar_al_torneo_amateur(self, torneo_amateur, juan):
        torneo_amateur.agregar_jugador(juan)
        assert len(torneo_amateur.get_participantes()) == 1

    def test_profesional_no_puede_entrar_al_torneo_amateur(self, torneo_amateur, nadal):
        with pytest.raises(ValueError):
            torneo_amateur.agregar_jugador(nadal)

    def test_jugador_duplicado_lanza_error(self, roland_garros, nadal):
        roland_garros.agregar_jugador(nadal)
        with pytest.raises(ValueError, match="registrado"):
            roland_garros.agregar_jugador(nadal)

    def test_reporte_incluye_nombre_y_participantes(self, roland_garros, nadal):
        roland_garros.agregar_jugador(nadal)
        reporte = roland_garros.generar_reporte()
        assert "Roland Garros" in reporte
        assert "Participantes: 1" in reporte
