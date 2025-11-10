"""Tests de l'API REST."""


def test_root_endpoint(client):
    """Test : L'endpoint racine fonctionne."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_create_book(client):
    """Test : Créer un livre."""
    response = client.post("/books/", json={
        "title": "1984",
        "author": "George Orwell",
        "year": 1949
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"
    assert data["year"] == 1949
    assert "id" in data


def test_list_books_empty(client):
    """Test : Lister les livres quand il n'y en a pas."""
    response = client.get("/books/")
    
    assert response.status_code == 200
    assert response.json() == []


def test_list_books_with_data(client):
    """Test : Lister les livres."""
    # Créer 2 livres
    client.post("/books/", json={
        "title": "Book 1",
        "author": "Author 1",
        "year": 2000
    })
    client.post("/books/", json={
        "title": "Book 2",
        "author": "Author 2",
        "year": 2001
    })
    
    # Lister
    response = client.get("/books/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Book 1"
    assert data[1]["title"] == "Book 2"


def test_get_book_by_id(client):
    """Test : Récupérer un livre par son ID."""
    # Créer un livre
    create_response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "year": 2000
    })
    book_id = create_response.json()["id"]
    
    # Récupérer le livre
    response = client.get(f"/books/{book_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == "Test Book"


def test_get_book_not_found(client):
    """Test : Récupérer un livre inexistant."""
    response = client.get("/books/999")
    
    assert response.status_code == 404


def test_search_books(client):
    """Test : Rechercher des livres."""
    # Créer des livres
    client.post("/books/", json={
        "title": "Python Programming",
        "author": "Author",
        "year": 2020
    })
    client.post("/books/", json={
        "title": "JavaScript Guide",
        "author": "Author",
        "year": 2021
    })
    
    # Rechercher "Python"
    response = client.get("/books/search?q=Python")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Python Programming"


def test_update_book(client):
    """Test : Mettre à jour un livre."""
    # Créer un livre
    create_response = client.post("/books/", json={
        "title": "Original",
        "author": "Author",
        "year": 2000
    })
    book_id = create_response.json()["id"]
    
    # Mettre à jour
    response = client.put(f"/books/{book_id}", json={
        "rating": 5
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["title"] == "Original"  # Titre inchangé


def test_delete_book(client):
    """Test : Supprimer un livre."""
    # Créer un livre
    create_response = client.post("/books/", json={
        "title": "To Delete",
        "author": "Author",
        "year": 2000
    })
    book_id = create_response.json()["id"]
    
    # Supprimer
    response = client.delete(f"/books/{book_id}")
    
    assert response.status_code == 204
    
    # Vérifier qu'il n'existe plus
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


def test_create_duplicate_book(client):
    """Test : Créer un livre en double."""
    # Créer le premier
    client.post("/books/", json={
        "title": "Duplicate",
        "author": "Author",
        "year": 2000
    })
    
    # Essayer de créer le doublon
    response = client.post("/books/", json={
        "title": "Duplicate",
        "author": "Author",
        "year": 2000
    })
    
    assert response.status_code == 409


def test_get_statistics(client):
    """Test : Obtenir les statistiques."""
    # Créer des livres
    client.post("/books/", json={
        "title": "Old Book",
        "author": "Author",
        "year": 1950
    })
    client.post("/books/", json={
        "title": "New Book",
        "author": "Author",
        "year": 2020
    })
    
    response = client.get("/books/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["oldest"] == 1950
    assert data["newest"] == 2020

