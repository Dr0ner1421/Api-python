from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel
from pymongo.collection import Collection


def parse_object_id(value: str, field: str = "Identificador") -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(
            status_code=400,
            detail=f"{field} debe ser un ObjectId valido de MongoDB (24 caracteres hexadecimales)",
        )
    return ObjectId(value)


def serialize(document: dict[str, Any], hidden_fields: set[str] | None = None):
    result = dict(document)
    result["id"] = str(result.pop("_id"))

    for key, value in result.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)

    for field in hidden_fields or set():
        result.pop(field, None)

    return result


def create_document(
    collection: Collection,
    payload: BaseModel | dict[str, Any],
    hidden_fields: set[str] | None = None,
):
    document = (
        payload.model_dump(by_alias=True)
        if isinstance(payload, BaseModel)
        else dict(payload)
    )
    result = collection.insert_one(document)
    document["_id"] = result.inserted_id
    return serialize(document, hidden_fields)


def list_documents(collection: Collection, limit: int = 100):
    return [serialize(document) for document in collection.find().limit(limit)]


def get_document(
    collection: Collection,
    item_id: str,
    hidden_fields: set[str] | None = None,
):
    document = collection.find_one({"_id": parse_object_id(item_id)})
    if document is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return serialize(document, hidden_fields)


def update_document(
    collection: Collection,
    item_id: str,
    payload: BaseModel | dict[str, Any],
    hidden_fields: set[str] | None = None,
):
    document_id = parse_object_id(item_id)
    changes = (
        payload.model_dump(exclude_unset=True, by_alias=True)
        if isinstance(payload, BaseModel)
        else dict(payload)
    )
    if not changes:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    collection.update_one({"_id": document_id}, {"$set": changes})
    return get_document(collection, item_id, hidden_fields)


def delete_document(collection: Collection, item_id: str):
    result = collection.delete_one({"_id": parse_object_id(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": "Registro eliminado"}


def validate_reference(
    target_collection: Collection,
    reference_id: str,
    source_collection: Collection,
    current_document_id: ObjectId | None = None,
):
    object_id = parse_object_id(reference_id, "usuario_id")
    if target_collection.find_one({"_id": object_id}) is None:
        raise HTTPException(status_code=404, detail="Usuario relacionado no encontrado")

    query: dict[str, Any] = {"usuario_id": object_id}
    if current_document_id is not None:
        query["_id"] = {"$ne": current_document_id}
    if source_collection.find_one(query) is not None:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya tiene un registro relacionado",
        )
    return object_id


def create_linked_document(
    collection: Collection,
    target_collection: Collection,
    payload: BaseModel,
):
    document = payload.model_dump(by_alias=True)
    document["usuario_id"] = validate_reference(
        target_collection,
        document["usuario_id"],
        collection,
    )
    result = collection.insert_one(document)
    document["_id"] = result.inserted_id
    return serialize(document)


def update_linked_document(
    collection: Collection,
    target_collection: Collection,
    item_id: str,
    payload: BaseModel,
):
    document_id = parse_object_id(item_id)
    changes = payload.model_dump(exclude_unset=True, by_alias=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    if "usuario_id" in changes:
        changes["usuario_id"] = validate_reference(
            target_collection,
            changes["usuario_id"],
            collection,
            document_id,
        )

    collection.update_one({"_id": document_id}, {"$set": changes})
    return get_document(collection, item_id)
