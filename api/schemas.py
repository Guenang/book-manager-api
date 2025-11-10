from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class BookCreate(BaseModel):
    """Schéma pour créer un livre."""
    title: str = Field(..., min_length=1, description="Titre du livre")
    author: str = Field(..., min_length=1, description="Auteur du livre")
    year: int = Field(..., ge=1000, le=2025, description="Année de publication")
    rating: Optional[int] = Field(None, ge=1, le=5)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "1984",
                "author": "George Orwell",
                "year": 1949,
                "rating": 4
            }
        }
    )


class BookUpdate(BaseModel):
    """Schéma pour mettre à jour un livre."""
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, ge=1000, le=2025)
    rating: Optional[int] = Field(None, ge=1, le=5)


class BookResponse(BaseModel):
    """Schéma de réponse pour un livre."""
    id: int
    title: str
    author: str
    year: int
    rating: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    """Schéma pour les erreurs."""
    detail: str


class StatsResponse(BaseModel):
    """Schéma pour les statistiques."""
    total: int
    oldest: Optional[int] = None
    newest: Optional[int] = None
