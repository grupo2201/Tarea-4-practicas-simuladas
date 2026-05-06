from abc import ABC, abstractmethod
from utils.logger import log_info

class EntidadBase(ABC):
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass

    def registrar_evento(self, evento: str):
        log_info(f"{self._id_entidad} - {evento}")