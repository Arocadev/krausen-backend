from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger("krausen")


def error_response(status_code: int, mensaje: str, detalle=None) -> JSONResponse:
    body = {"status": status_code, "error": mensaje}
    if detalle:
        body["detalle"] = detalle
    return JSONResponse(status_code=status_code, content=body)


async def http_exception_handler(request: Request, exc: HTTPException):
    mensajes = {
        400: "Solicitud incorrecta",
        401: "No autenticado",
        403: "Acceso denegado",
        404: "Recurso no encontrado",
        409: "Conflicto con datos existentes",
        422: "Datos inválidos",
        429: "Demasiadas peticiones",
    }
    mensaje = mensajes.get(exc.status_code, "Error en la petición")
    return error_response(exc.status_code, mensaje, exc.detail)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []
    for error in exc.errors():
        campo = " → ".join(str(loc) for loc in error["loc"] if loc != "body")
        errores.append({"campo": campo, "mensaje": error["msg"]})
    return error_response(422, "Los datos enviados no son válidos", errores)


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no controlado en {request.url}: {exc}", exc_info=True)
    return error_response(500, "Error interno del servidor")