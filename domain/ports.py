"""
Ports (Interfaces) pour l'architecture hexagonale.
Ces interfaces définissent les contrats que les adapters doivent respecter.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.book import Book


class IBookRepository(ABC):
    """
    Interface pour le repository de livres.
    Le Domain dépend de cette interface, pas d'une implémentation concrète.
    """
    
    @abstractmethod
    def add(self, book: Book) -> Book:
        """Ajoute un livre et retourne le livre avec son ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        """Retourne tous les livres."""
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Récupère un livre par son ID."""
        pass
    
    @abstractmethod
    def find_by_title(self, search_term: str) -> List[Book]:
        """Trouve des livres par titre (recherche partielle)."""
        pass
    
    @abstractmethod
    def exists(self, title: str, author: str) -> bool:
        """Vérifie si un livre existe déjà."""
        pass
    
    @abstractmethod
    def remove_by_id(self, book_id: int) -> bool:
        """Supprime un livre par son ID."""
        pass
    
    @abstractmethod
    def update(self, book: Book) -> Optional[Book]:
        """Met à jour un livre existant."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Retourne le nombre de livres."""
        pass