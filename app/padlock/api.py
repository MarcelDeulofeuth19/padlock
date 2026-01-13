from fastapi import APIRouter
from app.padlock.endpoints.knox import enrutador as enrutador_knox
from app.padlock.endpoints.motosafe import enrutador as enrutador_motosafe
from app.padlock.endpoints.nuovo import enrutador as enrutador_nuovo
from app.padlock.endpoints.trustonic import enrutador as enrutador_trustonic
from app.padlock.endpoints.proveedor import enrutador as enrutador_proveedor

enrutador_padlock = APIRouter()
enrutador_padlock.include_router(enrutador_knox)
enrutador_padlock.include_router(enrutador_trustonic)
enrutador_padlock.include_router(enrutador_nuovo)
enrutador_padlock.include_router(enrutador_motosafe)
enrutador_padlock.include_router(enrutador_proveedor)
