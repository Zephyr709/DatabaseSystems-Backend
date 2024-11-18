from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = ... #replace with database url with password

engine = create_engine(DATABASE_URL)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()