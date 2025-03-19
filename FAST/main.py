from fastapi import FastAPI,HTTPException
from typing import Optional,List
from models import modelUsuario, modelAuth
from genToken import createToken 

app= FastAPI(
    title="Mi primer API 194",
    description="Ivan Isay Guerra L.",
    version="1.0.1"
)

usuarios=[
    {"id":1, "nombre":"Ivan","edad":37, "correo":"Ivan@example.com"},
    {"id":2, "nombre":"Fernando","edad":21, "correo":"fenando@example.com"},
    {"id":3, "nombre":"Karla","edad":21, "correo":"karla@example.com"},
    {"id":4, "nombre":"Gonzalo","edad":21, "correo":"gonzalo@example.com"},
]


#ruta o EndPointcl
@app.get('/',tags=['Inicio'])
def home():
    return {'hello':'world fastApi'}



#EndPoint para generar Token
@app.post('/auth',tags=['Autentificacion'])
def auth(credenciales:modelAuth):
    if credenciales.mail == 'ivan@example.com' and credenciales.passw == '123456789':
        token:str= createToken(credenciales.model_dump())
        print(token)
        return {"Aviso:":"Token Generado"}
    else:
        return {"Aviso:":"Usuario no cuenta con permiso"}
        



#EndPoint CONSULTA TODOS
@app.get('/todosUsuarios',response_model=List[modelUsuario],tags=['Operaciones CRUD'])
def leer():
    return usuarios 


#EndPoint POST
@app.post('/usuarios/',response_model=modelUsuario,tags=['Operaciones CRUD'])
def guardar(usuario:modelUsuario):
    for usr in usuarios:
        if usr["id"]== usuario.id:
            raise HTTPException(status_code=400,detail="El usuario ya existe")
    
    usuarios.append(usuario)
    return usuario 



#Endpoint para actualizar
@app.put('/usuarios/{id}', response_model=modelUsuario, tags=['Operaciones CRUD'])
def actualizar(id:int,usuarioActualizado:modelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index]= usuarioActualizado.model_dump()
            return usuarios[index]
    raise HTTPException(status_code=400,detail="El usuario no existe")    


@app.delete('/usuarios/{id}',tags=['Operaciones CRUD'])
def actualizar(id:int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            #usuarios[index].update(usuarioActualizado)
            return usuarios[index]
    raise HTTPException(status_code=400,detail="El usuario no existe")    