from fastapi import APIRouter
from app.padlock.schemas import RespuestaAccionDispositivo, SolicitudAccionProveedor
from app.padlock.services.motosafe_service import ejecutar_accion_motosafe

enrutador = APIRouter(prefix="/motosafe", tags=["motosafe"])


@enrutador.post("/lock", response_model=RespuestaAccionDispositivo)
async def bloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return ejecutar_accion_motosafe("lock", datos.imei, datos.payload)


@enrutador.post("/unlock", response_model=RespuestaAccionDispositivo)
async def desbloquear_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return ejecutar_accion_motosafe("unlock", datos.imei, datos.payload)


@enrutador.post("/register", response_model=RespuestaAccionDispositivo)
async def registrar_dispositivo(datos: SolicitudAccionProveedor) -> RespuestaAccionDispositivo:
    return ejecutar_accion_motosafe("register", datos.imei, datos.payload)
