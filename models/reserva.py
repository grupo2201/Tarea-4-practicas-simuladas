from datetime import date
from models.base import EntidadBase
from excepciones import *
from utils.logger import log_error, log_info

class Reserva(EntidadBase):
    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)

        self._cliente = cliente
        self._servicio = servicio
        self._fecha_reserva = date.today()
        self._duracion = duracion
        self._estado = "pendiente"

    def confirmar_reserva(self):
        if self._estado != "pendiente":
            raise OperacionNoPermitidaError("No se puede confirmar")
        self._estado = "confirmada"

    def cancelar_reserva(self):
        if self._estado == "cancelada":
            raise OperacionNoPermitidaError("Ya cancelada")
        self._estado = "cancelada"

    def procesar_reserva(self):
        try:
            if not self._cliente:
                raise ClienteInvalidoError("Cliente inválido")

            if not self._servicio:
                raise ServicioNoDisponibleError("Servicio no disponible")

            costo = self._servicio.calcular_costo({"horas": self._duracion})
            self.confirmar_reserva()

        except ReservaError as e:
            log_error(e)
            raise
        except Exception as e:
            log_error(e)
            raise ReservaError("Error procesando reserva") from e
        else:
            log_info(f"Reserva exitosa. Total: {costo}")
        finally:
            log_info("Proceso finalizado")
            log_info("Proceso finalizado")

    def obtener_detalles(self):
        return f"Reserva {self._id_entidad} - Estado: {self._estado}"