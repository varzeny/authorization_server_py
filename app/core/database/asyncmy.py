# core/database.py

# lib
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

# module
from app.core.config import SETTING

# define
class Manager:
    instance:dict = {}

    @classmethod
    def __getitem__(cls, name:str):
        return cls.instance.get(name)
    

    def __init__(self, name:str, id:str, pw:str, ip:str, port:str):
        self.name = name
        self.id = id
        self.pw = pw
        self.ip = ip
        self.port = port
        self.url = f"mysql+asyncmy://{id}:{pw}@{ip}:{port}/{name}"
        self.engine = create_async_engine( self.url )
        self.session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        Manager.instance[name] = self

    async def get_ss(self):
        ss:AsyncSession = self.session()
        try:
            yield ss
        except Exception as e:
            print("ERROR from get_ss : ", e)
            await ss.rollback()
        finally:
            await ss.close()


# script
ENV = SETTING["app"]["core"]["database"]["session"]
DB = Manager(
    name=ENV.get("name"),
    id=ENV.get("id"),
    pw=ENV.get("pw"),
    ip=ENV.get("ip"),
    port=ENV.get("port")
) 