from models.servicio_base import Servicio
from excepciones import ValorInvalidoError, OperacionNoPermitidaError

class AlquilerEquipo(Servicio):
    def __init__(self, id_entidad, nombre, costo_base, duracion, tipo, estado):
        super().__init__(id_entidad, nombre, costo_base, duracion)
        self._tipo_equipo = tipo
        self._estado = estado

    def calcular_costo(self, parametros: dict) -> float:
        if self._estado.lower() != "disponible":
            raise OperacionNoPermitidaError(f"El equipo {self._tipo_equipo} no está disponible")
            
        dias = parametros.get("dias", 1)
        if dias <= 0:
            raise ValorInvalidoError("Los días de alquiler deben ser mayores a 0")
        return self._costo_base * dias

    def describir_servicio(self) -> str:
        return f"Equipo {self._tipo_equipo} - Estado: {self._estado}"
