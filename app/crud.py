# crud.py

# lib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# module

# define
async def read_account_by_refresh(refresh_token:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "SELECT account.* FROM account JOIN refresh ON account.id = refresh.account_id WHERE refresh.token = :token"
        ),
        params={"token":refresh_token}
    )
    respData = resp.mappings().fetchone()
    return respData


async def create_refresh(account_id:int, refresh_token:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "INSERT INTO refresh(account_id, token) VALUES(:account_id, :token)"
        ),
        params={
            "account_id":account_id,
            "token":refresh_token
        }
    )
    await ss.commit()
    return True


async def read_refresh_by_token(refresh_token:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "SELECT * FROM refresh WHERE token=:token"
        ),
        params={"token":refresh_token}
    )
    return resp.mappings().fetchone()


async def delete_refresh_by_id(id:int, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "DELETE FROM refresh WHERE id=:id"
        ),
        params={"id":id}
    )
    await ss.commit()
    return resp


async def delete_refresh_by_token(refresh_token:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "DELETE FROM refresh WHERE token=:token"
        ),
        params={
            "token":refresh_token
        }
    )
    await ss.commit()
    return




async def check_email(email:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "SELECT id FROM account WHERE email=:email"
        ),
        params={"email":email}
    )
    respData = resp.fetchall()
    return respData


async def create_account(email:str, name:str, pw_hashed:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "INSERT INTO account(role_id, email, pw_hashed, name) VALUES(:role_id, :email, :pw_hashed, :name)"
        ),
        params={
            "role_id":2,
            "email":email,
            "pw_hashed":pw_hashed,
            "name":name
        }
    )
    await ss.commit()
    return


async def read_account_by_email(email:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text(
            "SELECT * FROM account WHERE email=:email"
        ),
        params={
            "email":email
        }
    )
    respData = resp.mappings().fetchone()
    print(respData)
    return respData

