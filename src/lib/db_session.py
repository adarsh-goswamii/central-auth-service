from src.configs.env import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextvars import ContextVar

config = get_settings()

engine = create_engine(
  "postgresql://{user}:{password}@{host}/{db_name}".format(
    user=config.db_user,
    password=config.db_password,
    host=config.db_host,
    db_name=config.db_name,
  )
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db_session: ContextVar[Session] = ContextVar("db_session", default=None)

def get_db():
    """get db"""
    if not db_session.get():
        db = SessionLocal()
        db_session.set(db)
        return db
    return db_session.get()


def select_all(rows):
    """method to implement the select all fn"""
    db = get_db()
    try:
        rows = rows.all()
    except:
        db.close()
        db: Session = SessionLocal()
        db_session.set(db)
        rows = rows.all()

    return rows

def clear_db_session():
    """clear db session"""
    pass
    # db = get_db()
    # db.close()

def select_first(rows):
    """method to implement the select all fn"""
    db = get_db()
    try:
        rows = rows.first()
    except:
        db.rollback()
        db.close()
        db: Session = SessionLocal()
        db_session.set(db)
        rows = rows.first()
    return rows


def select_count(rows):
    """method to implement the select all fn"""
    db = get_db()
    try:
        rows = rows.count()
    except:
        db.rollback()
        db.close()
        db: Session = SessionLocal()
        db_session.set(db)
        rows = rows.count()
    return rows


def save_new_row(new_row):
    """method to save new rows into db"""
    db = get_db()
    try:
        db.add(new_row)
        db.commit()
        db.refresh(new_row)
        return new_row
    except Exception as e:
        db.rollback()
        db.close()
        raise e


def update_old_row(old_row):
    """method to update the data into old row"""
    db = get_db()
    try:
        db.commit()
        db.refresh(old_row)
        return old_row
    except Exception as e:
        db.rollback()
        db.close()
        raise e

def delete(old_row):
    """method to delete"""
    db = get_db()
    try:
        db.delete(old_row)
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        raise e