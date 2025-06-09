from fastapi import FastAPI, status, HTTPException

from schema import Message, UserDB, UserList, UserPublic, UserSchema



app = FastAPI(title='Curso de FastAPI')
database = []


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def get_root():
    return {"message": "Olá mundo!"}


# POST CREATE
@app.post('/users/', status_code=status.HTTP_201_CREATED,response_model=UserPublic) # Saída dos dados
def create_user(user: UserSchema): # function anotation (anotação de função) ou 'anotação de tipo' entrada dos dados
    user_with_id = UserDB(
        **user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


# GET TODOS OS USERS
@app.get('/users/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users():
    return {'users': database}


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
