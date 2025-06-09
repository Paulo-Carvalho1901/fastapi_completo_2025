from pydantic import BaseModel, EmailStr

class Message(BaseModel):
    message: str


# Montando a estrutura schema "contrato" do usuario
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# Criando um schema publico que não retorna a senha.
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

# 
class UserDB(UserSchema):
    id: int

class UserList(BaseModel):
    users: list[UserPublic]
    