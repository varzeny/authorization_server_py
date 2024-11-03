# model.py

# lib
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone, timedelta

# module
from .core.database import Manager as DB


# define
class Account(DB.base):
    __tablename__="account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(45), unique=True, nullable=False)
    pw_hashed = Column(String(60), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    role = relationship("Role", back_populates="account")
    refresh = relationship("Refresh", back_populates="account")


class Role(DB.base):
    __tablename__="role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)

    account = relationship("Account", back_populates="role")


class Refresh(DB.base):
    __tablename__="refresh"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc) + timedelta(days=10))
    created_at = Column(TIMESTAMP, default=func.now())
    revoked = Column(Boolean, default=False)

    account = relationship("Account", back_populates="refresh")