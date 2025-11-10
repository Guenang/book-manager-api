from service.book_service import BookService
from domain.exceptions import YearError, TitleError, AuthorError

class ConsoleUI:
    """Interface console pour gérer les livres."""
    
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    def display_menu(self):
        """Affiche le menu principal."""
        print("\n" + "="*50)
        print("📚 GESTIONNAIRE DE BIBLIOTHÈQUE")
        print("="*50)
        print("1. Ajouter un livre")
        print("2. Lister tous les livres")
        print("3. Rechercher un livre")
        print("4. Voir les statistiques")
        print("5. Quitter")
        print("6. Supprimer un livre")
        print("="*50)

    def add_book(self):
        """Interface pour ajouter un livre."""
        print("\n➕ Ajout d'un nouveau livre")
        print("-" * 30)
        
        try:
            title = input("Titre du livre: ")
            author = input("Auteur: ")
            year = int(input("Année de publication: "))
            
            book = self.book_service.create_book(title, author, year)
            print(f"\n✅ Livre ajouté avec succès!")
            print(f"   {book}")
            
        except ValueError:
            print("\n❌ Erreur: L'année doit être un nombre entier.")
        except (YearError, TitleError, AuthorError) as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")

    def list_books(self):
        """Affiche tous les livres."""
        books = self.book_service.list_all_books()
        
        print("\n📚 Liste des livres")
        print("-" * 30)
        
        if not books:
            print("Aucun livre dans la bibliothèque.")
            return
        
        for i, book in enumerate(books, 1):
            print(f"{i}. {book}")

    def search_books(self):
        """Interface pour rechercher des livres."""
        print("\n🔍 Recherche de livres")
        print("-" * 30)
        
        search_term = input("Entrez le titre (ou une partie): ")
        
        if not search_term.strip():
            print("❌ Veuillez entrer un terme de recherche.")
            return
        
        results = self.book_service.search_books(search_term)
        
        if not results:
            print(f"\nAucun livre trouvé pour '{search_term}'.")
        else:
            print(f"\n✅ {len(results)} livre(s) trouvé(s):")
            for i, book in enumerate(results, 1):
                print(f"   {i}. {book}")

    def show_statistics(self):
        """Affiche des statistiques sur la collection."""
        stats = self.book_service.get_statistics()
        
        print("\n📊 Statistiques de la bibliothèque")
        print("-" * 30)
        
        if stats["total"] == 0:
            print("Aucun livre dans la bibliothèque.")
            return
        
        print(f"Nombre total de livres: {stats['total']}")
        print(f"Livre le plus ancien: {stats['oldest']}")
        print(f"Livre le plus récent: {stats['newest']}")
    

    def delete_book(self):
        print("\n🗑️ Suppression d'un livre")
        print("-" * 30)
    
        title = input("Titre du livre à supprimer: ")
        result = self.book_service.delete_book(title)
        if result:
            print(f"le livre avec le titre {title} supprimer avec success ✅")
        else:
            print(f"échec de suppression ❌ le livre le livre avec le titre {title} na pas été trouver")

    def run(self):
        """Boucle principale de l'application."""
        print("\n🎉 Bienvenue dans votre gestionnaire de bibliothèque!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nVotre choix (1-6): ").strip()
                
                if choice == "1":
                    self.add_book()
                elif choice == "2":
                    self.list_books()
                elif choice == "3":
                    self.search_books()
                elif choice == "4":
                    self.show_statistics()
                elif choice == "5":
                    print("\n👋 Au revoir! À bientôt!")
                    break
                elif choice == "6":
                    self.delete_book()
                else:
                    print("\n❌ Choix invalide. Veuillez choisir entre 1 et 6.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programme interrompu. Au revoir!")
                break
            except Exception as e:
                print(f"\n❌ Erreur inattendue: {e}")
