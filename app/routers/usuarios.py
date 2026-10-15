from fastapi import APIRouter, Query

from app.crud import (
    create_document,
    delete_document,
    get_document,
    list_documents,
    update_document,
)
from app.database import get_collection
from app.schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.security import hash_password

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])
collection = get_collection("usuarios")
HIDDEN_FIELDS = {"contrasena", "confirmar_contrasena"}


@router.post(
    "/usuarios",
    status_code=201,
    summary="Crear un nuevo usuario",
    response_model=UsuarioResponse,
)
def create_usuario(payload: UsuarioCreate):
    values = payload.model_dump()
    values["contrasena"] = hash_password(values["contrasena"])
    nuevo_usuario = create_document(
        collection,
        values,
        HIDDEN_FIELDS,
    )

    return nuevo_usuario


@router.get("", summary="Listar usuarios")
def list_usuarios(limit: int = Query(default=100, ge=1, le=500)):
    return [
        {key: value for key, value in user.items() if key not in HIDDEN_FIELDS}
        for user in list_documents(collection, limit)
    ]


@router.get("/{item_id}", summary="Consultar usuario por ID")
def get_usuario(item_id: str):
    return get_document(collection, item_id, HIDDEN_FIELDS)


@router.patch("/{item_id}", summary="Actualizar usuario")
def update_usuario(item_id: str, payload: UsuarioUpdate):
    values = payload.model_dump(exclude_unset=True)
    if "contrasena" in values:
        values["contrasena"] = hash_password(values["contrasena"])
    values.pop("confirmar_contrasena", None)
    return update_document(collection, item_id, values, HIDDEN_FIELDS)


@router.delete("/{item_id}", summary="Eliminar usuario")
def delete_usuario(item_id: str):
    return delete_document(collection, item_id)
