from fastapi.routing import APIRouter
from fastapi import Depends,HTTPException,BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fast_zero.models import User
from fast_zero.schemas import RefreshToken
from fast_zero.security import verify_password,create_access_token,create_refresh_token,decode_refresh_token
from http import HTTPStatus
from typing import Annotated
from tortoise.exceptions import DoesNotExist

router = APIRouter(prefix='/auth',tags=['auth'])

T_OAuth = Annotated[OAuth2PasswordRequestForm,Depends()]

@router.post('/token',status_code=HTTPStatus.OK)
async def get_token(form_data: T_OAuth):
    try:
        db_user = await User.get(username=form_data.username)
    except DoesNotExist:       
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Nome de usuário não existe"
        )  
    if verify_password(form_data.password,db_user.password):
        acess_token = create_access_token(data={"sub":form_data.username})
        refresh_token = create_refresh_token(data={"sub":form_data.username})
        return {'access_token':acess_token,'refresh_token':refresh_token,'token_type':'bearer'}
    else:
        raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid password"
            )
    
@router.post("/refresh")
async def refresh_access_token(refresh_token: RefreshToken):
    username = decode_refresh_token(refresh_token.refresh_token)

    access_token = create_access_token(
        data={"sub": username}
    )

    new_refresh_token = create_refresh_token(
        data={"sub": username}
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,  
        "token_type": "bearer"
    }
