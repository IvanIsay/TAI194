from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional,List
from modelsPydantic import modelUsuario, modelAuth
from genToken import createToken
from DB.conexion import Session,engine,Base
from models.modelsDB import User 

app= FastAPI(
    title="Mi primer API 194",
    description="Ivan Isay Guerra L.",
    version="1.0.1"
)

Base.metadata.create_all(bind= engine)


#EndPoint Inicio
@app.get('/',tags=['Inicio'])
def home():
    return {'hello':'world fastApi'}



# --------- CRUD de Usuarios ----------- #


#EndPoint CONSULTA TODOS
@app.get('/todosUsuarios',tags=['Operaciones CRUD'])
def leer():
    db=Session()
    try:
        consulta= db.query(User).all()
        return JSONResponse(content= jsonable_encoder(consulta))
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={"message": "No fue posible consultar",
                                      "Error": str(e) })
    finally:
        db.close()
        
        
        
#EndPoint buscar por ID
@app.get('/usuario/{id}',tags=['Operaciones CRUD'])
def leeruno(id:int):
    db=Session()
    try:
        consulta1= db.query(User).filter(User.id == id).first()
        if not consulta1:
            return JSONResponse(status_code=404,content= {"mensaje":"Usuario no encontrado"})
        
        return JSONResponse(content= jsonable_encoder(consulta1))
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={"message": "No fue posible consultar",
                                      "Error": str(e) })
    finally:
        db.close()       
        
             
    
#EndPoint agregar Usuario
@app.post('/usuarios/',response_model=modelUsuario,tags=['Operaciones CRUD'])
def guardar(usuario:modelUsuario):
    db=Session()
    try:
        db.add(User(**usuario.model_dump()))
        db.commit()
        return JSONResponse(status_code=201,
                            content={"message": "usuario Guardado",
                                      "usuario": usuario.model_dump() })
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={"message": "No fue posible guardar",
                                      "Error": str(e) })
    finally:
        db.close()



#Endpoint para actualizar usuario
@app.put('/usuario/{id}', response_model=modelUsuario, tags=['Operaciones CRUD'])
def actualizar(id:int,usuarioActualizado:modelUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Actualizar campos
        for key, value in usuarioActualizado.model_dump().items():
            setattr(usuario, key, value)

        db.commit()
        return JSONResponse(status_code=200, content={"message": "Usuario actualizado", "usuario": usuarioActualizado.model_dump()})

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "No fue posible actualizar", "Error": str(e)})
    finally:
        db.close()


#Endpoint para eliminar usuario
@app.delete('/usuario/{id}',tags=['Operaciones CRUD'])
def eliminar(id:int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(usuario)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Usuario eliminado"})

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "No fue posible eliminar", "Error": str(e)})
    finally:
        db.close()
        
        

# --------------- AUtenticacion ----------- #

#EndPoint para generar Token
@app.post('/auth',tags=['Autentificacion'])
def auth(credenciales:modelAuth):
    if credenciales.mail == 'ivan@example.com' and credenciales.passw == '123456789':
        token:str= createToken(credenciales.model_dump())
        print(token)
        return {"Aviso:":"Token Generado"}
    else:
        return {"Aviso:":"Usuario no cuenta con permiso"}