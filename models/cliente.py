from models.base import EntidadBase
from excepciones import ClienteInvalidoError

class Cliente(EntidadBase):
    def __init__(self, nombre: str, identificacion: str):
        super().__init__(identificacion)

        self.__nombre = None
        self.__identificacion = None
        self.__datos_personales = {}

        self.nombre = nombre
        self.identificacion = identificacion

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        if not value or len(value.strip()) < 3:
            raise ClienteInvalidoError("Nombre inválido")
        self.__nombre = value.strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, value):
        if not value:
            raise ClienteInvalidoError("Identificación inválida")
        self.__identificacion = value

    def validar_datos(self):
        if not self.__nombre or not self.__identificacion:
            raise ClienteInvalidoError("Datos incompletos del cliente")

    def obtener_detalles(self) -> str:
        detalles = f"Cliente: {self.__nombre} ({self.__identificacion})"
        if self._datos_personales:
            detalles +=f"\ndatos personales:\n"
            for clave, valor in self._datos_personales.items():
                detalles +=f"-{clave}: {valor}\n"
        return detalles
    def __str__(self):
        return self.obtener_detalles()
    