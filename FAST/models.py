from pydantic import BaseModel,Field,EmailStr


class modelUsuario(BaseModel):
    id:int = Field(...,gt=0, description=" Id siempre debe ser positivo")
    nombre:str= Field(..., min_lenth= 1, max_length=85, description=" solo letras y espacios min 1 max 85")
    edad: int
    correo:str


class modelAuth(BaseModel):
    mail: EmailStr
    passw:str= Field(..., min_lenth= 8, strip_whitespace=True, description="solo letras sin espacios min 8")
   