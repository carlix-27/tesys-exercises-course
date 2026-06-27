"""
Tests de equipamiento: Raqueta, Pelota, Superficie.
Cubre: validaciones de construcción y comportamiento básico.
"""
import pytest
from modelos.equipamiento import Raqueta, Pelota, Superficie


# --- Fixtures ---

@pytest.fixture
def raqueta():
    return Raqueta("Wilson", "Blade", 340, 31.5, "Synthetic")

@pytest.fixture
def pelota():
    return Pelota("ATP", 60, 8)


# =============================================================================
# Raqueta
# =============================================================================

class TestRaqueta:

    def test_crear_raqueta_guarda_atributos(self, raqueta):
        assert raqueta.marca == "Wilson"
        assert raqueta.modelo == "Blade"
        assert raqueta.peso == 340
        assert raqueta.balance == 31.5

    def test_peso_fuera_de_rango_lanza_error(self):
        with pytest.raises(ValueError, match="peso"):
            Raqueta("Wilson", "Blade", 250, 31.5, "Synthetic")

    def test_balance_fuera_de_rango_lanza_error(self):
        with pytest.raises(ValueError, match="balance"):
            Raqueta("Wilson", "Blade", 300, 45.0, "Synthetic")

    def test_descripcion_incluye_marca_y_peso(self, raqueta):
        desc = raqueta.get_descripcion()
        assert "Wilson" in desc
        assert "340" in desc


# =============================================================================
# Pelota
# =============================================================================

class TestPelota:

    def test_crear_pelota_guarda_atributos(self, pelota):
        assert pelota.tipo == "ATP"
        assert pelota.presion == 60

    def test_tipo_invalido_lanza_error(self):
        with pytest.raises(ValueError, match="tipo"):
            Pelota("Falsa", 60, 8)

    def test_presion_fuera_de_rango_lanza_error(self):
        with pytest.raises(ValueError, match="presión"):
            Pelota("ATP", 30, 8)

    def test_pelota_nueva_esta_en_buen_estado(self, pelota):
        assert pelota.esta_buena_condicion() is True

    def test_pelota_se_desgasta_al_agotar_usos(self, pelota):
        for _ in range(pelota.durabilidad):
            pelota.registrar_uso()
        assert pelota.esta_buena_condicion() is False


# =============================================================================
# Superficie
# =============================================================================

class TestSuperficie:

    def test_tipo_invalido_lanza_error(self):
        with pytest.raises(ValueError, match="superficie"):
            Superficie("Arena", 1.0, 0.85)

    def test_pasto_es_rapido(self):
        pasto = Superficie("Pasto", 1.4, 0.9)
        assert "rápida" in pasto.get_caracteristicas().lower()

    def test_arcilla_es_lenta(self):
        arcilla = Superficie("Arcilla", 0.6, 0.75)
        assert "lenta" in arcilla.get_caracteristicas().lower()
