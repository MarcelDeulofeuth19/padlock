from fastapi import APIRouter, HTTPException, status
from app.padlock.schemas import RespuestaAccionDispositivo, SolicitudAccionUnificada
from app.padlock.services.knox_service import registrar_knox
from app.padlock.services.motosafe_service import ejecutar_accion_motosafe
from app.padlock.services.nuovo_service import ejecutar_accion_nuovo
from app.padlock.services.trustonic_service import registrar_trustonic

enrutador = APIRouter(prefix="/proveedor", tags=["proveedor"])

_PROVEEDORES = {
    "knox": registrar_knox,
    "trustonic": registrar_trustonic,
    "nuovo": ejecutar_accion_nuovo,
    "motosafe": ejecutar_accion_motosafe,
}


@enrutador.post("/accion", response_model=RespuestaAccionDispositivo)
async def ejecutar_accion(datos: SolicitudAccionUnificada) -> RespuestaAccionDispositivo:
    proveedor = datos.provider.strip().lower()
    if proveedor not in _PROVEEDORES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Proveedor no soportado.",
        )
    return _PROVEEDORES[proveedor](datos.action, datos.imei, datos.payload)
