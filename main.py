from fastapi import Depends, FastAPI, HTTPException, status

from schema import Message, UserDB, UserList, UserPublic, UserSchema
from sqlalchemy import select

from models import User
from database import get_session



app = FastAPI(title='Curso de FastAPI')
database = []


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def get_root():
    return {"message": "Olá mundo!"}


# POST CREATE
@app.post('/users/', status_code=status.HTTP_201_CREATED,response_model=UserPublic) # Saída dos dados
def create_user(user: UserSchema, session = Depends(get_session)): # function anotation (anotação de função) ou 'anotação de tipo' entrada dos dados

    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email)))
   
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(detail='Username already exists', status_code=status.HTTP_409_CONFLICT)
        
        elif db_user.email == user.email:
            raise HTTPException(detail='Email already exists', status_code=status.HTTP_409_CONFLICT)
       
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


# GET TODOS OS USERS
@app.get('/users/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users(session = Depends(get_session)):

    users = session.scalars(select(User))
    return {'users': users}


"""
Criar um GET para users por id
"""


# PUT ATUALIZAR DADOS
@app.put('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found!.'
        )
    database[user_id - 1] = user_with_id
    return user_with_id


# DELETE
@app.delete(
    '/users/{user_id}', status_code=status.HTTP_200_OK,
    response_model=UserPublic)

def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found!'
        ) 
    return database.pop(user_id - 1)





if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
