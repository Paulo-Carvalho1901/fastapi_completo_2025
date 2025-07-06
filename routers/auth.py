from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from schema import Token

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User
from database import get_session

from security import verify_password, create_acess_token


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
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

