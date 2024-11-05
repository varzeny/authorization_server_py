# api.py

# lib
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response ,RedirectResponse
from fastapi import HTTPException, Depends
from random import randint


# module
from app.core.database.asyncmy import DB
from app.core.messaging.email import EMAIL
from app.core.security.token.refresh_token import RefreshToken
from app.core.security.token.access_token import AccessToken
from app.core.security.token.signup_token import SignupToken
from app.core.security.hash import create_hash, verify_hash
from app.core.security.dependency import admin_only, user_only, guest_only

from app import crud as CRUD


# define
router = APIRouter()
template = Jinja2Templates(directory="template")


# endpoint
@router.get("/")
async def get_root(req:Request):
    resp = template.TemplateResponse(
        request=req,
        name="root.html",
        context={},
        status_code=200
    )
    return resp


@router.get("/test")
async def get_root(req:Request, at=Depends(user_only)):
    resp = template.TemplateResponse(
        request=req,
        name="test.html",
        context={},
        status_code=200
    )
    return resp


@router.get("/test-admin")
async def get_root(req:Request, at=Depends(admin_only)):
    resp = template.TemplateResponse(
        request=req,
        name="test_admin.html",
        context={},
        status_code=200
    )
    return resp


@router.post("/oauth/token/access")
async def post_root(req:Request, ss=Depends(DB.get_ss)):

    # 클라이언트가 refresh_token 가지고 있는지?
    refresh_token = req.cookies.get(RefreshToken.key)
    if not refresh_token:
        print("클라이언트에 리프레쉬 토큰 없음")
        return Response(status_code=401, content="Refresh token not found")
    
    # 유효한 refresh_token 인지?
    refresh = await CRUD.read_refresh_by_token(refresh_token, ss)
    
    if not RefreshToken.verify_token(refresh):
        await CRUD.delete_refresh_by_id(refresh.get("id"), ss)
        return Response(status_code=401, content="유효하지 않은 refresh_token")

    account = await CRUD.read_account_by_refresh(refresh_token, ss)
    if not account:
        print("해당 리프레쉬토큰을 가진 계정이 없음")
        return Response(status_code=401, content="Doesn't exist account")
    
    # access_token 재발급
    new_access_token = AccessToken(
        sub=account.get("id"),
        roles=account.get("role_id"),
        name=account.get("name")
    )

    resp = Response(status_code=200)
    resp.set_cookie(
        key=AccessToken.key,
        value=new_access_token.create_jwt(),
        max_age=AccessToken.exp_min*60,
        httponly=True,
        secure=True,
        domain=".varzeny.com",
        path="/"
    )
    
    return resp




# login & signup ##################################################

@router.get("/login/page")
async def get_login_page(req:Request, at=Depends(guest_only)):
    referer = req.headers.get("referer")
    try:
        resp = template.TemplateResponse(
            request=req,
            name="login.html",
            context={
                "referer":referer
            },
            status_code=200
        )

    except Exception as e:
        print("ERROR from get_login_page : ", e)
        resp = Response(status_code=400)

    finally:
        return resp


@router.post("/login")
async def post_login(req:Request, at=Depends(guest_only), ss=Depends(DB.get_ss)):
    try:
        # DB 확인
        reqData = await req.form()
        account = await CRUD.read_account_by_email( reqData.get("email"), ss )

        if not account:
            raise Exception("doesn't exist account")

        if not verify_hash(reqData.get("pw"), account.get("pw_hashed")):
            raise Exception("wrong PW")

        # refresh_token
        refresh_token = RefreshToken(account.get("id"))
        if not await CRUD.create_refresh(account.get("id"), refresh_token.token, ss):
            raise Exception("create refresh fail")

        # access_token
        access_token = AccessToken(
            sub=account.get("id"),
            roles=account.get("role_id"),
            name=account.get("name")
        )

        # set cookies
        resp = Response(status_code=200)
        resp.set_cookie(
            key=RefreshToken.key,
            value=refresh_token.token,
            max_age=RefreshToken.exp_min*60,
            httponly=True,
            secure=True,
            domain=".varzeny.com",
            path="/"
        )
        resp.set_cookie(
            key=AccessToken.key,
            value=access_token.create_jwt(),
            max_age=AccessToken.exp_min*60,
            httponly=True,
            secure=True,
            domain=".varzeny.com",
            path="/"
        )

    except Exception as e:
        print("ERROR from post_login_page : ", e)
        resp = Response(status_code=401, content=str(e))

    finally:
        return resp
    

@router.get("/logout")
async def get_logout(req:Request, at=Depends(user_only), ss=Depends(DB.get_ss)):
    try:
        # 로그아웃 위치
        referer=req.headers.get("referer")
        print("logout 요청 받음")

        # delete refresh 
        refresh_token = req.cookies.get(RefreshToken.key)
        await CRUD.delete_refresh_by_token(refresh_token, ss)

        if referer:
            resp = RedirectResponse(referer)
        else:
            resp = Response(status_code=200)
            
        # delete token
        resp.delete_cookie(
            key=AccessToken.key,
            domain=".varzeny.com",
            path="/"
        )
        resp.delete_cookie(
            key=RefreshToken.key,
            domain=".varzeny.com",
            path="/"
        )


    except Exception as e:
        print("ERROR from get_logout : ", e)
        resp = Response(status_code=500)

    finally:
        return resp






@router.get("/signup/page")
async def get_signup_page(req:Request, at=Depends(guest_only)):
    try:
        resp = template.TemplateResponse(
            request=req,
            name="signup.html",
            context={},
            status_code=200
        )

        signup_token = SignupToken()

        resp.set_cookie(
            key=SignupToken.key,
            value=signup_token.create_jwt(),
            max_age=SignupToken.exp_min*60,
            httponly=True,
            secure=True,
            domain=".varzeny.com",
            path="/"
        )
        return resp
    
    except Exception as e:
        print("ERROR from get_signup_page : ", e)
        return Response(status_code=400)
    

@router.post("/signup/seq")
async def post_signup_seq(req:Request, at=Depends(guest_only), ss=Depends(DB.get_ss)):
    try:
        encoded_signup_token = req.cookies.get(SignupToken.key)
        signup_token = SignupToken.verify_jwt(encoded_signup_token)

        reqData = await req.form()

        if not signup_token.seq == int( reqData.get("seq") ):
            raise Exception("토큰과 요청의 seq 가 다름")
        
        seq = signup_token.seq

        # email
        if seq == 1:
            email_addr = reqData.get("email")
            respData = await CRUD.check_email(email_addr, ss)
            if respData:
                raise Exception("이미 등록된 이메일")

            code = str( randint(10000, 99999) )

            if not await EMAIL.send_email(
                receiver_addr=email_addr,
                subject="Your verify code has arrived.",
                data=code
            ):
                raise Exception("이메일 전송 오류")
            
            signup_token.email = email_addr
            signup_token.code = code
            signup_token.seq = 2

        
        # code
        elif seq == 2:
            if not signup_token.code == reqData.get("code"):
                raise Exception("토큰과 요청의 code 가 다름")
            
            signup_token.seq = 3
            

        # pw
        elif seq == 3:
            await CRUD.create_account(signup_token.email, reqData.get("name"), create_hash(reqData.get("pw")), ss)
            signup_token.seq = 4
        

        else:
            raise Exception("등록되지 않은 seq")
    
        resp = Response( status_code=200, content="seq"+str(signup_token.seq) )
        resp.set_cookie(
            key=SignupToken.key,
            value=signup_token.create_jwt(),
            max_age=SignupToken.exp_min*60,
            httponly=True,
            secure=True,
            domain=".varzeny.com",
            path="/"
        )

    except Exception as e:
        print("ERROR from post_seq : ", e)
        resp = Response(status_code=400)

    finally:
        return resp


