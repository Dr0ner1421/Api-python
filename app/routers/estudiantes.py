from fastapi import APIRouter, Query

from app.crud import (
    create_linked_document,
    delete_document,
    get_document,
    include_related_document,
    list_related_documents,
    update_document,
)
from app.constantes.swaggercostantes import REGISTRAR_ESTUDIANTE
from app.database import get_collection
from app.schemas import EstudianteCreate, EstudianteUpdate

router = APIRouter(prefix="/api/estudiantes", tags=["Estudiantes"])
collection = get_collection("estudiantes")
users = get_collection("usuarios")
HIDDEN_USER_FIELDS = {"contrasena", "confirmar_contrasena"}


@router.post(
    "",
    status_code=201,
    summary="Crear perfil de estudiante",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": REGISTRAR_ESTUDIANTE,
                }
            }
        }
    },
)
def create_estudiante(payload: EstudianteCreate):
    student = create_linked_document(collection, users, payload)
    return include_related_document(
        student,
        users,
        profile_name="estudiante",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.get("", summary="Listar estudiantes con sus usuarios")
def list_estudiantes(limit: int = Query(default=100, ge=1, le=500)):
    return list_related_documents(
        collection,
        users,
        limit,
        profile_name="estudiante",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.get("/{item_id}", summary="Consultar estudiante por ID")
def get_estudiante(item_id: str):
    student = get_document(collection, item_id)
    return include_related_document(
        student,
        users,
        profile_name="estudiante",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.patch("/{item_id}", summary="Actualizar perfil de estudiante")
def update_estudiante(item_id: str, payload: EstudianteUpdate):
    student = update_document(collection, item_id, payload)
    return include_related_document(
        student,
        users,
        profile_name="estudiante",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.delete("/{item_id}", summary="Eliminar perfil de estudiante")
def delete_estudiante(item_id: str):
    return delete_document(collection, item_id)
