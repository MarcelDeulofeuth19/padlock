from typing import Dict, Optional
from fastapi import HTTPException, status
from app.padlock.config import NUOVO_API_CLAVE, NUOVO_URL_BASE


def ejecutar_accion_nuovo(accion: str, imei: str, datos: Optional[Dict]) -> Dict:
    if not NUOVO_URL_BASE or not NUOVO_API_CLAVE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Credenciales de Nuovo no configuradas.",
        )

    # TODO: Integrate Nuovo API client here.
    return {
        "provider": "nuovo",
        "action": accion,
        "imei": imei,
        "status": "accepted",
        "message": "Accion Nuovo recibida (stub).",
        "data": datos or {},
    }
