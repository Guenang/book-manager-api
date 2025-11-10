class YearError(Exception):
    def __init__(self, year):
        self.year = year
        super().__init__(f"Année invalide: {year}. L'année doit être entre 1000 et 2025.")


class TitleError(Exception):
    def __init__(self, title):
        self.title = title
        super().__init__(f"Titre invalide: Le titre ne peut pas être vide.")


class AuthorError(Exception):
    def __init__(self, author):
        self.author = author
        super().__init__(f"Auteur invalide: L'auteur ne peut pas être vide.")


class DuplicateBookError(Exception):
    def __init__(self, title, author):
        self.title = title
        self.author = author
        super().__init__(f"Le livre '{title}' par {author} existe déjà dans la bibliothèque.")


class BookNotFoundError(Exception):
    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(f"Livre non trouvé: {identifier}")