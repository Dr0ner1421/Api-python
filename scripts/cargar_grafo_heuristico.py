import sys
from pathlib import Path

from pymongo import UpdateOne

# Allow both `python -m scripts.cargar_grafo_heuristico` and direct file execution.
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.database import (
    HEURISTIC_CONNECTIONS_COLLECTION,
    HEURISTIC_NODES_COLLECTION,
    client,
    database,
)

NODES = (
    {"_id": "A", "nombre": "Casa", "heuristica_minutos": 25, "simulado": True},
    {"_id": "B", "nombre": "Avenida B", "heuristica_minutos": 20, "simulado": True},
    {"_id": "C", "nombre": "Avenida C", "heuristica_minutos": 15, "simulado": True},
    {"_id": "D", "nombre": "Calle D", "heuristica_minutos": 18, "simulado": True},
    {"_id": "E", "nombre": "Calle E sin salida", "heuristica_minutos": 30, "simulado": True},
    {"_id": "F", "nombre": "Calle F", "heuristica_minutos": 10, "simulado": True},
    {"_id": "G", "nombre": "Calle G sin salida", "heuristica_minutos": 25, "simulado": True},
    {"_id": "H", "nombre": "Calle H sin salida", "heuristica_minutos": 40, "simulado": True},
    {"_id": "I", "nombre": "Calle I", "heuristica_minutos": 5, "simulado": True},
    {"_id": "J", "nombre": "Universidad", "heuristica_minutos": 0, "simulado": True},
)

CONNECTIONS = (
    {"_id": "A-B", "origen": "A", "destino": "B", "simulado": True},
    {"_id": "A-C", "origen": "A", "destino": "C", "simulado": True},
    {"_id": "B-D", "origen": "B", "destino": "D", "simulado": True},
    {"_id": "B-E", "origen": "B", "destino": "E", "simulado": True},
    {"_id": "C-F", "origen": "C", "destino": "F", "simulado": True},
    {"_id": "C-G", "origen": "C", "destino": "G", "simulado": True},
    {"_id": "D-H", "origen": "D", "destino": "H", "simulado": True},
    {"_id": "F-I", "origen": "F", "destino": "I", "simulado": True},
    {"_id": "I-J", "origen": "I", "destino": "J", "simulado": True},
)


def main() -> None:
    try:
        client.admin.command("ping")
        print(f"Base seleccionada: {database.name}")

        nodes_result = database[HEURISTIC_NODES_COLLECTION].bulk_write(
            [
                UpdateOne(
                    {"_id": node["_id"]},
                    {"$set": {key: value for key, value in node.items() if key != "_id"}},
                    upsert=True,
                )
                for node in NODES
            ],
            ordered=True,
        )
        connections_result = database[HEURISTIC_CONNECTIONS_COLLECTION].bulk_write(
            [
                UpdateOne(
                    {"_id": connection["_id"]},
                    {
                        "$set": {
                            key: value
                            for key, value in connection.items()
                            if key != "_id"
                        }
                    },
                    upsert=True,
                )
                for connection in CONNECTIONS
            ],
            ordered=True,
        )
        print(
            "Grafo cargado correctamente. "
            f"Nodos insertados/actualizados: {nodes_result.upserted_count}/"
            f"{nodes_result.modified_count}; conexiones: "
            f"{connections_result.upserted_count}/"
            f"{connections_result.modified_count}."
        )
    finally:
        client.close()


if __name__ == "__main__":
    main()
