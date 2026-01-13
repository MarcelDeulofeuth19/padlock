from fastapi import APIRouter
from app.padlock.schemas import RespuestaAccionDispositivo, SolicitudAccionProveedor
from app.padlock.services.trustonic_service import registrar_trustonic

enrutador = APIRouter(prefix="/trustonic", tags=["trustonic"])

@enrutador.post("/register", response_model=RespuestaAccionDispositivo)
async def registrar_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return registrar_trustonic("register", datos.imei, datos.payload)

@enrutador.post("/lock", response_model=RespuestaAccionDispositivo)
async def bloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return registrar_trustonic("lock", datos.imei, datos.payload)


@enrutador.post("/unlock", response_model=RespuestaAccionDispositivo)
async def desbloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return registrar_trustonic("unlock", datos.imei, datos.payload)
