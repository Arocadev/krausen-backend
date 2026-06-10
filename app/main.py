from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.api.auth import router as auth_router
from app.api.cervezas import router as cervezas_router
from app.api.ingredientes import router as ingredientes_router
from app.api.valoraciones import router as valoraciones_router
from app.api.ranking import router as ranking_router

load_dotenv()

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

app.include_router(auth_router)
app.include_router(cervezas_router)
app.include_router(ingredientes_router)
app.include_router(valoraciones_router)
app.include_router(ranking_router)

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