from abc import ABC, abstractmethod
from models.base import EntidadBase

class Servicio(EntidadBase, ABC):
    def __init__(self, id_entidad, nombre, costo_base, duracion_estandar):
        super().__init__(id_entidad)
        self._nombre_servicio = nombre
        self._costo_base = costo_base
        self._duracion_estandar = duracion_estandar

    @abstractmethod
    def calcular_costo(self, parametros: dict) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    def obtener_detalles(self) -> str:
        return f"[{self._id_entidad}] {self.describir_servicio()} - Costo Base: ${self._costo_base}"
