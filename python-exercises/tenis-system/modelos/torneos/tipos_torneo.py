from modelos.torneos.torneo import Torneo
from modelos.personas.jugador import Jugador
from modelos.personas.jugador_profesional import JugadorProfesional
from modelos.personas.jugador_amateur import JugadorAmateur


class GrandSlam(Torneo):
    """
    Los 4 torneos más importantes del año.
    Máximo prestigio: 2000 puntos, hasta 128 jugadores profesionales.
    """

    def get_tipo(self) -> str:
        return "Grand Slam"

    def get_puntos_para_ganador(self) -> int:
        return 2000

    def get_puntos_para_finalista(self) -> int:
        return 1200

    def get_max_participantes(self) -> int:
        return 128

    def validar_jugador(self, jugador: Jugador) -> None:
        # TODO: verificar que jugador sea instancia de JugadorProfesional
        #       si no lo es → ValueError("Los jugadores amateur no pueden participar en un Grand Slam")
        pass


class MastersSeries(Torneo):
    """
    Torneos de alto nivel profesional.
    1000 puntos, hasta 64 jugadores.
    """

    def get_tipo(self) -> str:
        return "Masters Series"

    def get_puntos_para_ganador(self) -> int:
        return 1000

    def get_puntos_para_finalista(self) -> int:
        return 600

    def get_max_participantes(self) -> int:
        return 64

    def validar_jugador(self, jugador: Jugador) -> None:
        # TODO: solo JugadorProfesional
        pass


class TorneoChallengerATP(Torneo):
    """
    Para jugadores profesionales en ascenso.
    80 puntos, hasta 32 jugadores.
    """

    def get_tipo(self) -> str:
        return "Challenger ATP"

    def get_puntos_para_ganador(self) -> int:
        return 80

    def get_puntos_para_finalista(self) -> int:
        return 45

    def get_max_participantes(self) -> int:
        return 32

    def validar_jugador(self, jugador: Jugador) -> None:
        # TODO: solo JugadorProfesional
        pass


class TorneoAmateur(Torneo):
    """
    Torneo local sin puntos ATP.
    Solo participan jugadores amateurs, hasta 32.
    """

    def get_tipo(self) -> str:
        return "Torneo Amateur"

    def get_puntos_para_ganador(self) -> int:
        return 0  # No otorga puntos ATP

    def get_puntos_para_finalista(self) -> int:
        return 0

    def get_max_participantes(self) -> int:
        return 32

    def validar_jugador(self, jugador: Jugador) -> None:
        # TODO: solo JugadorAmateur
        #       si no lo es → ValueError("Los jugadores profesionales no pueden participar en torneos amateurs")
        pass
