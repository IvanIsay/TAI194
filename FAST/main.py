from fastapi import FastAPI,HTTPException
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


#EndPoint CONSULTA TODOS
@app.get('/todosUsuarios',tags=['Operaciones CRUD'])
def leer():
    return {'Usuarios Registrados: ' : usuarios }


#EndPoint POST
@app.post('/usuarios/',tags=['Operaciones CRUD'])
def guardar(usuario:dict):
    for usr in usuarios:
        if usr["id"]== usuario.get("id"):
            raise HTTPException(status_code=400,detail="El usuario ya existe")
    
    usuarios.append(usuario)
    return usuario 


#Endpoint para actualizar
@app.put('/usuarios/{id}',tags=['Operaciones CRUD'])
def actualizar(id:int,usuarioActualizado:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuarioActualizado)
            return usuarios[index]
    raise HTTPException(status_code=400,detail="El usuario no existe")    