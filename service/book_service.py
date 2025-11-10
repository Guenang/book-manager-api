from typing import List, Optional
from domain.book import Book
from domain.exceptions import DuplicateBookError, BookNotFoundError
from repository.book_repository import BookRepository


class BookService:
    """Coordonne les opérations sur les livres."""
    
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def create_book(self, title: str, author: str, year: int,  rating: int = None) -> Book:
        """Crée et enregistre un nouveau livre."""
        # Vérification des doublons
        if self.repository.exists(title, author):
            raise DuplicateBookError(title, author)
        
        book = Book(title, author, year, rating=rating)
        return self.repository.add(book)

    def get_book_by_id(self, book_id: int) -> Book:
        """Récupère un livre par son ID."""
        book = self.repository.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(f"ID {book_id}")
        return book

    def list_all_books(self) -> List[Book]:
        """Liste tous les livres."""
        return self.repository.get_all()
    
    def search_books(self, search_term: str) -> List[Book]:
        """Recherche des livres par titre."""
        return self.repository.find_by_title(search_term)
    
    def delete_book(self, book_id: int) -> bool:
        """Supprime un livre par son ID."""
        success = self.repository.remove_by_id(book_id)
        if not success:
            raise BookNotFoundError(f"ID {book_id}")
        return True
    
    def update_book(self, book_id: int = None, title: str = None, author: str = None, year: int = None, rating: int = None) -> Book:
        """Met à jour un livre existant."""
        # Vérifier que le livre existe
        existing_book = self.get_book_by_id(book_id)
        final_title = title if title is not None else existing_book.title
        final_author = author if author is not None else existing_book.author
        final_year = year if year is not None else existing_book.year
        final_rating = rating if rating is not None else existing_book.rating
        
        # Créer le livre mis à jour (avec validation)
        updated_book = Book(final_title, final_author, final_year, rating=final_rating, book_id=book_id)
        
        # Sauvegarder
        result = self.repository.update(updated_book)
        if not result:
            raise BookNotFoundError(f"ID {book_id}")
        return result
    
    def get_statistics(self) -> dict:
        """Retourne des statistiques sur la collection."""
        books = self.repository.get_all()
        if not books:
            return {"total": 0, "oldest": None, "newest": None}
        
        years = [book.year for book in books]
        return {
            "total": len(books),
            "oldest": min(years),
            "newest": max(years)
        }
