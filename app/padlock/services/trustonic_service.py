from datetime import datetime, timedelta
from typing import Dict, Optional

import httpx
from fastapi import HTTPException, status
from app.padlock.config import (
    TRUSTONIC_API_CLAVE,
    TRUSTONIC_ENCABEZADO_AUTORIZACION,
    TRUSTONIC_PREFIJO_AUTORIZACION,
    TRUSTONIC_TIEMPO_ESPERA_SEGUNDOS,
    TRUSTONIC_URL_BASE,
)


def registrar_trustonic(accion: str, imei: str, datos: Optional[Dict]) -> Dict:
    if not TRUSTONIC_URL_BASE or not TRUSTONIC_API_CLAVE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Credenciales de Trustonic no configuradas.",
        )

    if accion != "register":
        return {
            "provider": "trustonic",
            "action": accion,
            "imei": imei,
            "status": "accepted",
            "message": "Accion Trustonic recibida (stub).",
            "data": datos or {},
        }

    politica_asignada = (datos or {}).get("assignedPolicy", "A11Financed")
    nombre = (datos or {}).get("name", "UNKNOWN")
    fecha_vencimiento = datetime.now() + timedelta(days=14)
    fecha_vencimiento_str = fecha_vencimiento.strftime("%d-%m-%Y %H:%M:%S")

    cuerpo_peticion = {
        "devices": [
            {
                "imei": imei,
                "assignedPolicy": politica_asignada,
                "customProperties": {
                    "name": nombre,
                    "dueDate": fecha_vencimiento_str,
                },
            }
        ]
    }

    encabezados = {
        TRUSTONIC_ENCABEZADO_AUTORIZACION: f"{TRUSTONIC_PREFIJO_AUTORIZACION} {TRUSTONIC_API_CLAVE}".strip(),
        "Content-Type": "application/json",
    }

    url_base = TRUSTONIC_URL_BASE.rstrip("/")
    url_registro = f"{url_base}/register"

    try:
        with httpx.Client(timeout=TRUSTONIC_TIEMPO_ESPERA_SEGUNDOS) as cliente:
            respuesta = cliente.post(url_registro, json=cuerpo_peticion, headers=encabezados)
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Fallo la solicitud a Trustonic: {error}",
        ) from error

    if respuesta.status_code >= 400:
        raise HTTPException(
            status_code=respuesta.status_code,
            detail=respuesta.text,
        )

    return {
        "provider": "trustonic",
        "action": accion,
        "imei": imei,
        "status": "success",
        "message": "Registro Trustonic completado.",
        "data": respuesta.json() if respuesta.content else {},
    }
