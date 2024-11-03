# core/database.py

# lib
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

# module


# define


class Manager:
    url:str|None
    engine:AsyncEngine|None
    session:AsyncSession = None

    @classmethod
    def setup(cls, env:dict):
        cls.url = f"mysql+asyncmy://{env.get('id')}:{env.get('pw')}@{env.get('ip')}:{env.get('port')}/{env.get('name')}"
        cls.engine = create_async_engine( cls.url )
        cls.session = async_sessionmaker(
            bind=cls.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @classmethod
    async def getss(cls):
        try:
            ss:AsyncSession = cls.session()
            yield ss
        except Exception as e:
            print("ERROR from getss : ", e)
            await ss.rollback()
        finally:
            await ss.close()