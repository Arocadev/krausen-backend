from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import time
from collections import defaultdict
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

# Rate limiting simple en memoria
rate_limit_store: dict = defaultdict(list)
RATE_LIMIT_ENDPOINTS = ["/api/auth/login", "/api/auth/registro", "/api/auth/solicitar-recuperacion"]
RATE_LIMIT_MAX = 10      # máximo de peticiones
RATE_LIMIT_WINDOW = 60   # en segundos

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path in RATE_LIMIT_ENDPOINTS:
        ip = request.client.host
        ahora = time.time()
        ventana = rate_limit_store[ip]
        # Limpiar peticiones fuera de la ventana
        rate_limit_store[ip] = [t for t in ventana if ahora - t < RATE_LIMIT_WINDOW]
        if len(rate_limit_store[ip]) >= RATE_LIMIT_MAX:
            return JSONResponse(
                status_code=429,
                content={"detail": "Demasiadas peticiones. Espera un momento antes de volver a intentarlo."}
            )
        rate_limit_store[ip].append(ahora)
    response = await call_next(request)
    return response

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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