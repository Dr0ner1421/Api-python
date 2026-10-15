from fastapi import APIRouter, Query

from app.crud import (
    create_linked_document,
    delete_document,
    get_document,
    include_related_document,
    list_related_documents,
    update_linked_document,
)
from app.database import get_collection
from app.schemas import UsuarioGeneralCreate, UsuarioGeneralUpdate

router = APIRouter(prefix="/api/usuarios-generales", tags=["Usuarios generales"])
collection = get_collection("usuarios_generales")
users = get_collection("usuarios")
HIDDEN_USER_FIELDS = {"contrasena", "confirmar_contrasena"}


@router.post("", status_code=201, summary="Crear perfil de usuario general")
def create_usuario_general(payload: UsuarioGeneralCreate):
    profile = create_linked_document(collection, users, payload)
    return include_related_document(
        profile,
        users,
        profile_name="usuario_general",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.get("", summary="Listar perfiles de usuarios generales")
def list_usuarios_generales(limit: int = Query(default=100, ge=1, le=500)):
    return list_related_documents(
        collection,
        users,
        limit,
        profile_name="usuario_general",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.get("/{item_id}", summary="Consultar perfil de usuario general por ID")
def get_usuario_general(item_id: str):
    profile = get_document(collection, item_id)
    return include_related_document(
        profile,
        users,
        profile_name="usuario_general",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.patch("/{item_id}", summary="Actualizar perfil de usuario general")
def update_usuario_general(item_id: str, payload: UsuarioGeneralUpdate):
    profile = update_linked_document(collection, users, item_id, payload)
    return include_related_document(
        profile,
        users,
        profile_name="usuario_general",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.delete("/{item_id}", summary="Eliminar perfil de usuario general")
def delete_usuario_general(item_id: str):
    return delete_document(collection, item_id)
