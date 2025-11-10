"""
Tests du BookService avec mocking du Repository.
"""
import pytest
from unittest.mock import Mock, MagicMock
from domain.book import Book
from domain.exceptions import DuplicateBookError, BookNotFoundError
from service.book_service import BookService


class TestBookServiceCreate:
    """Tests de création de livres via le service."""
    
    def test_create_book_success(self):
        """Test : Créer un livre quand il n'existe pas."""
        # ARRANGE : Préparer les données
        mock_repo = Mock()
        mock_repo.exists.return_value = False  # Le livre n'existe pas
        mock_repo.add.return_value = Book("1984", "Orwell", 1949, book_id=1)
        
        service = BookService(mock_repo)
        
        # ACT : Exécuter l'action
        result = service.create_book("1984", "Orwell", 1949)
        
        # ASSERT : Vérifier les résultats
        assert result.title == "1984"
        assert result.id == 1
        mock_repo.exists.assert_called_once_with("1984", "Orwell")
        mock_repo.add.assert_called_once()
    
    def test_create_book_duplicate_raises_error(self):
        """Test : Créer un livre qui existe déjà doit lever DuplicateBookError."""
        # ARRANGE
        mock_repo = Mock()
        mock_repo.exists.return_value = True  # Le livre existe déjà !
        
        service = BookService(mock_repo)
        
        # ACT & ASSERT
        with pytest.raises(DuplicateBookError):
            service.create_book("1984", "Orwell", 1949)
        
        # Vérifier que add() n'a jamais été appelé
        mock_repo.add.assert_not_called()
    
    def test_create_book_with_rating(self):
        """Test : Créer un livre avec un rating."""
        # ARRANGE
        mock_repo = Mock()
        mock_repo.exists.return_value = False
        mock_repo.add.return_value = Book("1984", "Orwell", 1949, rating=5, book_id=1)
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.create_book("1984", "Orwell", 1949, rating=5)
        
        # ASSERT
        assert result.rating == 5


class TestBookServiceRead:
    """Tests de lecture de livres."""
    
    def test_get_book_by_id_success(self):
        """Test : Récupérer un livre par son ID."""
        # ARRANGE
        mock_repo = Mock()
        expected_book = Book("1984", "Orwell", 1949, book_id=1)
        mock_repo.get_by_id.return_value = expected_book
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.get_book_by_id(1)
        
        # ASSERT
        assert result.id == 1
        assert result.title == "1984"
        mock_repo.get_by_id.assert_called_once_with(1)
    
    def test_get_book_by_id_not_found(self):
        """Test : Récupérer un livre inexistant doit lever BookNotFoundError."""
        # ARRANGE
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        service = BookService(mock_repo)
        
        # ACT & ASSERT
        with pytest.raises(BookNotFoundError):
            service.get_book_by_id(999)
    
    def test_list_all_books(self):
        """Test : Lister tous les livres."""
        # ARRANGE
        mock_repo = Mock()
        expected_books = [
            Book("1984", "Orwell", 1949, book_id=1),
            Book("Brave New World", "Huxley", 1932, book_id=2)
        ]
        mock_repo.get_all.return_value = expected_books
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.list_all_books()
        
        # ASSERT
        assert len(result) == 2
        assert result[0].title == "1984"
        assert result[1].title == "Brave New World"
    
    def test_search_books(self):
        """Test : Rechercher des livres par titre."""
        # ARRANGE
        mock_repo = Mock()
        expected_books = [Book("1984", "Orwell", 1949, book_id=1)]
        mock_repo.find_by_title.return_value = expected_books
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.search_books("1984")
        
        # ASSERT
        assert len(result) == 1
        assert result[0].title == "1984"
        mock_repo.find_by_title.assert_called_once_with("1984")


class TestBookServiceUpdate:
    """Tests de mise à jour de livres."""
    
    def test_update_book_success(self):
        """Test : Mettre à jour un livre existant."""
        # ARRANGE
        mock_repo = Mock()
        existing_book = Book("1984", "Orwell", 1949, book_id=1)
        updated_book = Book("1984 Updated", "Orwell", 1949, book_id=1)
        
        mock_repo.get_by_id.return_value = existing_book
        mock_repo.update.return_value = updated_book
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.update_book(1, title="1984 Updated", author="Orwell", year=1949)
        
        # ASSERT
        assert result.title == "1984 Updated"
        mock_repo.update.assert_called_once()
    
    def test_update_book_not_found(self):
        """Test : Mettre à jour un livre inexistant."""
        # ARRANGE
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        service = BookService(mock_repo)
        
        # ACT & ASSERT
        with pytest.raises(BookNotFoundError):
            service.update_book(999, title="New Title", author="author", year=1900)
    
    def test_update_book_partial(self):
        """Test : Mise à jour partielle (seulement rating)."""
        # ARRANGE
        mock_repo = Mock()
        existing_book = Book("1984", "Orwell", 1949, rating=3, book_id=1)
        updated_book = Book("1984", "Orwell", 1949, rating=5, book_id=1)
        
        mock_repo.get_by_id.return_value = existing_book
        mock_repo.update.return_value = updated_book
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.update_book(1, rating=5)
        
        # ASSERT
        assert result.rating == 5
        assert result.title == "1984"  # Titre inchangé


class TestBookServiceDelete:
    """Tests de suppression de livres."""
    
    def test_delete_book_success(self):
        """Test : Supprimer un livre existant."""
        # ARRANGE
        mock_repo = Mock()
        mock_repo.remove_by_id.return_value = True
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.delete_book(1)
        
        # ASSERT
        assert result is True
        mock_repo.remove_by_id.assert_called_once_with(1)
    
    def test_delete_book_not_found(self):
        """Test : Supprimer un livre inexistant."""
        # ARRANGE
        mock_repo = Mock()
        mock_repo.remove_by_id.return_value = False
        
        service = BookService(mock_repo)
        
        # ACT & ASSERT
        with pytest.raises(BookNotFoundError):
            service.delete_book(999)


class TestBookServiceStatistics:
    """Tests des statistiques."""
    
    def test_get_statistics_with_books(self):
        """Test : Statistiques quand il y a des livres."""
        # ARRANGE
        mock_repo = Mock()
        books = [
            Book("Book 1", "Author", 1950, book_id=1),
            Book("Book 2", "Author", 2000, book_id=2),
            Book("Book 3", "Author", 1975, book_id=3)
        ]
        mock_repo.get_all.return_value = books
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.get_statistics()
        
        # ASSERT
        assert result["total"] == 3
        assert result["oldest"] == 1950
        assert result["newest"] == 2000
    
    def test_get_statistics_empty(self):
        """Test : Statistiques quand il n'y a pas de livres."""
        # ARRANGE
        mock_repo = Mock()
        mock_repo.get_all.return_value = []
        
        service = BookService(mock_repo)
        
        # ACT
        result = service.get_statistics()
        
        # ASSERT
        assert result["total"] == 0
        assert result["oldest"] is None
        assert result["newest"] is None