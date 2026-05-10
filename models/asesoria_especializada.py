from models.servicio_base import Servicio
from excepciones import ValorInvalidoError

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_entidad, nombre, costo_base, duracion, especialidad, consultor):
        super().__init__(id_entidad, nombre, costo_base, duracion)
        self._especialidad = especialidad
        self._consultor = consultor

    def calcular_costo(self, parametros: dict) -> float:
        horas = parametros.get("horas", 1)
        if horas <= 0:
            raise ValorInvalidoError("Las horas de asesoría deben ser mayores a 0")
            
        nivel = parametros.get("nivel", "normal")

        if nivel == "alta":
            return self._costo_base * horas * 1.5
        return self._costo_base * horas

    def describir_servicio(self) -> str:
        return f"Asesoría en {self._especialidad} con {self._consultor}"
