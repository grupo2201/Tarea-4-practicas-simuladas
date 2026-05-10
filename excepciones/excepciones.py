class ReservaError(Exception):
    """Clase base para excepciones en el sistema de reservas."""
    pass

class ClienteInvalidoError(ReservaError):
    """Excepción lanzada cuando los datos del cliente son inválidos."""
    pass

class ServicioNoDisponibleError(ReservaError):
    """Excepción lanzada cuando un servicio no está disponible o no se encuentra."""
    pass

class OperacionNoPermitidaError(ReservaError):
    """Excepción lanzada al intentar una operación ilegal (ej. cancelar reserva ya cancelada)."""
    pass

class ParametrosFaltantesError(ReservaError):
    """Excepción lanzada cuando faltan parámetros para calcular un costo o crear un servicio."""
    pass

class ValorInvalidoError(ReservaError):
    """Excepción lanzada cuando un valor numérico provisto es inválido (ej. capacidad negativa)."""
    pass
