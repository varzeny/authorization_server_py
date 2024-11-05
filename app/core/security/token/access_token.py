# access_token.py

# lib
import jwt
from datetime import datetime, timezone, timedelta

# module
from app.core.config import SETTING

# define
class AccessToken:
    key:str|None
    secret_key:str|None
    alg:str|None
    exp_min:int|None

    @classmethod
    def setup(cls, env:dict):
        cls.key = env["key"]
        cls.secret_key = env["secretkey"]
        cls.alg = env["algorithm"]
        cls.exp_min = env["expmin"]

    @classmethod
    def verify_jwt(cls, encoded_access_token:str):
        try:
            decoded_token = jwt.decode(
                jwt=encoded_access_token,
                key=cls.secret_key,
                algorithms=cls.alg,
            )
            return cls(**decoded_token)
        
        except jwt.ExpiredSignatureError:
            print("this Access_Token has expired")
            return None
        
        except jwt.InvalidTokenError:
            print("this Access_Token is Invalid token")
            return None
        
        except Exception as e:
            print("error from verify_token : ", e)
            return None  


    def __init__(self, sub:int=0, roles:int=3, name:str="unknown", exp:datetime=None):
        self.sub = sub
        self.roles = roles
        self.name = name
        self.exp = datetime.now(timezone.utc) + timedelta(minutes=self.exp_min)

    def create_jwt(self):
        encoded_token = jwt.encode(
            payload={
                "sub":self.sub,
                "roles":self.roles,
                "name":self.name,
                "exp":self.exp
            },
            key=self.secret_key,
            algorithm=self.alg
        )
        return encoded_token


# script
ENV = SETTING["app"]["core"]["security"]["access"]
AccessToken.setup(ENV)