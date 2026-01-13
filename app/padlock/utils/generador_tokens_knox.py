import base64
import json
import time
import uuid
from typing import Tuple

import httpx
import jwt
from cryptography.hazmat.primitives import serialization

from app.padlock.config import (
    KNOX_ALGORITMO,
    KNOX_AUDIENCIA,
    KNOX_CLIENT_IDENTIFIER_CO,
    KNOX_EXPIRACION_SEG,
    KNOX_RUTA_LLAVES_CO,
    KNOX_URL_BASE,
    KNOX_VALIDEZ_MINUTOS,
)


def _cargar_llaves(ruta_llaves: str) -> Tuple[object, str]:
    with open(ruta_llaves, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)

    der_privada = base64.b64decode(data["Private"].strip())
    der_publica = base64.b64decode(data["Public"].strip())
    llave_privada = serialization.load_der_private_key(der_privada, password=None)
    publica_b64 = base64.b64encode(der_publica).decode("ascii")
    return llave_privada, publica_b64


def _jwtid() -> str:
    return f"{uuid.uuid1()}{uuid.uuid1()}"


def _generar_jwt_client_identifier(ruta_llaves: str, identificador_cliente: str) -> str:
    llave_privada, publica_b64 = _cargar_llaves(ruta_llaves)
    ahora = int(time.time())
    payload = {
        "clientIdentifier": identificador_cliente,
        "publicKey": publica_b64,
        "aud": KNOX_AUDIENCIA,
        "iat": ahora,
        "exp": ahora + KNOX_EXPIRACION_SEG,
        "jti": _jwtid(),
    }
    return jwt.encode(payload, llave_privada, algorithm=KNOX_ALGORITMO)


def _generar_jwt_access_token(ruta_llaves: str, token_acceso: str) -> str:
    llave_privada, publica_b64 = _cargar_llaves(ruta_llaves)
    ahora = int(time.time())
    payload = {
        "accessToken": token_acceso,
        "publicKey": publica_b64,
        "aud": KNOX_AUDIENCIA,
        "iat": ahora,
        "exp": ahora + KNOX_EXPIRACION_SEG,
        "jti": _jwtid(),
    }
    return jwt.encode(payload, llave_privada, algorithm=KNOX_ALGORITMO)


def _solicitar_access_token(jwt_client_identifier: str, clave_publica_b64: str) -> str:
    if not KNOX_URL_BASE:
        raise RuntimeError("KNOX_URL_BASE no configurado.")
    url = f"{KNOX_URL_BASE.rstrip('/')}/ams/v1/users/accesstoken"
    cuerpo = {
        "clientIdentifierJwt": jwt_client_identifier,
        "base64EncodedStringPublicKey": clave_publica_b64,
        "validityForAccessTokenInMinutes": KNOX_VALIDEZ_MINUTOS,
    }
    encabezados = {"Content-Type": "application/json", "Accept": "application/json"}
    with httpx.Client(timeout=30) as cliente:
        respuesta = cliente.post(url, json=cuerpo, headers=encabezados)
    if respuesta.status_code != 200:
        raise RuntimeError(f"HTTP Error {respuesta.status_code}: {respuesta.text}")
    data = respuesta.json()
    if "accessToken" not in data:
        raise RuntimeError(f"No llego accessToken: {data}")
    return data["accessToken"]


def obtener_token_knox_co() -> str:
    if not KNOX_CLIENT_IDENTIFIER_CO:
        raise RuntimeError("KNOX_CLIENT_IDENTIFIER_CO no configurado.")
    _, clave_publica_b64 = _cargar_llaves(KNOX_RUTA_LLAVES_CO)
    jwt_client_identifier = _generar_jwt_client_identifier(
        KNOX_RUTA_LLAVES_CO, KNOX_CLIENT_IDENTIFIER_CO
    )
    token_acceso = _solicitar_access_token(jwt_client_identifier, clave_publica_b64)
    return _generar_jwt_access_token(KNOX_RUTA_LLAVES_CO, token_acceso)
