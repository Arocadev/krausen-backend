<div align="center">

# Krausen — Backend

**API REST para la plataforma de recetas de cerveza artesanal**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://docker.com)

</div>

---

## ¿Qué es Krausen?

Krausen es una plataforma de recetas de cerveza artesanal donde los usuarios pueden publicar sus elaboraciones, hacer versiones (forks) de recetas existentes, registrar temperaturas de fermentación y valorar las recetas de la comunidad. Este repositorio contiene el backend — la API REST construida con FastAPI.

🍺 **Frontend:** [github.com/ArocaDev/krausen-frontend](https://github.com/ArocaDev/krausen-frontend)

---

## ✨ Funcionalidades

- **Autenticación JWT** con access token (30 min) y refresh token (7 días)
- **Recetas** — CRUD completo con ingredientes, pasos, estilo, alcohol, IBU y volumen
- **Sistema de forks** — cualquier receta puede ser versionada; el árbol de versiones se construye con una CTE recursiva en PostgreSQL
- **Fermentación** — registro de temperaturas por intervalos configurables (cada N horas durante X días)
- **Me gustas** — un me gusta por usuario por receta
- **Ranking** — top recetas por mes, año y global calculado en tiempo real
- **Notificaciones** — al recibir un me gusta o fork
- **Comentarios** — por receta con gestión de permisos
- **Perfiles públicos** — recetas y me gustas de cada usuario
- **Recuperación de contraseña** vía email con Resend
- **Rate limiting** en endpoints de autenticación
- **i18n** — respuestas de error en ES/EN/DE según header `Accept-Language`

---

## 🗂️ Diagramas

### Arquitectura del sistema
![Arquitectura](assets/krausen_arquitectura.svg)

### Flujo JWT
![JWT](assets/krausen_jwt.svg)

### Sistema de forks
![Fork](assets/krausen_fork.svg)

---

## 🛠️ Stack técnico

| Capa | Tecnología |
|------|-----------|
| Framework | FastAPI 0.115 + Python 3.11 |
| Base de datos | PostgreSQL 16 + SQLAlchemy 2 |
| Migraciones | Alembic |
| Auth | JWT (python-jose) + bcrypt |
| Email | Resend |
| Contenedores | Docker + Docker Compose |
| Documentación | Swagger UI / ReDoc (auto) |

---

## 📁 Estructura del proyecto

```
krausen-backend/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── cervezas.py
│   │   ├── comentarios.py
│   │   ├── ingredientes.py
│   │   ├── notificaciones.py
│   │   ├── perfil.py
│   │   ├── perfiles_publicos.py
│   │   ├── ranking.py
│   │   ├── temperaturas.py
│   │   └── valoraciones.py
│   ├── core/
│   │   ├── deps.py
│   │   ├── exceptions.py
│   │   └── security.py
│   └── models/
│       ├── base.py
│       ├── cerveza.py
│       ├── comentario.py
│       ├── ingrediente.py
│       ├── me_gusta.py
│       ├── notificacion.py
│       ├── registro_temperatura.py
│       └── usuario.py
├── alembic/
│   └── versions/
├── assets/
│   ├── krausen_arquitectura.svg
│   ├── krausen_jwt.svg
│   └── krausen_fork.svg
├── create_users.py
├── seed.py
├── seed_recetas.py
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── requirements.txt
```

---

## 🚀 Instalación con Docker (recomendado)

```bash
git clone https://github.com/ArocaDev/krausen-backend.git
cd krausen-backend
cp .env.example .env
# Edita .env con tus credenciales
docker compose up --build -d
docker compose exec backend alembic upgrade head
docker compose exec backend python create_users.py
docker compose exec backend python seed.py
docker compose exec backend python seed_recetas.py
```

API disponible en `http://localhost:8000`  
Swagger en `http://localhost:8000/docs`

---

## 🚀 Instalación local

```bash
git clone https://github.com/ArocaDev/krausen-backend.git
cd krausen-backend
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus credenciales
alembic upgrade head
python create_users.py
python seed.py
python seed_recetas.py
uvicorn app.main:app --reload
```

---

## 🔑 Variables de entorno

```env
# Local
DATABASE_URL=postgresql://postgres:password@localhost:5432/krausen
# Docker (usar 'db' en vez de 'localhost')
DATABASE_URL=postgresql://postgres:password@db:5432/krausen
POSTGRES_PASSWORD=password
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RESEND_API_KEY=re_...
```

---

## 📡 Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/registro` | Crear cuenta |
| POST | `/api/auth/login` | Login → JWT |
| POST | `/api/auth/refresh` | Renovar token |
| GET | `/api/cervezas` | Listar recetas con filtros |
| POST | `/api/cervezas` | Crear receta |
| GET | `/api/cervezas/{id}` | Detalle de receta |
| POST | `/api/cervezas/{id}/fork` | Hacer fork de una receta |
| GET | `/api/cervezas/arbol/{id}` | Árbol de versiones (CTE recursiva) |
| POST | `/api/cervezas/{id}/me-gusta` | Dar/quitar me gusta |
| GET | `/api/temperaturas/{id}` | Registros de fermentación |
| POST | `/api/temperaturas/{id}` | Añadir lectura de temperatura |
| GET | `/api/ranking` | Top recetas (mes/año/global) |
| GET | `/api/notificaciones` | Notificaciones del usuario |
| GET | `/api/perfiles/{username}` | Perfil público |

Documentación completa en `/docs` (Swagger) o `/redoc`.

---

## 🗺️ Roadmap

- [x] Auth JWT con refresh token
- [x] CRUD de recetas con ingredientes y pasos
- [x] Sistema de forks con árbol recursivo (CTE PostgreSQL)
- [x] Registro de temperaturas de fermentación
- [x] Me gustas y ranking mensual/anual/global
- [x] Notificaciones
- [x] Comentarios
- [x] Recuperación de contraseña con Resend
- [x] Rate limiting
- [x] Docker Compose
- [x] i18n en errores (ES/EN/DE)
- [ ] Tests unitarios
- [ ] Despliegue en Railway


---

## 👤 Autor

**Alejandro Rodríguez Calabuig**  
[github.com/ArocaDev](https://github.com/ArocaDev) · [LinkedIn](https://www.linkedin.com/in/alejandro-rodriguez-calabuig-a871a1230)

---

## 📄 Licencia

Proyecto personal — no licenciado para uso comercial.
