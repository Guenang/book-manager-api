"""
Adapter SQLAlchemy pour le repository de livres.
Implémente l'interface IBookRepository.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from domain.book import Book
from domain.ports import IBookRepository
from adapters.models import BookModel


class SQLAlchemyBookRepository(IBookRepository):
    """Implémentation SQLAlchemy du repository de livres."""
    
    def __init__(self, db: Session):
        self.db = db

    def add(self, book: Book) -> Book:
        """Ajoute un livre à la base de données."""
        db_book = BookModel(
            title=book.title,
            author=book.author,
            year=book.year,
            rating=book.rating
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        
        book.id = db_book.id
        return book

    def get_all(self) -> List[Book]:
        """Retourne tous les livres."""
        db_books = self.db.query(BookModel).all()
        return [db_book.to_domain() for db_book in db_books]
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Récupère un livre par son ID."""
        db_book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        return db_book.to_domain() if db_book else None
    
    def find_by_title(self, search_term: str) -> List[Book]:
        """Trouve des livres par titre."""
        if not search_term:
            return []
        
        db_books = self.db.query(BookModel).filter(
            BookModel.title.ilike(f"%{search_term}%")
        ).all()
        return [db_book.to_domain() for db_book in db_books]

    def exists(self, title: str, author: str) -> bool:
        """Vérifie si un livre existe déjà."""
        count = self.db.query(BookModel).filter(
            BookModel.title.ilike(title),
            BookModel.author.ilike(author)
        ).count()
        return count > 0
    
    def remove_by_id(self, book_id: int) -> bool:
        """Supprime un livre par son ID."""
        db_book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        if db_book:
            self.db.delete(db_book)
            self.db.commit()
            return True
        return False
    
    def update(self, book: Book) -> Optional[Book]:
        """Met à jour un livre existant."""
        db_book = self.db.query(BookModel).filter(BookModel.id == book.id).first()
        if db_book:
            db_book.title = book.title
            db_book.author = book.author
            db_book.year = book.year
            db_book.rating = book.rating
            self.db.commit()
            self.db.refresh(db_book)
            return db_book.to_domain()
        return None

    def count(self) -> int:
        """Retourne le nombre de livres."""
        return self.db.query(BookModel).count()