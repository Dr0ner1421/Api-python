from math import isfinite
from numbers import Real

from fastapi import APIRouter, HTTPException

from app.database import (
    HEURISTIC_CONNECTIONS_COLLECTION,
    HEURISTIC_NODES_COLLECTION,
    get_collection,
)
from app.schemas import (
    BusquedaHeuristicaRequest,
    BusquedaHeuristicaResponse,
    NodoVisitado,
)

router = APIRouter(prefix="/api/busquedas", tags=["Búsqueda heurística"])


@router.post("/heuristica", response_model=BusquedaHeuristicaResponse)
def buscar_ruta_heuristica(
    payload: BusquedaHeuristicaRequest,
) -> BusquedaHeuristicaResponse:
    node_documents = list(
        get_collection(HEURISTIC_NODES_COLLECTION).find(
            {}, {"nombre": 1, "heuristica_minutos": 1}
        )
    )
    if not node_documents:
        raise HTTPException(
            status_code=409,
            detail="No hay nodos para buscar. Ejecuta scripts/cargar_grafo_heuristico.py.",
        )

    heuristics: dict[str, float] = {}
    for node in node_documents:
        node_id = node["_id"]
        value = node.get("heuristica_minutos")
        if (
            not isinstance(node_id, str)
            or not isinstance(value, Real)
            or isinstance(value, bool)
            or not isfinite(value)
            or value < 0
        ):
            raise HTTPException(
                status_code=409,
                detail="Los nodos del grafo deben tener un id de texto y una heurística numérica no negativa.",
            )
        heuristics[node_id] = float(value)

    if payload.inicio not in heuristics or payload.objetivo not in heuristics:
        missing = [
            node_id
            for node_id in (payload.inicio, payload.objetivo)
            if node_id not in heuristics
        ]
        raise HTTPException(
            status_code=404,
            detail=f"No existe(n) el/los nodo(s): {', '.join(missing)}",
        )

    adjacency = {node_id: [] for node_id in heuristics}
    connection_documents = get_collection(HEURISTIC_CONNECTIONS_COLLECTION).find(
        {}, {"origen": 1, "destino": 1}
    )
    for connection in connection_documents:
        origin = connection.get("origen")
        destination = connection.get("destino")
        if (
            not isinstance(origin, str)
            or not isinstance(destination, str)
            or origin not in adjacency
            or destination not in adjacency
        ):
            raise HTTPException(
                status_code=409,
                detail="Hay una conexión que referencia un nodo inexistente en el grafo.",
            )
        adjacency[origin].append(destination)

    current = payload.inicio
    route = [current]
    visited: set[str] = set()
    trace: list[NodoVisitado] = []

    while True:
        trace.append(
            NodoVisitado(
                nodo=current,
                heuristica_minutos=heuristics[current],
            )
        )
        if current == payload.objetivo:
            return BusquedaHeuristicaResponse(
                algoritmo="greedy_heuristico_local",
                encontrada=True,
                inicio=payload.inicio,
                objetivo=payload.objetivo,
                ruta=route,
                nodos_visitados=trace,
                mensaje=(
                    "Objetivo encontrado. La heurística es una estimación "
                    "guardada en MongoDB, no un tiempo real."
                ),
            )

        visited.add(current)
        candidates = [
            neighbor
            for neighbor in adjacency[current]
            if neighbor not in visited
        ]
        if not candidates:
            return BusquedaHeuristicaResponse(
                algoritmo="greedy_heuristico_local",
                encontrada=False,
                inicio=payload.inicio,
                objetivo=payload.objetivo,
                ruta=[],
                nodos_visitados=trace,
                mensaje=(
                    "No se encontró una ruta con la búsqueda heurística local. "
                    "El algoritmo no retrocede cuando llega a un callejón sin salida."
                ),
            )

        current = min(candidates, key=lambda node_id: (heuristics[node_id], node_id))
        route.append(current)
