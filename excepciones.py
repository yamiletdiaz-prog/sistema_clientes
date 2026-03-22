# ==========================
# excepciones.py
# ==========================
class ClienteError(Exception): pass
class ValidacionError(ClienteError): pass
class ClienteNoEncontradoError(ClienteError): pass
class ClienteDuplicadoError(ClienteError): pass
class ArchivoError(ClienteError): pass
