from fastapi import APIRouter

from app.schemas import SolicitudRecomendacion
from app.services.recomendador import recomendar




router = APIRouter(
    prefix="/recomendaciones",
    tags=["Recomendaciones"]
)


@router.post("/")
def obtener_recomendaciones(
    solicitud: SolicitudRecomendacion
):

    p = solicitud.preferencias

    usuario =[
        p.precio,
        p.calidad
    ] 


    negocios = [
        {
            "id": 1,
            "nombre": "TecnoFix",
            "perfil": (2, 2)
        },
        {
            "id": 2,
            "nombre": "PC Solutions",
            "perfil": (6, 9)
        },
        {
            "id": 3,
            "nombre": "CompuExpress",
            "perfil": (8, 7)
        },
        {
            "id": 4,
            "nombre": "Panaderia",
            "perfil": (2, 3)
        }
        
    ]



    #calcula la recomendacion

    resultados = recomendar(
        usuario,
        negocios,
        solicitud.metodo
    )



    return {
        "success" : True,
        "metodo": solicitud.metodo,
        "recomendaciones": resultados     
    }