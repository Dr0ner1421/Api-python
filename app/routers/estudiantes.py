from fastapi import APIRouter, Query

from app.crud import (
    create_document,
    delete_document,
    get_document,
    list_documents,
    update_document,
)
from app.database import get_collection
from app.schemas import EstudianteCreate, EstudianteUpdate

router = APIRouter(prefix="/api/estudiantes", tags=["Estudiantes"])
collection = get_collection("estudiantes")


@router.post("", status_code=201)
def create_estudiante(payload: EstudianteCreate):
    return create_document(collection, payload)


@router.get("")
def list_estudiantes(limit: int = Query(default=100, ge=1, le=500)):
    return list_documents(collection, limit)


@router.get("/{item_id}")
def get_estudiante(item_id: str):
    return get_document(collection, item_id)


@router.patch("/{item_id}")
def update_estudiante(item_id: str, payload: EstudianteUpdate):
    return update_document(collection, item_id, payload)


@router.delete("/{item_id}")
def delete_estudiante(item_id: str):
    return delete_document(collection, item_id)
