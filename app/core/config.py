# config.py

# lib
from os import getenv
from dotenv import load_dotenv

# module


# define
load_dotenv()
SETTING = {
    "project":{
        "name":getenv("PROJECT_NAME"),
    },
    "app":{
        "core":{
            "database":{
                "session":{
                    "name":getenv("APP_CORE_DATABASE_SESSION_NAME"),
                    "id":getenv("APP_CORE_DATABASE_SESSION_ID"),
                    "pw":getenv("APP_CORE_DATABASE_SESSION_PW"),
                    "ip":getenv("APP_CORE_DATABASE_SESSION_IP"),
                    "port":int(getenv("APP_CORE_DATABASE_SESSION_PORT")),
                },
                "orm":{},
            },
            "messaging":{
                "email":{
                    "name":getenv("APP_CORE_MESSAGING_EMAIL_NAME"),
                    "smtphost":getenv("APP_CORE_MESSAGING_EMAIL_SMTPHOST"),
                    "smtpport":getenv("APP_CORE_MESSAGING_EMAIL_SMTPPORT"),
                    "senderid":getenv("APP_CORE_MESSAGING_EMAIL_SENDERID"),
                    "senderpw":getenv("APP_CORE_MESSAGING_EMAIL_SENDERPW"),
                },
            },
            "security":{
                "auth":{
                    "url":getenv("APP_CORE_SECURITY_AUTH_URL"),
                },
                "refresh":{
                    "key":getenv("APP_CORE_SECURITY_REFRESH_KEY"),
                    "secretkey":getenv("APP_CORE_SECURITY_REFRESH_SECRETKEY"),
                    "algorithm":getenv("APP_CORE_SECURITY_REFRESH_ALGORITHM"),
                    "expmin":int(getenv("APP_CORE_SECURITY_REFRESH_EXPMIN")),
                },
                "access":{
                    "key":getenv("APP_CORE_SECURITY_ACCESS_KEY"),
                    "secretkey":getenv("APP_CORE_SECURITY_ACCESS_SECRETKEY"),
                    "algorithm":getenv("APP_CORE_SECURITY_ACCESS_ALGORITHM"),
                    "expmin":int(getenv("APP_CORE_SECURITY_ACCESS_EXPMIN")),
                },
                "signup":{
                    "key":getenv("APP_CORE_SECURITY_SIGNUP_KEY"),
                    "secretkey":getenv("APP_CORE_SECURITY_SIGNUP_SECRETKEY"),
                    "algorithm":getenv("APP_CORE_SECURITY_SIGNUP_ALGORITHM"),
                    "expmin":int(getenv("APP_CORE_SECURITY_SIGNUP_EXPMIN")),
                },
            },
        },
    }
}