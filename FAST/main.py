from fastapi import FastAPI
from typing import Optional

app= FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra L.",
    version="1.0.1"
)

usuarios=[
    {"id":1, "nombre":"Ivan","edad":37},
    {"id":2, "nombre":"Fernando","edad":21},
    {"id":3, "nombre":"Karla","edad":21},
    {"id":4, "nombre":"Gonzalo","edad":21},
]

#ruta o EndPoint
@app.get('/',tags=['Inicio'])
def home():
    return {'hello':'world fastApi'}

#EndPoint promedio
@app.get('/promedio',tags=['Mi calificaion TAI'])
def promedio():
    return 10.5

#EndPoint con parametro obligatorio
@app.get('/usuario/{id}',tags=['Endpoint parametro Obligatorio '])
def consultausuario(id:int):
    #caso ficticio de busqueda en BD
    return {"Se encontro el usuario":id}


#EndPoint con parametro opcional

@app.get('/usuario2/',tags=['Endpoint parametro Opcional '])
def consultausuario2(id: Optional[int]=None):
   
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje":"usuario encontrado","El usuario es: ":usuario}
        return{"mensaje":f"No se encontro el id: {id}"}
    return{"mensaje":"No se proporciono un Id"}


#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}