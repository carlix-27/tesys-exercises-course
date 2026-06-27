"""
Tests de jugadores: JugadorProfesional y JugadorAmateur.
Cubre: composición con equipamiento, herencia, estadísticas, validaciones.
"""
import pytest
from modelos.equipamiento import Raqueta, Pelota
from modelos.personas import JugadorProfesional, JugadorAmateur


# --- Fixtures ---

@pytest.fixture
def raqueta():
    return Raqueta("Wilson", "Blade", 340, 31.5, "Synthetic")

@pytest.fixture
def pelota():
    return Pelota("ATP", 60, 8)

@pytest.fixture
def raqueta_yonex():
    return Raqueta("Yonex", "Vcore", 320, 32.0, "Synthetic")

@pytest.fixture
def nadal(raqueta, pelota):
    return JugadorProfesional("Rafael Nadal", 36, "España", 10, "Arcilla", raqueta, pelota)

@pytest.fixture
def djokovic(raqueta, pelota):
    return JugadorProfesional("Novak Djokovic", 35, "Serbia", 1, "Cemento Duro", raqueta, pelota)

@pytest.fixture
def juan(raqueta):
    return JugadorAmateur("Juan Pérez", 22, "Argentina", "Cemento Duro", raqueta, Pelota("Recreativa", 55, 5))


# =============================================================================
# JugadorProfesional
# =============================================================================

class TestJugadorProfesional:

    # Composición: el jugador TIENE una raqueta y una pelota
    def test_composicion_raqueta_y_pelota(self, nadal, raqueta, pelota):
        assert nadal.get_raqueta() is raqueta
        assert nadal.get_pelota() is pelota

    def test_cambiar_raqueta(self, nadal, raqueta_yonex):
        nadal.set_raqueta(raqueta_yonex)
        assert nadal.get_raqueta().marca == "Yonex"

    def test_set_raqueta_none_lanza_error(self, nadal):
        with pytest.raises(ValueError, match="raqueta"):
            nadal.set_raqueta(None)

    # Validaciones de construcción
    def test_edad_minima_15_anos(self, raqueta, pelota):
        with pytest.raises(ValueError, match="edad"):
            JugadorProfesional("Junior", 12, "España", 500, "Arcilla", raqueta, pelota)

    def test_ranking_negativo_lanza_error(self, raqueta, pelota):
        with pytest.raises(ValueError, match="ranking"):
            JugadorProfesional("Test", 20, "España", -1, "Arcilla", raqueta, pelota)

    def test_nombre_vacio_lanza_error(self, raqueta, pelota):
        with pytest.raises(ValueError, match="nombre"):
            JugadorProfesional("", 25, "España", 100, "Arcilla", raqueta, pelota)

    # Estadísticas
    def test_registrar_victoria_y_derrota(self, nadal, djokovic):
        nadal.registrar_victoria(djokovic)
        nadal.registrar_derrota(djokovic)
        assert nadal.get_victorias() == 1
        assert nadal.get_derrotas() == 1

    def test_win_rate_calculado_correctamente(self, nadal, djokovic):
        nadal.registrar_victoria(djokovic)
        nadal.registrar_victoria(djokovic)
        nadal.registrar_derrota(djokovic)
        assert nadal.get_win_rate() == pytest.approx(66.67, rel=1e-2)

    def test_win_rate_sin_partidos_es_cero(self, nadal):
        assert nadal.get_win_rate() == 0.0

    # Puntos y ranking
    def test_acumular_puntos(self, nadal):
        nadal.agregar_puntos(2000)
        nadal.agregar_puntos(1000)
        assert nadal.get_puntos_acumulados() == 3000

    def test_compara_ranking_mas_puntos_gana(self, nadal, djokovic):
        nadal.agregar_puntos(5000)
        djokovic.agregar_puntos(2000)
        assert nadal.compara_ranking(djokovic) == 1

    def test_estadisticas_por_superficie(self, nadal):
        nadal.registrar_estadistica_por_superficie("Arcilla", True)
        nadal.registrar_estadistica_por_superficie("Arcilla", False)
        stats = nadal.get_estadisticas_por_superficie("Arcilla")
        assert stats["victorias"] == 1
        assert stats["derrotas"] == 1


# =============================================================================
# JugadorAmateur
# =============================================================================

class TestJugadorAmateur:

    def test_amateur_no_tiene_ranking(self, juan):
        assert juan.get_ranking() is None

    def test_edad_minima_10_anos(self, raqueta):
        with pytest.raises(ValueError, match="edad"):
            JugadorAmateur("Niño", 7, "Argentina", "Arcilla", raqueta, Pelota("Recreativa", 55, 5))

    def test_estadisticas_superficie_sin_datos_retorna_ceros(self, juan):
        stats = juan.get_estadisticas_por_superficie("Pasto")
        assert stats["victorias"] == 0
        assert stats["win_rate"] == 0.0
