from models import (
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva
)
from utils.logger import log_error

class SimulacionOperaciones:
    def __init__(self):
        self.__lista_operaciones = []

    def ejecutar_10_operaciones(self):
        try:
            c1 = Cliente("Juan Perez", "123")

            s1 = ReservaSala("S1", "Sala Norte", 50, 2, 10, "Piso 2")
            r1 = Reserva("R1", c1, s1, 2)
            r1.procesar_reserva()

            s2 = AlquilerEquipo("S2", "Laptop", 30, 1, "Portátil", "Disponible")
            r2 = Reserva("R2", c1, s2, 3)
            r2.procesar_reserva()

            s3 = AsesoriaEspecializada("S3", "Consultoría", 100, 1, "IA", "Carlos")
            r3 = Reserva("R3", c1, s3, 2)
            r3.procesar_reserva()

            # Casos con error
            r4 = Reserva("R4", None, s1, 2)
            r4.procesar_reserva()

            c2 = Cliente("A", "999")  # error

        except Exception as e:
            log_error(e)


if __name__ == "__main__":
    sim = SimulacionOperaciones()
    sim.ejecutar_10_operaciones()