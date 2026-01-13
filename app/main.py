from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.padlock.api import enrutador_padlock
from app.padlock.seguridad import validar_api_key


aplicacion = FastAPI(
    title="Padlock API",
    description="Microservicio para operaciones de bloqueo de dispositivos.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

def _custom_openapi():
    if aplicacion.openapi_schema:
        return aplicacion.openapi_schema
    schema = get_openapi(
        title=aplicacion.title,
        version=aplicacion.version,
        description=aplicacion.description,
        routes=aplicacion.routes,
    )
    schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"]["AloApiKey"] = {
        "type": "apiKey",
        "in": "header",
        "name": "alo-api-key",
    }
    schema["security"] = [{"AloApiKey": []}]
    aplicacion.openapi_schema = schema
    return aplicacion.openapi_schema


aplicacion.openapi = _custom_openapi

@aplicacion.middleware("http")
async def validar_api_key_middleware(request, call_next):
    ruta = request.url.path
    if ruta in ("/docs", "/openapi.json"):
        return await call_next(request)
    await validar_api_key(request)
    return await call_next(request)

aplicacion.include_router(enrutador_padlock)
app = aplicacion
