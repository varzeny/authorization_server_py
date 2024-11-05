# signup_token.py

# lib
import jwt

# module
from app.core.config import SETTING

# define
class SignupToken:
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
            print("this Token has expired")
            return None
        
        except jwt.InvalidTokenError:
            print("this Token is Invalid token")
            return None
        
        except Exception as e:
            print("error from verify_token : ", e)
            return None  


    def __init__(self, seq:int=1, email:str=None, code:int=None, name:str=None, pw:str=None):
        self.seq:int = seq
        self.email:str|None = email
        self.code:int|None = code
        self.name:str|None = name
        self.pw:str|None = pw
        
    def create_jwt(self):
        encoded_token = jwt.encode(
            payload={
                "seq":self.seq,
                "email":self.email,
                "code":self.code,
                "name":self.name,
                "pw":self.pw
            },
            key=self.secret_key,
            algorithm=self.alg
        )
        return encoded_token


# script
ENV = SETTING["app"]["core"]["security"]["signup"]
SignupToken.setup(ENV)