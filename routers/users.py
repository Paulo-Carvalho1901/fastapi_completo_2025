from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, status, HTTPException

from schema import Message, UserList, UserPublic, UserSchema
from models import User
from database import get_session
from security import get_password_hash, get_current_user
from http import HTTPStatus


router = APIRouter(prefix='/users', tags=['users'])


# POST CREATE
@router.post('/', status_code=status.HTTP_201_CREATED,response_model=UserPublic)
def create_user(user: UserSchema, session = Depends(get_session)):
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
@router.get('/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    ):

    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}



# Criar um GET para users por id
@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


# PUT ATUALIZAR DADOS
@router.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
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
@router.delete('/{user_id}', response_model=Message)
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
