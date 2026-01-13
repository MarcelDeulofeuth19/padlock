from fastapi import APIRouter
from app.padlock.schemas import RespuestaAccionDispositivo, SolicitudAccionProveedor
from app.padlock.services.knox_service import registrar_knox

enrutador = APIRouter(prefix="/knox", tags=["knox"])


@enrutador.post("/lock", response_model=RespuestaAccionDispositivo)
async def bloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return registrar_knox("lock", datos.imei, datos.payload)


@enrutador.post("/unlock", response_model=RespuestaAccionDispositivo)
async def desbloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return registrar_knox("unlock", datos.imei, datos.payload)


@enrutador.post("/register", response_model=RespuestaAccionDispositivo)
async def registrar_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return registrar_knox("register", datos.imei, datos.payload)
