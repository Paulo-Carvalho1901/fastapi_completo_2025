from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schema import Message, UserList, UserPublic, UserSchema, Token
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

from models import User
from database import get_session

from security import get_password_hash, verify_password, create_acess_token, get_current_user


app = FastAPI(title='Curso de FastAPI')


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
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


# GET TODOS OS USERS
@app.get('/users/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    ):

    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


"""
Criar um GET para users por id
"""


# PUT ATUALIZAR DADOS
@app.put('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(
    user_id: int, 
    user: UserSchema, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
    
    ):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions'
        )
    
    try:
        current_user.email = user.email
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user
    
    except IntegrityError:
        raise HTTPException(
            detail='Username or Email already exists',
            status_code=status.HTTP_409_CONFLICT,
        )

# DELETE
@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@app.post('/token', response_model=Token)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect email or password'
        )
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect email or password'
        )
    
    access_token = create_acess_token(
        {'sub': user.email}
    )
    return {'access_token': access_token, 'token_type': 'Bearer'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
