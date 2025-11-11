"""
Adapter In-Memory pour le repository de livres.
Utile pour les tests et le développement rapide.
"""
from typing import List, Optional
from domain.book import Book
from domain.ports import IBookRepository


class InMemoryBookRepository(IBookRepository):
    """Implémentation en mémoire du repository de livres."""
    
    def __init__(self):
        self._books: List[Book] = []
        self._next_id = 1
    
    def add(self, book: Book) -> Book:
        """Ajoute un livre en mémoire."""
        book.id = self._next_id
        self._next_id += 1
        self._books.append(book)
        return book
    
    def get_all(self) -> List[Book]:
        """Retourne tous les livres."""
        return self._books.copy()
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Récupère un livre par son ID."""
        for book in self._books:
            if book.id == book_id:
                return book
        return None
    
    def find_by_title(self, search_term: str) -> List[Book]:
        """Trouve des livres par titre."""
        if not search_term:
            return []
        return [book for book in self._books if book.matches_title(search_term)]
    
    def exists(self, title: str, author: str) -> bool:
        """Vérifie si un livre existe déjà."""
        return any(
            book.title.lower() == title.lower() and 
            book.author.lower() == author.lower()
            for book in self._books
        )
    
    def remove_by_id(self, book_id: int) -> bool:
        """Supprime un livre par son ID."""
        for i, book in enumerate(self._books):
            if book.id == book_id:
                self._books.pop(i)
                return True
        return False
    
    def update(self, book: Book) -> Optional[Book]:
        """Met à jour un livre existant."""
        for i, existing_book in enumerate(self._books):
            if existing_book.id == book.id:
                self._books[i] = book
                return book
        return None
    
    def count(self) -> int:
        """Retourne le nombre de livres."""
        return len(self._books)