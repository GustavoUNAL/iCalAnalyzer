from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Calendar Analytics API",
    version=settings.API_VERSION,
    debug=settings.DEBUG_MODE
)

# Configurar las políticas de CORS
origins = ["*"]  # Ajusta esta lista según los orígenes permitidos

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir el router principal con un prefijo
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Calendar Analytics API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}