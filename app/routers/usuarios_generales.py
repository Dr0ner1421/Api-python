from fastapi import APIRouter, Query

from app.crud import (
    create_linked_document,
    delete_document,
    get_document,
    list_documents,
    update_linked_document,
)
from app.database import get_collection
from app.schemas import UsuarioGeneralCreate, UsuarioGeneralUpdate

router = APIRouter(prefix="/api/usuarios-generales", tags=["Usuarios generales"])
collection = get_collection("usuarios_generales")
users = get_collection("usuarios")


@router.post("", status_code=201)
def create_usuario_general(payload: UsuarioGeneralCreate):
    return create_linked_document(collection, users, payload)


@router.get("")
def list_usuarios_generales(limit: int = Query(default=100, ge=1, le=500)):
    return list_documents(collection, limit)


@router.get("/{item_id}")
def get_usuario_general(item_id: str):
    return get_document(collection, item_id)


@router.patch("/{item_id}")
def update_usuario_general(item_id: str, payload: UsuarioGeneralUpdate):
    return update_linked_document(collection, users, item_id, payload)


@router.delete("/{item_id}")
def delete_usuario_general(item_id: str):
    return delete_document(collection, item_id)
