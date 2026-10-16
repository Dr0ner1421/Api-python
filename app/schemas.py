from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Literal

from app.constantes.swaggercostantes import (
    ACTUALIZAR_EMPRESA,
    ACTUALIZAR_ESTUDIANTE,
    ACTUALIZAR_SOLICITUD,
    ACTUALIZAR_USUARIO,
    ACTUALIZAR_USUARIO_GENERAL,
    REGISTRAR_EMPRESA,
    REGISTRAR_ESTUDIANTE,
    REGISTRAR_SOLICITUD,
    REGISTRAR_USUARIO,
    REGISTRAR_USUARIO_GENERAL,
)

class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Preferencias(BaseModel):
    precio: int = Field(ge=1, le=10)
    calidad: int = Field(ge=1, le=10)



class SolicitudRecomendacion(BaseModel):
    categoria: str

    preferencias: Preferencias

    metodo: Literal[
        "manhattan",
        "euclidiana"
    ] = "euclidiana"


class UsuarioResponse(InputModel):
    id: str
    tipo_cuenta: str
    nombres: str
    apellidos: str
    correo: str
    telefono: str
    pais_ciudad: str
    foto_perfil: str
    acepta_terminos: bool
    recibe_avisos: bool
    correo_verificado: bool
    correo_recuperacion: str


class UsuarioCreate(InputModel):
    tipo_cuenta: str
    nombres: str
    apellidos: str
    correo: str
    contrasena: str = Field(min_length=8)
    telefono: str
    pais_ciudad: str
    foto_perfil: str
    acepta_terminos: bool
    recibe_avisos: bool
    correo_verificado: bool
    correo_recuperacion: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": REGISTRAR_USUARIO
        }
    )




class UsuarioUpdate(InputModel):
    tipo_cuenta: str | None = None
    nombres: str | None = None
    apellidos: str | None = None
    correo: str | None = None
    contrasena: str | None = Field(default=None, min_length=8)
    confirmar_contrasena: str | None = None
    telefono: str | None = None
    pais_ciudad: str | None = None
    foto_perfil: str | None = None
    acepta_terminos: bool | None = None
    recibe_avisos: bool | None = None
    correo_verificado: bool | None = None
    correo_recuperacion: str | None = None

    model_config = ConfigDict(json_schema_extra={"example": ACTUALIZAR_USUARIO})

    @model_validator(mode="after")
    def validate_password_confirmation(self):
        if self.contrasena is not None or self.confirmar_contrasena is not None:
            if not self.contrasena or self.contrasena != self.confirmar_contrasena:
                raise ValueError("Envia contrasena y confirmar_contrasena iguales")
        return self


class EstudianteCreate(InputModel):
    usuario_id: str
    edad: int
    institucion_educativa: str
    correo_institucional: str
    programa_carrera: str
    habilidades_servicios_intereses: str
    portafolio_url: str
    catalogo_url: str
    modalidad: bool = Field(alias="Modalidad")
    disponibilidad_horarios: str

    model_config = ConfigDict(json_schema_extra={"example": REGISTRAR_ESTUDIANTE})


class EstudianteUpdate(InputModel):
    edad: int | None = None
    institucion_educativa: str | None = None
    correo_institucional: str | None = None
    programa_carrera: str | None = None
    habilidades_servicios_intereses: str | None = None
    portafolio_url: str | None = None
    catalogo_url: str | None = None
    modalidad: bool | None = Field(default=None, alias="Modalidad")
    disponibilidad_horarios: str | None = None

    model_config = ConfigDict(json_schema_extra={"example": ACTUALIZAR_ESTUDIANTE})


class EmpresaCreate(InputModel):
    usuario_id: str
    nombre_publico: str
    tipo_actividad_sector: str
    descripcion: str
    productos_servicios: str
    catalogo_sitio_web_tienda_portafolio: str
    red_social_tipo: str
    red_social_url: str
    correo_contacto_publico: str
    telefono_mensajeria: str
    ubicacion_atencion: str
    horario: str
    modalidad: str
    representacion_legitimidad: bool
    nombre_representante: str

    model_config = ConfigDict(json_schema_extra={"example": REGISTRAR_EMPRESA})


class EmpresaUpdate(InputModel):
    nombre_publico: str | None = None
    tipo_actividad_sector: str | None = None
    descripcion: str | None = None
    productos_servicios: str | None = None
    catalogo_sitio_web_tienda_portafolio: str | None = None
    red_social_tipo: str | None = None
    red_social_url: str | None = None
    correo_contacto_publico: str | None = None
    telefono_mensajeria: str | None = None
    ubicacion_atencion: str | None = None
    horario: str | None = None
    modalidad: str | None = None
    representacion_legitimidad: bool | None = None
    nombre_representante: str | None = None

    model_config = ConfigDict(json_schema_extra={"example": ACTUALIZAR_EMPRESA})


class UsuarioGeneralCreate(InputModel):
    usuario_id: str
    pais_ciudad_zona: str
    areas_interes: str
    solicitud_servicio: bool

    model_config = ConfigDict(json_schema_extra={"example": REGISTRAR_USUARIO_GENERAL})


class UsuarioGeneralUpdate(InputModel):
    usuario_id: str | None = None
    pais_ciudad_zona: str | None = None
    areas_interes: str | None = None
    solicitud_servicio: bool | None = None

    model_config = ConfigDict(
        json_schema_extra={"example": ACTUALIZAR_USUARIO_GENERAL}
    )


class SolicitudCreate(InputModel):
    usuario_id: str
    servicio: str
    descripcion: str
    categoria: str
    zona_general: str
    fecha_plazo_aproximado: str

    model_config = ConfigDict(json_schema_extra={"example": REGISTRAR_SOLICITUD})


class SolicitudUpdate(InputModel):
    usuario_id: str | None = None
    servicio: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    zona_general: str | None = None
    fecha_plazo_aproximado: str | None = None

    model_config = ConfigDict(json_schema_extra={"example": ACTUALIZAR_SOLICITUD})
