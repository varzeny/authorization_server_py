# hash.py

# lib
from bcrypt import checkpw, hashpw, gensalt

# module


# define
def create_hash(input_val:str) -> str:
    result = hashpw(
        password= input_val.encode("utf-8"), 
        salt= gensalt()
    )
    return result.decode("utf-8")


def verify_hash(input_val:str, hashed_val:str ) -> bool:
    return checkpw(
        password=input_val.encode("utf-8"),
        hashed_password=hashed_val.encode("utf-8")
    )


if __name__=="__main__":
    input_val:str|None = None
    hashed_val:str|None = None

    print( create_hash(input_val) )
    print( verify_hash(input_val, hashed_val) )