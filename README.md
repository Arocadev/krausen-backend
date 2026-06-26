# Krausen — Backend

> API REST para plataforma de recetas de cerveza artesanal | REST API for craft beer recipe platform

---

## 🇪🇸 Español

**Krausen** es el backend de una plataforma comunitaria para compartir, descubrir y versionar recetas de cerveza artesanal. El nombre hace referencia a la espuma que se forma durante la fermentación de la cerveza.

---

### ✨ Funcionalidades

- 🔐 **Autenticación JWT** — registro, login, cambio de contraseña, encriptación BCrypt
- 👥 **Gestión de usuarios** — roles USER y ADMIN, perfil de usuario
- 🍺 **Gestión de cervezas** — CRUD completo, búsqueda con filtros por nombre, estilo, alcohol e IBU
- 🔀 **Sistema de forks** — crea tu propia versión de cualquier receta, con árbol de versiones
- ❤️ **Me gusta** — sistema de likes con bloqueo de autovaloración
- 🏆 **Ranking mensual** — las recetas más gustadas del mes
- 🌡️ **Registro de temperaturas** — seguimiento de fermentación con intervalos configurables
- 🧪 **Ingredientes predefinidos** — lista curada de maltas, lúpulos, levaduras y adjuntos
- 📝 **Pasos de elaboración** — instrucciones ordenadas con duración estimada
- ✏️ **Edición controlada** — editar receta solo si no tiene forks derivados
- 📖 **Documentación automática** — Swagger / OpenAPI disponible en `/docs`

---

### 🛠️ Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Framework | Python 3.14 + FastAPI |
| Seguridad | JWT (python-jose) + BCrypt |
| ORM | SQLAlchemy 2.0 |
| Migraciones | Alembic |
| Base de datos | PostgreSQL 16 |
| Validación | Pydantic v2 |
| Despliegue | Docker + Docker Compose |

---

### 📁 Estructura del proyecto

```
app/
├── api/            # Endpoints REST
│   ├── auth.py          # Registro y login
│   ├── cervezas.py      # CRUD cervezas, forks, búsqueda, árbol
│   ├── ingredientes.py  # Gestión de ingredientes
│   ├── valoraciones.py  # Sistema de me gusta
│   ├── ranking.py       # Ranking mensual por likes
│   ├── temperaturas.py  # Registro de fermentación
│   └── perfil.py        # Perfil y cambio de contraseña
├── core/           # Seguridad y configuración
│   ├── security.py      # JWT, BCrypt, tokens
│   ├── deps.py          # Dependencias (auth, roles)
│   └── seed.py          # Datos iniciales de ingredientes
├── models/         # Entidades SQLAlchemy
│   ├── usuario.py       # Usuario con roles
│   ├── cerveza.py       # Receta con fork (parent_id)
│   ├── ingrediente.py   # Ingrediente + tabla intermedia
│   ├── paso.py          # Pasos de elaboración
│   ├── valoracion.py    # Me gusta (MeGusta)
│   └── temperatura.py   # Registro de temperaturas
├── schemas/        # DTOs con Pydantic
│   ├── usuario.py       # Create, Login, Response, Token
│   └── cerveza.py       # Create, Response, ingredientes, pasos
├── services/       # Lógica de negocio
│   ├── usuario_service.py
│   ├── cerveza_service.py
│   ├── valoracion_service.py
│   └── ingrediente_service.py
└── main.py         # Punto de entrada FastAPI
```

---

### 🔗 Endpoints destacados

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/registro` | Registro de usuario |
| POST | `/api/auth/login` | Login con JWT |
| GET | `/api/cervezas/` | Listar todas las cervezas |
| GET | `/api/cervezas/buscar` | Buscar con filtros |
| POST | `/api/cervezas/` | Crear cerveza |
| PUT | `/api/cervezas/{id}` | Editar cerveza (sin forks) |
| POST | `/api/cervezas/{id}/fork` | Crear versión |
| GET | `/api/cervezas/arbol/{id}` | Árbol de forks |
| POST | `/api/cervezas/{id}/me-gusta` | Dar me gusta |
| DELETE | `/api/cervezas/{id}/me-gusta` | Quitar me gusta |
| GET | `/api/ranking/mensual` | Top 10 del mes |
| POST | `/api/cervezas/{id}/temperaturas` | Registrar temperatura |
| GET | `/api/cervezas/{id}/temperaturas` | Historial de temperaturas |
| GET | `/api/perfil/` | Ver perfil |
| PUT | `/api/perfil/password` | Cambiar contraseña |

Documentación completa en `/docs` (Swagger UI).

---

### 🧪 Ingredientes iniciales

47 ingredientes precargados organizados por tipo:

| Tipo | Cantidad | Ejemplos |
|------|----------|----------|
| Malta | 12 | Pilsner, Pale Ale, Chocolate, Trigo... |
| Lúpulo | 12 | Cascade, Citra, Saaz, Mosaic... |
| Levadura | 7 | Ale Americana, Lager, Belga, Kveik... |
| Adjunto | 16 | Café, Cacao, Miel, Vainilla, Frambuesa... |

---

### 🚀 Instalación y arranque

```bash
# Clonar el repositorio
git clone https://github.com/krausen-beer/krausen-backend
cd krausen-backend

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar migraciones
alembic upgrade head

# Cargar ingredientes iniciales
python seed.py

# Arrancar el servidor
uvicorn app.main:app --reload
```

API disponible en `http://127.0.0.1:8000` · Swagger en `http://127.0.0.1:8000/docs`

---

### 🐳 Despliegue con Docker

```bash
docker-compose up --build
```

---

### 🔗 Repositorios del proyecto

| Componente | Repositorio |
|---|---|
| Backend (este repo) | [krausen-backend](https://github.com/krausen-beer/krausen-backend) |
| Frontend | [krausen-frontend](https://github.com/krausen-beer/krausen-frontend) |
| Bot de Telegram | [audio-to-trello-bot](https://github.com/krausen-beer/audio-to-trello-bot) |

---

## 🌐 English

**Krausen** is the backend for a community platform to share, discover and version craft beer recipes. The name refers to the foam layer that forms during beer fermentation.

---

### ✨ Features

- 🔐 **JWT Authentication** — registration, login, password change, BCrypt encryption
- 👥 **User management** — USER and ADMIN roles, user profile
- 🍺 **Beer management** — full CRUD, search with filters by name, style, ABV and IBU
- 🔀 **Fork system** — create your own version of any recipe, with version tree
- ❤️ **Likes** — like system with self-like prevention
- 🏆 **Monthly ranking** — most liked recipes of the month
- 🌡️ **Temperature tracking** — fermentation monitoring with configurable intervals
- 🧪 **Predefined ingredients** — curated list of malts, hops, yeasts and adjuncts
- 📝 **Brewing steps** — ordered instructions with estimated duration
- ✏️ **Controlled editing** — edit recipe only if it has no derived forks
- 📖 **Auto documentation** — Swagger / OpenAPI available at `/docs`

---

### 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Python 3.14 + FastAPI |
| Security | JWT (python-jose) + BCrypt |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Validation | Pydantic v2 |
| Deployment | Docker + Docker Compose |

---

### 🚀 Getting Started

```bash
git clone https://github.com/krausen-beer/krausen-backend
cd krausen-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```

API at `http://127.0.0.1:8000` · Swagger at `http://127.0.0.1:8000/docs`

---

## 👤 Autores / Authors

**Alejandro Rodríguez Calabuig** — [github.com/ArocaDev](https://github.com/ArocaDev)

---

## 📄 Licencia / License

Proyecto personal en desarrollo.
Personal project under development.
