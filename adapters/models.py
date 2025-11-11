from sqlalchemy import Column, Integer, String
from adapters.database import Base

class BookModel(Base):
    """
    Modèle SQLAlchemy pour la table 'books'.
    C'est la représentation de la table en base de données.
    """
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=True)
    
    def to_domain(self):
        """Convertit le modèle DB en objet Domain Book."""
        from domain.book import Book
        return Book(
            title=self.title,
            author=self.author,
            year=self.year,
            rating=self.rating,
            book_id=self.id
        )