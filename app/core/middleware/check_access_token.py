# middleware

# lib
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request
from fastapi.responses import Response

# module
from app.core.security.token.access_token import AccessToken

# define
class Manager(BaseHTTPMiddleware):
    async def dispatch(self, req:Request, call_next):
        # 전처리
        encoded_access_token = req.cookies.get(AccessToken.key)

        if encoded_access_token:
            access_token = AccessToken.verify_jwt(encoded_access_token)
            req.state.access_token = access_token
        else:
            req.state.access_token = AccessToken()


        # 대기
        resp:Response = await call_next(req)


        # 후처리
        return resp