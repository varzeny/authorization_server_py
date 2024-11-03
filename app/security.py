# core/security

# lib
from app.util import jwt as JWT
from secrets import token_hex

# module


# define
class Manager:
    # auth_server
    auth_url:str|None

    # refresh_token
    refresh_name:str|None
    refresh_secretkey:str|None
    refresh_algorithm:str|None
    refresh_expmin:float|None

    # access_token
    access_name:str|None
    access_secretkey:str|None
    access_algorithm:str|None
    access_expmin:float|None

    # signup_token
    signup_name:str|None
    signup_secretkey:str|None
    signup_algorithm:str|None
    signup_expmin:float|None

    # email
    smtp_host:str|None
    smtp_port:int|None
    sender_id:str|None
    sender_pw:str|None



    @classmethod
    def setup(cls, env:dict):
        # auth_server
        cls.auth_url=env["auth"]["url"]

        # refresh_token
        cls.refresh_name=env["refresh"]["name"]
        cls.refresh_secretkey=env["refresh"]["secretkey"]
        cls.refresh_algorithm=env["refresh"]["algorithm"]
        cls.refresh_expmin=env["refresh"]["expmin"]

        # access_token
        cls.access_name=env["access"]["name"]
        cls.access_secretkey=env["access"]["secretkey"]
        cls.access_algorithm=env["access"]["algorithm"]
        cls.access_expmin=env["access"]["expmin"]

        # signup_token
        cls.signup_name=env["signup"]["name"]
        cls.signup_secretkey=env["signup"]["secretkey"]
        cls.signup_algorithm=env["signup"]["algorithm"]
        cls.signup_expmin=env["signup"]["expmin"]

        # email
        cls.smtp_host=env["email"]["smtphost"]
        cls.smtp_port=env["email"]["smtpport"]
        cls.sender_id=env["email"]["senderid"]
        cls.sender_pw=env["email"]["senderpw"]


    @classmethod
    def create_refresh_token(cls):
        return token_hex(64)


    @classmethod
    def create_access_token(cls, decoded_token:dict):
        encoded_token = JWT.create_jwt(
            payload=decoded_token,
            secret_key=cls.access_secretkey,
            algorithm=cls.access_algorithm,
            exp_min=cls.access_expmin
        )
        return encoded_token

    @classmethod
    def verify_access_token(cls, encoded_token:str):
        decoded_token = JWT.verify_jwt(
            encoded_token=encoded_token,
            secret_key=cls.access_secretkey,
            algorithm=cls.access_algorithm
        )
        return decoded_token
    






    

    @classmethod
    def create_signup_token(cls, decoded_token:dict):
        encoded_token = JWT.create_jwt(
            payload=decoded_token,
            secret_key=cls.signup_secretkey,
            algorithm=cls.signup_algorithm,
            exp_min=cls.signup_expmin
        )
        return encoded_token
    
    @classmethod
    def verify_signup_token(cls, encoded_token):
        decoded_token = JWT.verify_jwt(
            encoded_token=encoded_token,
            secret_key=cls.signup_secretkey,
            algorithm=cls.signup_algorithm,
        )
        return decoded_token