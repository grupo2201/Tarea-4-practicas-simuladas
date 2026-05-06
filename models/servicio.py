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
class ReservaSala(Servicio):
     def __init__(self, id_entidad, nombre, costo_base, duracion, capacidad, ubicacion):
        super().__init__(id_entidad, nombre, costo_base, duracion)
        self._capacidad = capacidad
        self._ubicacion = ubicacion

     def calcular_costo(self, parametros: dict) -> float:
        horas = parametros.get("horas")
        if not horas:
            raise ValueError("Faltan horas")
        return self._costo_base * horas

     def describir_servicio(self) -> str:
        return f"Sala en {self._ubicacion} para {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    def __init__(self, id_entidad, nombre, costo_base, duracion, tipo, estado):
        super().__init__(id_entidad, nombre, costo_base, duracion)
        self._tipo_equipo = tipo
        self._estado = estado

    def calcular_costo(self, parametros: dict) -> float:
        dias = parametros.get("dias", 1)
        return self._costo_base * dias

    def describir_servicio(self) -> str:
        return f"Equipo {self._tipo_equipo} - Estado: {self._estado}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_entidad, nombre, costo_base, duracion, especialidad, consultor):
        super().__init__(id_entidad, nombre, costo_base, duracion)
        self._especialidad = especialidad
        self._consultor = consultor

    def calcular_costo(self, parametros: dict) -> float:
        horas = parametros.get("horas", 1)
        nivel = parametros.get("nivel", "normal")

        if nivel == "alta":
            return self._costo_base * horas * 1.5
        return self._costo_base * horas

    def describir_servicio(self) -> str:
        return f"Asesoría en {self._especialidad} con {self._consultor}"