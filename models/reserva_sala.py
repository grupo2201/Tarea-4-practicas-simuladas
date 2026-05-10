from models.servicio_base import Servicio
from excepciones import ParametrosFaltantesError, ValorInvalidoError

class ReservaSala(Servicio):
     def __init__(self, id_entidad, nombre, costo_base, duracion, capacidad, ubicacion):
        super().__init__(id_entidad, nombre, costo_base, duracion)
        if capacidad <= 0:
            raise ValorInvalidoError("La capacidad debe ser mayor a 0")
        self._capacidad = capacidad
        self._ubicacion = ubicacion

     def calcular_costo(self, parametros: dict) -> float:
        horas = parametros.get("horas")
        if not horas:
            raise ParametrosFaltantesError("Faltan horas para la reserva de sala")
        if horas <= 0:
            raise ValorInvalidoError("Las horas deben ser mayores a 0")
        return self._costo_base * horas

     def describir_servicio(self) -> str:
        return f"Sala en {self._ubicacion} para {self._capacidad} personas"
