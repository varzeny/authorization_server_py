# main.py

# lib
from fastapi import FastAPI, staticfiles
from fastapi.middleware.cors import CORSMiddleware

# module
from app.api import router
from app.core.middleware.check_access_token import Manager as CheckAccessToken

# define
"""
uvicorn main:app --host 0.0.0.0 --port 9000 --reload

"""


# app
app = FastAPI()

# mount
app.mount(
    path="/static",
    app=staticfiles.StaticFiles(directory="static"),
    name="static"
)

# middleware
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["https://test.varzeny.com"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware( CheckAccessToken )

# api
app.include_router( router )





