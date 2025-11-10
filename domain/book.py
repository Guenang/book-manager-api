from domain.exceptions import YearError, TitleError, AuthorError


class Book:
    """Représente un livre avec validation des données."""
    
    def __init__(self, title: str, author: str, year: int, rating: int = None, book_id: int = None):
        # Validation complète
        if not title or not title.strip():
            raise TitleError(title)
        if not author or not author.strip():
            raise AuthorError(author)
        if not isinstance(year, int) or year < 1000 or year > 2025:
            raise YearError(year)
        if rating is not None and (not isinstance(rating, int) or rating < 1 or rating > 5):
            raise ValueError("Le rating doit être entre 1 et 5")
        
        self.id = book_id
        self.title = title.strip()
        self.author = author.strip()
        self.year = year
        self.rating = rating

    def matches_title(self, search_term: str) -> bool:
        """Vérifie si le titre contient le terme recherché (insensible à la casse)."""
        return search_term.lower() in self.title.lower()

    def __str__(self):
        return f"📖 '{self.title}' par {self.author}, publié en {self.year}"
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', year={self.year})"
