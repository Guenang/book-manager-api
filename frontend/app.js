// Configuration de l'API
const API_URL = "https://book-manager-api-0feo.onrender.com";

// Fonction pour afficher les messages
function showMessage(elementId, message, duration = 3000) {
  const el = document.getElementById(elementId);
  el.textContent = message;
  el.style.display = "block";
  setTimeout(() => {
    el.style.display = "none";
  }, duration);
}

// Charger les statistiques
async function loadStats() {
  try {
    const response = await fetch(`${API_URL}/books/stats`);
    const stats = await response.json();

    document.getElementById("stat-total").textContent = stats.total;
    document.getElementById("stat-oldest").textContent = stats.oldest || "-";
    document.getElementById("stat-newest").textContent = stats.newest || "-";
  } catch (error) {
    console.error("Erreur lors du chargement des stats:", error);
  }
}

// Afficher les livres
function displayBooks(books) {
  const listContainer = document.getElementById("books-list");

  if (books.length === 0) {
    listContainer.innerHTML = `
                    <div class="empty-state">
                        <p style="font-size: 3rem;">📚</p>
                        <p>Aucun livre dans votre bibliothèque</p>
                        <p>Ajoutez-en un pour commencer !</p>
                    </div>
                `;
    return;
  }

  listContainer.innerHTML = books
    .map(
      (book) => `
                <div class="book-item" data-id="${book.id}">
                    <div class="book-header">
                        <div>
                            <div class="book-title">📖 ${book.title}</div>
                            <div class="book-author">par ${book.author}</div>
                        </div>
                    </div>
                    <div class="book-meta">
                        <span class="meta-item">📅 ${book.year}</span>
                        ${
                          book.rating
                            ? `<span class="meta-item rating">${"⭐".repeat(
                                book.rating
                              )}</span>`
                            : ""
                        }
                    </div>
                    <div class="book-actions">
                        <button class="btn-edit" onclick="openEditModal(${
                          book.id
                        })">✏️ Modifier</button>
                        <button class="btn-delete" onclick="deleteBook(${
                          book.id
                        })">🗑️ Supprimer</button>
                    </div>
                </div>
            `
    )
    .join("");
}

// Charger tous les livres
async function loadBooks() {
  try {
    const response = await fetch(`${API_URL}/books/`);
    const books = await response.json();
    displayBooks(books);
    loadStats();
  } catch (error) {
    console.error("Erreur lors du chargement des livres:", error);
    document.getElementById("books-list").innerHTML = `
                    <div class="error-message" style="display: block;">
                        ❌ Erreur de connexion à l'API. Assurez-vous que le serveur est lancé.
                    </div>
                `;
  }
}

// Ajouter un livre
document
  .getElementById("add-book-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      title: document.getElementById("title").value,
      author: document.getElementById("author").value,
      year: parseInt(document.getElementById("year").value),
      rating: document.getElementById("rating").value
        ? parseInt(document.getElementById("rating").value)
        : null,
    };

    try {
      const response = await fetch(`${API_URL}/books/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        showMessage("form-success", "✅ Livre ajouté avec succès !");
        document.getElementById("add-book-form").reset();
        loadBooks();
      } else {
        const error = await response.json();
        showMessage("form-error", `❌ ${error.detail}`);
      }
    } catch (error) {
      showMessage("form-error", "❌ Erreur de connexion");
    }
  });

// Recherche en temps réel
document.getElementById("search-input").addEventListener("input", async (e) => {
  const query = e.target.value.trim();

  if (query === "") {
    loadBooks();
    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/books/search?q=${encodeURIComponent(query)}`
    );
    const books = await response.json();
    displayBooks(books);
  } catch (error) {
    console.error("Erreur lors de la recherche:", error);
  }
});

// Ouvrir le modal d'édition
async function openEditModal(bookId) {
  try {
    const response = await fetch(`${API_URL}/books/${bookId}`);
    const book = await response.json();

    document.getElementById("edit-id").value = book.id;
    document.getElementById("edit-title").value = book.title;
    document.getElementById("edit-author").value = book.author;
    document.getElementById("edit-year").value = book.year;
    document.getElementById("edit-rating").value = book.rating || "";

    document.getElementById("edit-modal").classList.add("active");
  } catch (error) {
    console.error("Erreur:", error);
  }
}

// Fermer le modal
function closeEditModal() {
  document.getElementById("edit-modal").classList.remove("active");
}

// Modifier un livre
document
  .getElementById("edit-book-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const bookId = document.getElementById("edit-id").value;
    const data = {
      title: document.getElementById("edit-title").value,
      author: document.getElementById("edit-author").value,
      year: parseInt(document.getElementById("edit-year").value),
      rating: document.getElementById("edit-rating").value
        ? parseInt(document.getElementById("edit-rating").value)
        : null,
    };

    try {
      const response = await fetch(`${API_URL}/books/${bookId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        closeEditModal();
        loadBooks();
      } else {
        const error = await response.json();
        showMessage("edit-error", `❌ ${error.detail}`);
      }
    } catch (error) {
      showMessage("edit-error", "❌ Erreur de connexion");
    }
  });

// Supprimer un livre
async function deleteBook(bookId) {
  if (!confirm("Êtes-vous sûr de vouloir supprimer ce livre ?")) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/books/${bookId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      loadBooks();
    } else {
      alert("Erreur lors de la suppression");
    }
  } catch (error) {
    alert("Erreur de connexion");
  }
}

// Charger les livres au démarrage
loadBooks();
