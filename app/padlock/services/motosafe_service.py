from typing import Dict, Optional
from fastapi import HTTPException, status
from app.padlock.config import MOTOSAFE_API_CLAVE, MOTOSAFE_URL_BASE


def ejecutar_accion_motosafe(accion: str, imei: str, datos: Optional[Dict]) -> Dict:
    if not MOTOSAFE_URL_BASE or not MOTOSAFE_API_CLAVE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Credenciales de MotoSafe no configuradas.",
        )

    # TODO: Integrate MotoSafe API client here.
    return {
        "provider": "motosafe",
        "action": accion,
        "imei": imei,
        "status": "accepted",
        "message": "Accion MotoSafe recibida (stub).",
        "data": datos or {},
    }
