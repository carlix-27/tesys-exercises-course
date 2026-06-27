"""
main.py — Ejemplo de uso del sistema de gestión de torneos de tenis.
Sirve para entender cómo las clases interactúan entre sí una vez implementadas.
"""

from modelos import (
    Raqueta, Pelota, Superficie,
    JugadorProfesional, JugadorAmateur,
    GrandSlam, TorneoAmateur,
    Partido,
)


def main():
    # -------------------------------------------------------------------------
    # 1. Crear equipamiento (objetos simples, sin dependencias)
    # -------------------------------------------------------------------------
    raqueta_nadal = Raqueta("Babolat", "Pure Aero", 300, 32.0, "Synthetic")
    pelota_atp    = Pelota("ATP", 60, 8)
    arcilla       = Superficie("Arcilla", 0.6, 0.75)

    raqueta_djoko = Raqueta("Head", "Speed Pro", 310, 31.0, "Polyester")
    pelota_djoko  = Pelota("ATP", 58, 8)

    # -------------------------------------------------------------------------
    # 2. Crear jugadores (composición: cada jugador TIENE su equipamiento)
    # -------------------------------------------------------------------------
    nadal    = JugadorProfesional("Rafael Nadal",    36, "España", 10, "Arcilla",       raqueta_nadal, pelota_atp)
    djokovic = JugadorProfesional("Novak Djokovic",  35, "Serbia",  1, "Cemento Duro",  raqueta_djoko, pelota_djoko)

    print(nadal.get_descripcion())
    print(djokovic.get_descripcion())

    # -------------------------------------------------------------------------
    # 3. Crear torneo (herencia: GrandSlam es un Torneo)
    # -------------------------------------------------------------------------
    roland_garros = GrandSlam("Roland Garros", "Francia", "Arcilla", "2024-05-26")
    roland_garros.agregar_jugador(nadal)
    roland_garros.agregar_jugador(djokovic)

    print(roland_garros.generar_reporte())

    # -------------------------------------------------------------------------
    # 4. Simular un partido (composición: Partido TIENE jugadores y superficie)
    # -------------------------------------------------------------------------
    partido = Partido(nadal, djokovic, arcilla, roland_garros, "2024-05-30")
    partido.registrar_set(6, 4)
    partido.registrar_set(7, 5)
    partido.set_aces(12)
    partido.set_errores_no_forzados(5)
    partido.finalizar_partido()

    roland_garros.registrar_partido(partido)

    # -------------------------------------------------------------------------
    # 5. Consultar estadísticas (polimorfismo: get_estadisticas varía por tipo)
    # -------------------------------------------------------------------------
    print(nadal.get_estadisticas())
    print(djokovic.get_estadisticas())
    print(nadal.get_estadisticas_por_superficie("Arcilla"))

    # -------------------------------------------------------------------------
    # 6. Torneo Amateur (solo acepta JugadorAmateur)
    # -------------------------------------------------------------------------
    raqueta_local = Raqueta("Head", "Radical", 310, 32.0, "Synthetic")
    pelota_local  = Pelota("Recreativa", 55, 5)
    juan = JugadorAmateur("Juan Pérez", 22, "Argentina", "Cemento Duro", raqueta_local, pelota_local)

    open_local = TorneoAmateur("Open Local", "Argentina", "Cemento Duro", "2024-07-01")
    open_local.agregar_jugador(juan)
    print(open_local.generar_reporte())


if __name__ == "__main__":
    main()
