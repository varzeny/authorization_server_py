# security/dependency

# lib
from fastapi.requests import Request
from fastapi import HTTPException

# module
from .token.access_token import AccessToken


# define
async def guest_only(req:Request):
    access_token:AccessToken = req.state.access_token
    if access_token.roles == 3:
        return
    else:
        raise HTTPException(status_code=401 , detail="you are not guest")


async def user_only(req:Request):
    access_token:AccessToken = req.state.access_token
    if access_token.roles == 2 or access_token.roles == 1:
        return
    else:
        raise HTTPException(status_code=401 , detail="you are not user")


async def admin_only(req:Request):
    access_token:AccessToken = req.state.access_token
    if access_token.roles == 1:
        return
    else:
        raise HTTPException(status_code=401 , detail="you are not admin")