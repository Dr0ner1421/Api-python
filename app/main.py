from fastapi import FastAPI

from app.routers import (
    busquedas,
    empresas,
    estudiantes,
    solicitudes,
    usuarios,
    usuarios_generales,
)

app = FastAPI(
    title="API de servicios",
    description="API para usuarios, perfiles y solicitudes de servicio",
    version="1.0.0",
)

app.include_router(usuarios.router)
app.include_router(estudiantes.router)
app.include_router(empresas.router)
app.include_router(usuarios_generales.router)
app.include_router(solicitudes.router)
app.include_router(busquedas.router)
