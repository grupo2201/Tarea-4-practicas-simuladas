class ReservaError(Exception):
    pass

class ClienteInvalidoError(ReservaError):
    pass

class ServicioNoDisponibleError(ReservaError):
    pass

class OperacionNoPermitidaError(ReservaError):
    pass

class ParametrosFaltantesError(ReservaError):
    pass