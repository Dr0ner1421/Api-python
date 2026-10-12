from fastapi import APIRouter, Query

from app.crud import (
    create_document,
    delete_document,
    get_document,
    list_documents,
    update_document,
)
from app.database import get_collection
from app.schemas import UsuarioCreate, UsuarioUpdate
from app.security import hash_password

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])
collection = get_collection("usuarios")
HIDDEN_FIELDS = {"contrasena", "confirmar_contrasena"}


@router.post("", status_code=201)
def create_usuario(payload: UsuarioCreate):
    values = payload.model_dump(exclude={"confirmar_contrasena"})
    values["contrasena"] = hash_password(values["contrasena"])
    return create_document(collection, values, HIDDEN_FIELDS)


@router.get("")
def list_usuarios(limit: int = Query(default=100, ge=1, le=500)):
    return [
        {key: value for key, value in user.items() if key not in HIDDEN_FIELDS}
        for user in list_documents(collection, limit)
    ]


@router.get("/{item_id}")
def get_usuario(item_id: str):
    return get_document(collection, item_id, HIDDEN_FIELDS)


@router.patch("/{item_id}")
def update_usuario(item_id: str, payload: UsuarioUpdate):
    values = payload.model_dump(exclude_unset=True)
    if "contrasena" in values:
        values["contrasena"] = hash_password(values["contrasena"])
    values.pop("confirmar_contrasena", None)
    return update_document(collection, item_id, values, HIDDEN_FIELDS)


@router.delete("/{item_id}")
def delete_usuario(item_id: str):
    return delete_document(collection, item_id)
