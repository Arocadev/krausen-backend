<div align="center">

# Krausen — Backend

**API REST para plataforma de recetas de cerveza artesanal**

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)](https://sqlalchemy.org)
[![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://docker.com)

</div>

---

## ¿Qué es Krausen?

Krausen es el backend de una plataforma comunitaria para compartir, descubrir y versionar recetas de cerveza artesanal. El nombre hace referencia a la espuma que se forma durante la fermentación. La API gestiona autenticación, recetas, forks, me gustas, comentarios, notificaciones y seguimiento de fermentación.

---

## ✨ Funcionalidades

- 🔐 **Autenticación JWT** — registro, login, cambio de contraseña con BCrypt
- 🔑 **Recuperación de contraseña** — email con Resend, tokens de reset con expiración
- 👥 **Gestión de usuarios** — roles USER y ADMIN, perfil público y privado
- 🍺 **Gestión de cervezas** — CRUD completo, búsqueda con filtros por nombre, estilo, alcohol, IBU, ingrediente y autor
- 🔀 **Sistema de forks** — versionar cualquier receta, con árbol de versiones por CTE recursiva
- ❤️ **Me gusta** — likes con bloqueo de autovaloración y notificación automática
- 🏆 **Ranking** — top 10 mensual, anual y global por me gustas
- 💬 **Comentarios** — comentarios por receta
- 🔔 **Notificaciones** — me gustas y forks con badge en navbar
- 🌡️ **Registro de temperaturas** — seguimiento de fermentación con intervalos configurables
- 🧪 **47 ingredientes precargados** — maltas, lúpulos, levaduras y adjuntos
- 📝 **Pasos de elaboración** — instrucciones ordenadas con duración estimada
- ✏️ **Edición controlada** — solo editable si no tiene forks derivados
- 🛡️ **Seguridad** — rate limiting, headers HTTP, sanitización, validaciones Pydantic completas
- ⚡ **Consultas optimizadas** — CTE recursiva en árbol de forks, queries fusionadas, joinedload contra N+1
- 📖 **Documentación automática** — Swagger / OpenAPI en `/docs`

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Framework | Python 3.14 + FastAPI |
| Seguridad | JWT (python-jose) + BCrypt |
| ORM | SQLAlchemy 2.0 |
| Migraciones | Alembic |
| Base de datos | PostgreSQL 16 |
| Validación | Pydantic v2 |
| Email | Resend |
| Contenedores | Docker + Docker Compose |

---

## 📁 Estructura del proyecto

```
app/
├── api/
│   ├── auth.py              # Registro, login, recuperación de contraseña
│   ├── cervezas.py          # CRUD, forks, búsqueda, árbol CTE
│   ├── ingredientes.py      # Catálogo de ingredientes
│   ├── valoraciones.py      # Me gusta
│   ├── ranking.py           # Ranking mensual, anual y global
│   ├── temperaturas.py      # Seguimiento de fermentación
│   ├── comentarios.py       # Comentarios por receta
│   ├── notificaciones.py    # Notificaciones
│   ├── perfiles_publicos.py # Perfil público
│   └── perfil.py            # Perfil privado y cambio de contraseña
├── core/
│   ├── security.py          # JWT, BCrypt, tokens
│   ├── deps.py              # Dependencias de autenticación
│   ├── exceptions.py        # Exception handlers centralizados
│   └── seed.py              # Datos iniciales de ingredientes
├── models/                  # Entidades SQLAlchemy
├── schemas/                 # DTOs Pydantic con validaciones completas
├── services/                # Lógica de negocio
└── main.py                  # Punto de entrada FastAPI
```

---

## 🔗 Endpoints destacados

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/registro` | Registro de usuario |
| POST | `/api/auth/login` | Login con JWT |
| POST | `/api/auth/solicitar-recuperacion` | Solicitar reset de contraseña |
| POST | `/api/auth/reset-password` | Restablecer contraseña |
| GET | `/api/cervezas/` | Listar cervezas |
| GET | `/api/cervezas/buscar` | Buscar con filtros |
| POST | `/api/cervezas/` | Crear cerveza |
| PUT | `/api/cervezas/{id}` | Editar cerveza |
| POST | `/api/cervezas/{id}/fork` | Crear versión |
| GET | `/api/cervezas/arbol/{id}` | Árbol de forks (CTE recursiva) |
| POST | `/api/cervezas/{id}/me-gusta` | Dar me gusta |
| DELETE | `/api/cervezas/{id}/me-gusta` | Quitar me gusta |
| GET | `/api/ranking/mensual` | Top 10 del mes |
| GET | `/api/ranking/anual` | Top 10 del año |
| GET | `/api/ranking/global` | Top 10 global |
| GET | `/api/cervezas/{id}/comentarios` | Listar comentarios |
| POST | `/api/cervezas/{id}/comentarios` | Añadir comentario |
| GET | `/api/notificaciones/` | Listar notificaciones |
| PATCH | `/api/notificaciones/leer-todas` | Marcar todas como leídas |
| GET | `/api/usuarios/{username}` | Perfil público |
| POST | `/api/cervezas/{id}/temperaturas` | Registrar temperatura |
| GET | `/api/perfil/` | Ver perfil privado |
| PUT | `/api/perfil/password` | Cambiar contraseña |

Documentación completa en `/docs` (Swagger UI).

---

## 🧪 Ingredientes iniciales

47 ingredientes precargados organizados por tipo:

| Tipo | Cantidad | Ejemplos |
|------|----------|----------|
| Malta | 12 | Pilsner, Pale Ale, Chocolate, Trigo... |
| Lúpulo | 12 | Cascade, Citra, Saaz, Mosaic... |
| Levadura | 7 | Ale Americana, Lager, Belga, Kveik... |
| Adjunto | 16 | Café, Cacao, Miel, Vainilla, Frambuesa... |

---

## 🚀 Instalación y arranque

```bash
git clone https://github.com/ArocaDev/krausen-backend
cd krausen-backend

python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

pip install -r requirements.txt

cp .env.example .env
# Edita .env con tus credenciales

alembic upgrade head
python create_users.py
python seed.py
python seed_recetas.py

uvicorn app.main:app --reload
```

API disponible en `http://127.0.0.1:8000` · Swagger en `http://127.0.0.1:8000/docs`

---

## 🐳 Docker

```bash
docker compose up db -d
uvicorn app.main:app --reload
```

---

## 🔑 Variables de entorno

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/krausen
POSTGRES_PASSWORD=password
SECRET_KEY=tu_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
RESEND_API_KEY=tu_resend_key
```

---

## 🔗 Repositorios del proyecto

| Componente | Repositorio |
|---|---|
| Backend (este repo) | [krausen-backend](https://github.com/ArocaDev/krausen-backend) |
| Frontend | [krausen-frontend](https://github.com/ArocaDev/krausen-frontend) |

---

## 👤 Autor

**Alejandro Rodríguez Calabuig**
[github.com/ArocaDev](https://github.com/ArocaDev) · [LinkedIn](https://www.linkedin.com/in/alejandro-rodriguez-calabuig-a871a1230)

---

## 📄 Licencia

Proyecto personal — no licenciado para uso comercial.
