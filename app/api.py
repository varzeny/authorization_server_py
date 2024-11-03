# api.py

# lib
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response ,RedirectResponse
from fastapi import HTTPException, Depends
from random import randint


# module
from app.database import Manager as DB
from app.security import Manager as SECURITY
from app import crud as CRUD
from app.util import email as EMAIL
from app.util import hash as HASH


# define
router = APIRouter()
template = Jinja2Templates(directory="app/template")


# dependency
async def guest_only(req:Request):
    t = req.cookies.get(SECURITY.access_name)
    if t and SECURITY.verify_access_token(t):
        print("게스트 아님")
        raise HTTPException(status_code=401, detail="you are not guest")
    else:
        print("게스트 맞음")
        return


async def user_only(req:Request):
    access_et = req.cookies.get(SECURITY.access_name)
    if access_et and SECURITY.verify_access_token(access_et):
        print("유저임")
        return
    else:
        print("access_token 없음")
        raise HTTPException(status_code=401, detail="access_token doesn't exist")


async def admin_only(req:Request):
    access_et = req.cookies.get(SECURITY.access_name)
    access_dt = SECURITY.verify_access_token(access_et)
    if access_et and access_dt:
        print(access_dt)
        if access_dt.get("role_id")==1:
            print("관리자임")
            return
        else:
            print("엑세스 토큰은 있는데, 관리자가 아님")
            raise HTTPException(status_code=403, detail="you are not admin")
    else:
        print("access_token 없음")
        raise HTTPException(status_code=401, detail="access_token doesn't exist")


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
async def get_root(req:Request, t=Depends(user_only)):

    resp = template.TemplateResponse(
        request=req,
        name="test.html",
        context={},
        status_code=200
    )
    return resp


@router.get("/test-admin")
async def get_root(req:Request, t=Depends(admin_only)):

    resp = template.TemplateResponse(
        request=req,
        name="test_admin.html",
        context={},
        status_code=200
    )
    return resp


@router.post("/oauth/token/access")
async def post_root(req:Request, ss=Depends(DB.getss)):

    # 기존거 있으면 제거

    # refresh_token 있는지?
    refresh_token = req.cookies.get(SECURITY.refresh_name)
    if not refresh_token:
        print("클라이언트에 리프레쉬 토큰 없음")
        return Response(status_code=401, content="Refresh token not found")
    
    # refresh_token 검증
    account = await CRUD.read_account_by_refresh(refresh_token, ss)
    if not account:
        print("DB에 리프레쉬 토큰 없음")
        return Response(status_code=401, content="Doesn't exist refresh token")
    
    # refresh_token 기간확인
    
    # access_token 재발급
    new_access_token = SECURITY.create_access_token( {
        "id":account.get("id"),
        "role_id":account.get("role_id"),
        "name":account.get("name")
    } )
    
    resp = Response(status_code=200)
    resp.set_cookie(
        key=SECURITY.access_name,
        value=new_access_token,
        max_age=SECURITY.access_expmin*60,
        httponly=True,
        secure=True,
        domain=".varzeny.com",
        path="/"
    )
    
    return resp






# login & signup ##################################################

@router.get("/login/page")
async def get_login_page(req:Request, t=Depends(guest_only)):
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
async def post_login(req:Request, ss=Depends(DB.getss)):
    try:
        # DB 확인
        reqData = await req.form()
        account = await CRUD.read_account_by_email( reqData.get("email"), ss )

        if not account:
            raise Exception("doesn't exist account")

        if not HASH.verify_hash(reqData.get("pw"), account.get("pw_hashed")):
            raise Exception("wrong PW")

        # refresh_token
        refresh_token = SECURITY.create_refresh_token()
        if not await CRUD.create_refresh(
            account.get("id"), 
            refresh_token, 
            ss
        ):
            raise Exception("create refresh fail")

        # access_token
        access_token = SECURITY.create_access_token( {
            "id":account.get("id"),
            "role_id":account.get("role_id"),
            "name":account.get("name")
        } )

        # set cookies
        resp = Response(status_code=200)
        resp.set_cookie(
            key=SECURITY.refresh_name,
            value=refresh_token,
            max_age=SECURITY.refresh_expmin*60,
            httponly=True,
            secure=True,
            domain=".varzeny.com",
            path="/"
        )
        resp.set_cookie(
            key=SECURITY.access_name,
            value=access_token,
            max_age=SECURITY.access_expmin*60,
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
async def get_logout(req:Request, ss=Depends(DB.getss)):
    try:
        # 로그아웃 위치
        referer=req.headers.get("referer")

        print("logout 요청 받음")
        # delete refresh 
        refresh_token = req.cookies.get(SECURITY.refresh_name)
        await CRUD.delete_refresh_by_token(refresh_token, ss)

        if referer:
            resp = RedirectResponse(referer)
        else:
            resp = Response(status_code=200)
            
        # delete token
        resp.delete_cookie(
            key=SECURITY.access_name,
            domain=".varzeny.com",
            path="/"
        )
        resp.delete_cookie(
            key=SECURITY.refresh_name,
            domain=".varzeny.com",
            path="/"
        )


    except Exception as e:
        print("ERROR from get_logout : ", e)
        resp = Response(status_code=500)

    finally:
        return resp






@router.get("/signup/page")
async def get_signup_page(req:Request):
    try:
        resp = template.TemplateResponse(
            request=req,
            name="signup.html",
            context={},
            status_code=200
        )

        resp.set_cookie(
            key=SECURITY.signup_name,
            value=SECURITY.create_signup_token( {"seq":"1"} ),
            max_age=SECURITY.signup_expmin*60,
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
async def post_signup_seq(req:Request, ss=Depends(DB.getss)):
    try:
        encoded_token = req.cookies.get(SECURITY.signup_name)
        decoded_token = SECURITY.verify_signup_token(encoded_token)
        reqData = await req.form()


        if not decoded_token.get("seq") == reqData.get("seq"):
            print(decoded_token.get("seq"),"???",reqData.get("seq"))
            raise Exception("토큰과 요청의 seq 가 다름")
        
        seq = decoded_token.get("seq")

        # email
        if seq == "1":
            email_addr = reqData.get("email")
            respData = await CRUD.check_email(email_addr, ss)
            if respData:
                raise Exception("이미 등록된 이메일")

            code = str( randint(10000, 99999) )

            if not await EMAIL.send_email(
                smtp_host=SECURITY.smtp_host,
                smtp_port=SECURITY.smtp_port,
                sender_addr=SECURITY.sender_id,
                sender_pw=SECURITY.sender_pw,
                receiver_addr=email_addr,
                subject="Your verify code has arrived.",
                bodyData=code
            ):
                raise Exception("이메일 전송 오류")

            decoded_token["email"] = email_addr
            decoded_token["code"] = code
            decoded_token["seq"] = "2"

        
        # code
        elif seq == "2":
            if not decoded_token.get("code") == reqData.get("code"):
                raise Exception("토큰과 요청의 code 가 다름")
            
            decoded_token["seq"] = "3"
            

        # pw
        elif seq == "3":
            await CRUD.create_account(decoded_token["email"], reqData.get("name"), reqData.get("pw"), ss)
            decoded_token["seq"] = "4"
        

        else:
            raise Exception("등록되지 않은 seq")
    
        encoded_token = SECURITY.create_signup_token( decoded_token )
        resp = Response(status_code=200, content="seq"+decoded_token.get("seq"))
        resp.set_cookie(
            key=SECURITY.signup_name,
            value=encoded_token,
            max_age=SECURITY.signup_expmin*60,
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


