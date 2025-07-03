from pydantic import BaseModel, ConfigDict, EmailStr

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
    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    users: list[UserPublic]
    
class Token(BaseModel):
    access_token: str
    token_type: str
    