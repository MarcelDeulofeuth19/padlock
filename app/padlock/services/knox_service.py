from typing import Dict, Optional
import httpx
from fastapi import HTTPException, status
from app.padlock.config import KNOX_TIEMPO_ESPERA_SEGUNDOS, KNOX_URL_BASE
from app.padlock.utils.generador_tokens_knox import obtener_token_knox_co


def registrar_knox(accion: str, imei: str, datos: Optional[Dict]) -> Dict:
    if not KNOX_URL_BASE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="KNOX_URL_BASE no configurado.",
        )

    if accion != "register":
        return {
            "provider": "knox",
            "action": accion,
            "imei": imei,
            "status": "accepted",
            "message": "Accion Knox recibida (stub).",
            "data": datos or {},
        }

    try:
        token_api = obtener_token_knox_co()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo generando token Knox: {error}",
        ) from error

    cuerpo = {
        "deviceList": [{"deviceUid": imei}],
        "autoAccept": True,
        "autoLock": True,
        "applySimControl": True,
        "enableBlockFactoryReset": True,
        "blockDOProvision": True,
        "blockADBCommand": True,
    }
    if datos:
        for clave in (
            "autoAccept",
            "autoLock",
            "applySimControl",
            "enableBlockFactoryReset",
            "blockDOProvision",
            "blockADBCommand",
        ):
            if clave in datos:
                cuerpo[clave] = datos[clave]

    encabezados = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-knox-apitoken": token_api,
    }
    id_transaccion = (datos or {}).get("transactionId") or (datos or {}).get("transaction_id")
    if id_transaccion:
        encabezados["x-knox-transactionId"] = str(id_transaccion)

    url_registro = f"{KNOX_URL_BASE.rstrip('/')}/kcs/v1.1/kg/devices/uploads"
    try:
        with httpx.Client(timeout=KNOX_TIEMPO_ESPERA_SEGUNDOS) as cliente:
            respuesta = cliente.post(url_registro, json=cuerpo, headers=encabezados)
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Fallo la solicitud a Knox: {error}",
        ) from error

    if respuesta.status_code >= 400:
        raise HTTPException(
            status_code=respuesta.status_code,
            detail=respuesta.text,
        )

    return {
        "provider": "knox",
        "action": accion,
        "imei": imei,
        "status": "success",
        "message": "Registro Knox completado.",
        "data": respuesta.json() if respuesta.content else {},
    }
