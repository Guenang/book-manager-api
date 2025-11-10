"""
Tests unitaires pour le Domain (Book).
Ces tests vérifient la logique métier isolée.
"""
import pytest
from domain.book import Book
from domain.exceptions import YearError, TitleError, AuthorError


class TestBookCreation:
    """Tests de création d'un Book valide."""
    
    def test_create_valid_book(self):
        """Test : Créer un livre valide."""
        book = Book(
            title="1984",
            author="George Orwell",
            year=1949
        )
        
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.year == 1949
        assert book.rating is None
        assert book.id is None
    
    def test_create_book_with_rating(self):
        """Test : Créer un livre avec un rating."""
        book = Book(
            title="1984",
            author="George Orwell",
            year=1949,
            rating=5
        )
        
        assert book.rating == 5
    
    def test_create_book_with_id(self):
        """Test : Créer un livre avec un ID."""
        book = Book(
            title="1984",
            author="George Orwell",
            year=1949,
            book_id=42
        )
        
        assert book.id == 42
    
    def test_title_with_leading_trailing_spaces(self):
        """Test : Les espaces au début/fin du titre doivent être supprimés."""
        book = Book(title="  1984  ", author="Orwell", year=1949)
        assert book.title == "1984"

    def test_valid_rating_boundaries(self):
        """Test : Les ratings 1 et 5 doivent être acceptés."""
        book1 = Book(title="Test", author="Test", year=2000, rating=1)
        book2 = Book(title="Test", author="Test", year=2000, rating=5)
        
        assert book1.rating == 1
        assert book2.rating == 5


class TestBookValidation:
    """Tests de validation des données."""
    
    def test_empty_title_raises_error(self):
        """Test : Un titre vide doit lever TitleError."""
        with pytest.raises(TitleError):
            Book(title="", author="Orwell", year=1949)
    
    def test_whitespace_title_raises_error(self):
        """Test : Un titre avec seulement des espaces doit lever TitleError."""
        with pytest.raises(TitleError):
            Book(title="   ", author="Orwell", year=1949)
    
    def test_empty_author_raises_error(self):
        """Test : Un auteur vide doit lever AuthorError."""
        with pytest.raises(AuthorError):
            Book(title="1984", author="", year=1949)
    
    def test_year_too_old_raises_error(self):
        """Test : Une année < 1000 doit lever YearError."""
        with pytest.raises(YearError):
            Book(title="1984", author="Orwell", year=999)
    
    def test_year_too_recent_raises_error(self):
        """Test : Une année > 2025 doit lever YearError."""
        with pytest.raises(YearError):
            Book(title="1984", author="Orwell", year=2026)
    
    def test_invalid_rating_too_low(self):
        """Test : Un rating < 1 doit lever ValueError."""
        with pytest.raises(ValueError, match="rating"):
            Book(title="1984", author="Orwell", year=1949, rating=0)
    
    def test_invalid_rating_too_high(self):
        """Test : Un rating > 5 doit lever ValueError."""
        with pytest.raises(ValueError, match="rating"):
            Book(title="1984", author="Orwell", year=1949, rating=6)


class TestBookMethods:
    """Tests des méthodes de Book."""
    
    def test_matches_title_case_insensitive(self):
        """Test : matches_title doit être insensible à la casse."""
        book = Book(title="1984", author="Orwell", year=1949)
        
        assert book.matches_title("1984") is True
        assert book.matches_title("1984") is True
        assert book.matches_title("nineteen") is False
    
    def test_str_representation(self):
        """Test : La représentation string du livre."""
        book = Book(title="1984", author="George Orwell", year=1949)
        
        result = str(book)
        assert "1984" in result
        assert "George Orwell" in result
        assert "1949" in result