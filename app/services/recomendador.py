
import math


# Distancia Manhattan
def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# Distancia Euclidiana
def euclidiana(x1, y1, x2, y2):
    return math.sqrt(
        (x2 - x1)**2 + (y2 - y1)**2
    )



def recomendar(usuario, negocios, metodo="euclidiana"):

    resultados = []

    for negocio in negocios:

        # Obtener las coordenadas del usuario y del negocio
        x1, y1 = usuario
        x2, y2 = negocio["perfil"]


        if metodo == "manhattan":
            distancia = manhattan(x1, y1, x2, y2)
        else:
            distancia = euclidiana(x1, y1, x2, y2)


        resultados.append({
            "id": negocio["id"],
            "nombre": negocio["nombre"],
            "distancia": round(distancia, 2)
        })

    # Mostrar primero los negocios más similares
    resultados.sort(key=lambda x: x["distancia"])

    return resultados
