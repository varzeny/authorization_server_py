# main.py

# lib
from os import getenv
from dotenv import load_dotenv
from fastapi import FastAPI, staticfiles

# module
from app.database import Manager as DB
from app.security import Manager as SECURITY
from app import api as API

# define



async def startup():
    print("-"*40, app.state.env.get("project")["name"], "-"*40)

    # database
    DB.setup( app.state.env["app"]["database"] )

    # security
    SECURITY.setup( app.state.env["app"]["security"] )

    # api
    app.include_router( API.router )


async def shutdown():
    print("-"*40, "end", "-"*40)



app = FastAPI(
    on_startup=[startup],
    on_shutdown=[shutdown]
)

# env
load_dotenv()
app.state.env = {
    "project":{
        "name":getenv("PROJECT_NAME"),
    },
    "app":{
        "database":{
            "name":getenv("APP_DATABASE_NAME"),
            "id":getenv("APP_DATABASE_ID"),
            "pw":getenv("APP_DATABASE_PW"),
            "ip":getenv("APP_DATABASE_IP"),
            "port":int(getenv("APP_DATABASE_PORT")),
        },
        "security":{
            "auth":{
                "url":getenv("APP_SECURITY_AUTH_URL"),
            },
            "refresh":{
                "name":getenv("APP_SECURITY_REFRESH_NAME"),
                "secretkey":getenv("APP_SECURITY_REFRESH_SECRETKEY"),
                "algorithm":getenv("APP_SECURITY_REFRESH_ALGORITHM"),
                "expmin":int(getenv("APP_SECURITY_REFRESH_EXPMIN")),
            },
            "access":{
                "name":getenv("APP_SECURITY_ACCESS_NAME"),
                "secretkey":getenv("APP_SECURITY_ACCESS_SECRETKEY"),
                "algorithm":getenv("APP_SECURITY_ACCESS_ALGORITHM"),
                "expmin":int(getenv("APP_SECURITY_ACCESS_EXPMIN")),
            },
            "signup":{
                "name":getenv("APP_SECURITY_SIGNUP_NAME"),
                "secretkey":getenv("APP_SECURITY_SIGNUP_SECRETKEY"),
                "algorithm":getenv("APP_SECURITY_SIGNUP_ALGORITHM"),
                "expmin":int(getenv("APP_SECURITY_SIGNUP_EXPMIN")),
            },
            "email":{
                "smtphost":getenv("APP_SECURITY_EMAIL_SMTPHOST"),
                "smtpport":getenv("APP_SECURITY_EMAIL_SMTPPORT"),
                "senderid":getenv("APP_SECURITY_EMAIL_SENDERID"),
                "senderpw":getenv("APP_SECURITY_EMAIL_SENDERPW"),
            }
        },
    }
}
# mount
app.mount(
    path="/static",
    app=staticfiles.StaticFiles(directory="app/static"),
    name="static"
)

# middleware









"""
uvicorn main:app --host 0.0.0.0 --port 9000 --reload

"""