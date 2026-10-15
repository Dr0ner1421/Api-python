from typing import Any

from fastapi import APIRouter, Query

from app.crud import (
    create_linked_document,
    delete_document,
    get_document,
    include_related_document,
    list_documents,
    update_linked_document,
)
from app.constantes.swaggercostantes import (
    ACTUALIZAR_SOLICITUD,
    REGISTRAR_SOLICITUD,
)
from app.database import get_collection
from app.schemas import SolicitudCreate, SolicitudUpdate

router = APIRouter(prefix="/api/solicitudes-servicio", tags=["Solicitudes de servicio"])
collection = get_collection("solicitudes_servicio")
users = get_collection("usuarios")
SOLICITUD_USER_FIELDS = ("nombres", "apellidos", "correo")


def solicitud_response(solicitud: dict[str, Any]):
    return include_related_document(
        solicitud,
        users,
        profile_name="solicitud",
        relation_name="usuario",
        include_related_id=True,
        include_profile_id=True,
        include_root_id=False,
        related_fields=SOLICITUD_USER_FIELDS,
    )


@router.post(
    "",
    status_code=201,
    summary="Crear solicitud de servicio",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": REGISTRAR_SOLICITUD,
                }
            }
        }
    },
)
def create_solicitud(payload: SolicitudCreate):
    solicitud = create_linked_document(collection, users, payload)
    return solicitud_response(solicitud)


@router.get("", summary="Listar solicitudes de servicio")
def list_solicitudes(limit: int = Query(default=100, ge=1, le=500)):
    return [
        solicitud_response(solicitud)
        for solicitud in list_documents(collection, limit)
    ]


@router.get("/{item_id}", summary="Consultar solicitud por ID")
def get_solicitud(item_id: str):
    solicitud = get_document(collection, item_id)
    return solicitud_response(solicitud)


@router.patch(
    "/{item_id}",
    summary="Actualizar solicitud de servicio",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": ACTUALIZAR_SOLICITUD,
                }
            }
        }
    },
)
def update_solicitud(item_id: str, payload: SolicitudUpdate):
    solicitud = update_linked_document(collection, users, item_id, payload)
    return solicitud_response(solicitud)


@router.delete("/{item_id}", summary="Eliminar solicitud de servicio")
def delete_solicitud(item_id: str):
    return delete_document(collection, item_id)
