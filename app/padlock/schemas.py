from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class SolicitudAccionProveedor(BaseModel):
    imei: str = Field(..., min_length=1)
    payload: Optional[Dict[str, Any]] = None


class RespuestaAccionDispositivo(BaseModel):
    provider: str
    action: str
    imei: str
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


class SolicitudAccionUnificada(BaseModel):
    provider: str = Field(..., min_length=1)
    action: str = Field(..., min_length=1)
    imei: str = Field(..., min_length=1)
    payload: Optional[Dict[str, Any]] = None
