from fastapi import APIRouter
from app.padlock.schemas import RespuestaAccionDispositivo, SolicitudAccionProveedor
from app.padlock.services.nuovo_service import ejecutar_accion_nuovo

enrutador = APIRouter(prefix="/nuovo", tags=["nuovo"])


@enrutador.post("/lock", response_model=RespuestaAccionDispositivo)
async def bloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return ejecutar_accion_nuovo("lock", datos.imei, datos.payload)


@enrutador.post("/unlock", response_model=RespuestaAccionDispositivo)
async def desbloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return ejecutar_accion_nuovo("unlock", datos.imei, datos.payload)


@enrutador.post("/register", response_model=RespuestaAccionDispositivo)
async def registrar_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return ejecutar_accion_nuovo("register", datos.imei, datos.payload)
