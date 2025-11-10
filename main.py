from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.database import create_tables
from api.routes import router
import os


IS_PRODUCTION = os.environ.get("RENDER") is not None

# Gestion du cycle de vie de l'application (méthode moderne)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gère les événements de démarrage et d'arrêt de l'application.
    Remplace les anciens @app.on_event("startup") et @app.on_event("shutdown")
    """
    # Code exécuté au DÉMARRAGE
    print("🚀 Démarrage de l'API Book Manager...")
    create_tables()
    print("✅ Tables de base de données créées/vérifiées")
    
    yield  # L'application tourne ici
    
    # Code exécuté à l'ARRÊT (si nécessaire)
    print("👋 Arrêt de l'API Book Manager...")


# Créer l'application FastAPI avec le lifespan
app = FastAPI(
    title="Book Manager API",
    description="API REST pour gérer une bibliothèque de livres",
    version="1.0.0",
    lifespan=lifespan  # Nouveau paramètre !
)

# Configuration CORS
allowed_origins = ["*"] if not IS_PRODUCTION else [
    "https://votre-frontend.com",  # Vous mettrez l'URL réelle plus tard
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # En production, spécifiez les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(router)

# Route racine pour vérifier que l'API fonctionne
@app.get("/")
def root():
    return {
        "message": "Bienvenue sur l'API Book Manager! 📚",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }


# Pour lancer l'application en développement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # Format string (important pour --reload)
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )