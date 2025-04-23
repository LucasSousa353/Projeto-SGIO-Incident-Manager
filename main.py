from fastapi import FastAPI
from app.api import routes 

app = FastAPI(
    title="SGIO - Sistema de Gerenciamento de Incidentes Operacionais",
    version="1.0.0"
)

app.include_router(routes.router)
