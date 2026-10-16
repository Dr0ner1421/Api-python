from fastapi import APIRouter, Query

from app.crud import (
    create_linked_document,
    delete_document,
    get_document,
    include_related_document,
    list_related_documents,
    update_document,
)
from app.constantes.swaggercostantes import REGISTRAR_EMPRESA
from app.database import get_collection
from app.schemas import EmpresaCreate, EmpresaUpdate

router = APIRouter(
    prefix="/api/empresas-micro-negocios",
    tags=["Empresas y micro negocios"],
)
collection = get_collection("empresas_micro_negocios")
users = get_collection("usuarios")
HIDDEN_USER_FIELDS = {"contrasena", "confirmar_contrasena"}


@router.post(
    "",
    status_code=201,
    summary="Crear perfil de empresa",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": REGISTRAR_EMPRESA,
                }
            }
        }
    },
)
def create_empresa(payload: EmpresaCreate):
    company = create_linked_document(collection, users, payload)
    return include_related_document(
        company,
        users,
        profile_name="empresa",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.get("", summary="Listar empresas con sus usuarios")
def list_empresas(limit: int = Query(default=100, ge=1, le=500)):
    return list_related_documents(
        collection,
        users,
        limit,
        profile_name="empresa",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.get(
        "/{item_id}", 
        summary="Consultar empresa por ID")

def get_empresa(item_id: str):

    company = get_document(collection, item_id)

    return include_related_document(
        company,
        users,
        profile_name="empresa",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.patch(
        "/{item_id}", 
        summary="Actualizar perfil de empresa")

def update_empresa(item_id: str, payload: EmpresaUpdate):
    
    company = update_document(collection, item_id, payload)

    return include_related_document(
        company,
        users,
        profile_name="empresa",
        hidden_related_fields=HIDDEN_USER_FIELDS,
    )


@router.delete(
        "/{item_id}", 
        summary="Eliminar perfil de empresa")

def delete_empresa(item_id: str):
    
    return delete_document(collection, item_id)
