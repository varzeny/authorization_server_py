# refresh_token.py

# lib
from secrets import token_hex
from datetime import datetime, timezone, timedelta

# module
from app.core.config import SETTING

# define

class RefreshToken:
    """
	id	bigint AI PK
	account_id	int
	token	varchar(255)
	created_at	timestamp

    """
    key:str|None
    exp_min:int|None

    @classmethod
    def setup(cls, env:dict):
        cls.key = env["key"]
        cls.exp_min = env["expmin"]

    @classmethod
    def verify_token(cls, refresh):
        # 기간 만료 확인
        created_at = refresh.get("created_at")
        created_at = created_at.replace(tzinfo=timezone.utc)
        # print("@@@@@@@@@ create_at: ", type(created_at), created_at)
        now = datetime.now(timezone.utc)
        # print("@@@@@@@@ now : ", type(now), now)
        expire = created_at + timedelta(minutes=cls.exp_min)
        if now < expire:
            print("유효한 refresh_token")
            return True
        else:
            print("만료된 refresh_token")
            return False


    def __init__(self, account_id:int):
        self.account_id = account_id
        self.token = token_hex(64)


# script
ENV = SETTING["app"]["core"]["security"]["refresh"]
RefreshToken.setup(ENV)