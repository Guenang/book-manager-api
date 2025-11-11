import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Utiliser PostgreSQL en production, SQLite en local
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./books.db"
)

# Fix pour Render qui utilise postgres:// au lieu de postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuration selon l'environnement
if DATABASE_URL.startswith("postgresql://"):
    # PostgreSQL en production
    engine = create_engine(DATABASE_URL)
else:
    # SQLite en local
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Générateur de session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crée toutes les tables dans la base de données."""
    Base.metadata.create_all(bind=engine)