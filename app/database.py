from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://diplom_tv4n_user:UKcJ8Tk9yNaw0XV4Vng4Be2rfuHk9xWW@dpg-d0g3e83uibrs73f7h7ig-a/diplom_tv4n"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")