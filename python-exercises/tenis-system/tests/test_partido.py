"""
Tests de Partido.
Cubre: validaciones de construcción, registro de sets y finalización del partido.
Este es el punto donde todo el sistema se conecta.
"""
import pytest
from modelos.equipamiento import Raqueta, Pelota, Superficie
from modelos.personas import JugadorProfesional
from modelos.torneos import GrandSlam
from modelos.partido import Partido


# --- Fixtures ---

@pytest.fixture
def raqueta():
    return Raqueta("Wilson", "Blade", 340, 31.5, "Synthetic")

@pytest.fixture
def pelota():
    return Pelota("ATP", 60, 8)

@pytest.fixture
def arcilla():
    return Superficie("Arcilla", 0.6, 0.75)

@pytest.fixture
def nadal(raqueta, pelota):
    return JugadorProfesional("Rafael Nadal", 36, "España", 10, "Arcilla", raqueta, pelota)

@pytest.fixture
def djokovic(raqueta, pelota):
    return JugadorProfesional("Novak Djokovic", 35, "Serbia", 1, "Cemento Duro", raqueta, pelota)

@pytest.fixture
def roland_garros():
    return GrandSlam("Roland Garros", "Francia", "Arcilla", "2024-05-26")

@pytest.fixture
def partido(nadal, djokovic, arcilla, roland_garros):
    return Partido(nadal, djokovic, arcilla, roland_garros, "2024-05-30")


# =============================================================================
# Tests de Partido
# =============================================================================

class TestPartido:

    def test_mismo_jugador_en_ambos_lados_lanza_error(self, nadal, arcilla, roland_garros):
        with pytest.raises(ValueError, match="diferentes"):
            Partido(nadal, nadal, arcilla, roland_garros, "2024-05-30")

    def test_fecha_invalida_lanza_error(self, nadal, djokovic, arcilla, roland_garros):
        with pytest.raises(ValueError, match="fecha"):
            Partido(nadal, djokovic, arcilla, roland_garros, "30/05/2024")

    def test_registrar_set_guarda_resultado(self, partido):
        partido.registrar_set(6, 4)
        assert partido.get_resultados() == [{"juegos1": 6, "juegos2": 4}]

    def test_no_se_pueden_registrar_mas_de_5_sets(self, partido):
        for _ in range(5):
            partido.registrar_set(6, 4)
        with pytest.raises(ValueError, match="sets"):
            partido.registrar_set(6, 4)

    def test_finalizar_sin_sets_lanza_error(self, partido):
        with pytest.raises(ValueError, match="set"):
            partido.finalizar_partido()

    def test_finalizar_registra_victoria_y_derrota(self, partido, nadal, djokovic):
        partido.registrar_set(6, 4)  # gana nadal
        partido.registrar_set(7, 5)  # gana nadal
        partido.finalizar_partido()
        assert nadal.get_victorias() == 1
        assert djokovic.get_derrotas() == 1

    def test_finalizar_actualiza_stats_por_superficie(self, partido, nadal):
        partido.registrar_set(6, 4)
        partido.registrar_set(7, 5)
        partido.finalizar_partido()
        stats = nadal.get_estadisticas_por_superficie("Arcilla")
        assert stats["victorias"] == 1
