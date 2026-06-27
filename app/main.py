from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from app.api.auth import router as auth_router
from app.api.cervezas import router as cervezas_router
from app.api.ingredientes import router as ingredientes_router
from app.api.valoraciones import router as valoraciones_router
from app.api.ranking import router as ranking_router
from app.api.perfil import router as perfil_router
from app.api.temperaturas import router as temperaturas_router
from app.api.notificaciones import router as notificaciones_router
from app.api.comentarios import router as comentarios_router
from app.api.perfiles_publicos import router as perfiles_publicos_router

load_dotenv()

os.makedirs("uploads/cervezas", exist_ok=True)

app = FastAPI(
    title="Krausen API",
    description="API para la plataforma de recetas de cerveza artesanal Krausen",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_router)
app.include_router(cervezas_router)
app.include_router(ingredientes_router)
app.include_router(valoraciones_router)
app.include_router(ranking_router)
app.include_router(perfil_router)
app.include_router(temperaturas_router)
app.include_router(notificaciones_router)
app.include_router(comentarios_router)
app.include_router(perfiles_publicos_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": 500, "error": "Error interno del servidor", "mensaje": str(exc)}
    )

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Krausen 🍺"}

@app.get("/health")
def health():
    return {"status": "ok"}