from datetime import datetime

from sqlalchemy import BIGINT, Column, DateTime, VARCHAR, ARRAY, Enum
from sqlalchemy.ext.declarative import declarative_base

from src.configs.enums import ApplicationStatus
from src.configs.constants import DBTables, DBConfig

Base = declarative_base()

class SessionModel(Base):
    __tablename__  = DBTables.SESSIONS
    __table_args__ = DBConfig.BASE_ARGS

    id  = Column(BIGINT, primary_key=True)
    user_id     = Column(BIGINT, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    expires_at  = Column(DateTime, nullable=False)
    user_agent  = Column(VARCHAR(512))
    ip          = Column(VARCHAR(100))

class UserModel(Base):
    __tablename__ = DBTables.USERS
    __table_args__ = DBConfig.BASE_ARGS

    id              = Column(BIGINT, primary_key=True, autoincrement=True)
    email           = Column(VARCHAR(256), nullable=False, unique=True)
    password_hash   = Column(VARCHAR(512), nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)

class ApplicationModel(Base):
    __tablename__ = DBTables.APPLICATIONS
    __table_args__ = DBConfig.BASE_ARGS

    id                  = Column(BIGINT, primary_key=True, autoincrement=True)
    name                = Column(VARCHAR(512), nullable=False)
    application_id      = Column(VARCHAR(512), nullable=False)
    application_secret  = Column(VARCHAR(512), nullable=False)
    redirect_uris       = Column(ARRAY(VARCHAR), default=[])
    status              = Column(Enum(ApplicationStatus), default=ApplicationStatus.ACTIVE)

class AuthCodeModel(Base):
    __tablename__ = DBTables.AUTH_CODES
    __table_args__ = DBConfig.BASE_ARGS

    code            = Column(VARCHAR(512), primary_key=True)
    user_id         = Column(BIGINT, nullable=False)
    application_id  = Column(VARCHAR(512), nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)
    expires_at      = Column(DateTime, nullable=False)