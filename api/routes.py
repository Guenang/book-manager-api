from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from infrastructure.database import get_db
from repository.book_repository import BookRepository
from service.book_service import BookService
from api.schemas import BookCreate, BookUpdate, BookResponse, StatsResponse
from domain.exceptions import (
    DuplicateBookError, BookNotFoundError, 
    YearError, TitleError, AuthorError
)

router = APIRouter(prefix="/books", tags=["Books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    """Injection de dépendances pour le service."""
    repository = BookRepository(db)
    return BookService(repository)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    """
    Crée un nouveau livre.
    
    - **title**: Titre du livre (au moins 1 caractère)
    - **author**: Auteur du livre (au moins 1 caractère)
    - **year**: Année de publication (entre 1000 et 2025)
    """
    try:
        created_book = service.create_book(book.title, book.author, book.year, book.rating )
        return created_book
    except DuplicateBookError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except (YearError, TitleError, AuthorError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[BookResponse])
def list_books(service: BookService = Depends(get_book_service)):
    """Liste tous les livres de la bibliothèque."""
    return service.list_all_books()


@router.get("/search", response_model=List[BookResponse])
def search_books(
    q: str,
    service: BookService = Depends(get_book_service)
):
    """
    Recherche des livres par titre.
    
    - **q**: Terme de recherche (recherche partielle, insensible à la casse)
    """
    return service.search_books(q)


@router.get("/stats", response_model=StatsResponse)
def get_stats(service: BookService = Depends(get_book_service)):
    """Retourne des statistiques sur la bibliothèque."""
    return service.get_statistics()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    """
    Récupère un livre par son ID.
    
    - **book_id**: ID du livre
    """
    try:
        return service.get_book_by_id(book_id)
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    service: BookService = Depends(get_book_service)
):
    """
    Met à jour un livre existant.
    
    - **book_id**: ID du livre à modifier
    - **title**: Nouveau titre
    - **author**: Nouvel auteur
    - **year**: Nouvelle année
    """
    try:
        # convertir les string vide en None
        title = book.title if book.title and book.title.strip() else None
        author = book.author if book.author and book.author.strip() else None
        year = book.year if book.year else None
        rating = book.rating if book.rating else None
        return service.update_book(book_id, title, author, year, rating)
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (YearError, TitleError, AuthorError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    """
    Supprime un livre par son ID.
    
    - **book_id**: ID du livre à supprimer
    """
    try:
        service.delete_book(book_id)
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
