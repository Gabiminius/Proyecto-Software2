# Sistema de Registro de Incidentes Escolares

Aplicación web full-stack para registrar, consultar y gestionar incidentes escolares.

**Tecnologías:**
- **Backend:** FastAPI + SQLAlchemy Async (Python)
- **Frontend:** React + Vite (JavaScript)
- **Base de datos:** PostgreSQL (Neon - cloud)

## ¿Qué hace el proyecto?

### Funcionalidades actuales:

1. **Registro de incidentes** - Formulario web para reportar nuevos incidentes
   - Título y descripción detallada
   - Tipo: Convivencia, Disciplina, Acoso, Seguridad, Otro
   - Severidad: Baja, Media, Alta, Crítica
   - Datos del estudiante, curso y docente reportante
   - Fecha y hora del incidente

2. **Listado y filtrado** - Visualizar todos los incidentes registrados
   - Filtrar por tipo de incidente
   - Filtrar por estado (Abierto, En revisión, Resuelto, Cerrado)
   - Filtrar por curso o nombre del estudiante
   - Búsqueda por título o descripción

3. **Estado de la base de datos** - Endpoint de health check
   - Verifica conectividad con PostgreSQL
   - Devuelve estado: `ok` (conectada) o `degraded` (no disponible)

### Estructura del proyecto

```text
.
├─ backend/
│  ├─ app/
│  │  ├─ api/v1/endpoints/      # Endpoints (health, incidents)
│  │  ├─ core/                  # Configuracion y DB
│  │  ├─ crud/                  # Acceso a datos
│  │  ├─ models/                # Modelos SQLAlchemy
│  │  ├─ schemas/               # Contratos de entrada/salida
│  │  └─ main.py                # App FastAPI
│  ├─ .env.example
│  └─ requirements.txt
└─ frontend/
   ├─ src/
   │  ├─ api/
   │  ├─ components/
   │  ├─ App.jsx
   │  └─ main.jsx
   ├─ .env.example
   └─ package.json
```

## Requisitos previos

- **Python 3.11+** (para el backend)
- **Node.js 20+** y **npm 10+** (para el frontend)
- **PostgreSQL en Neon** - La conexión ya está configurada en el archivo `.env`

## Configuración inicial para cada integrante

### Paso 1: Clonar el repositorio
```powershell
git clone <URL-del-repositorio>
cd Proyecto-Software2
```

### Paso 2: Crear archivos `.env` locales desde plantillas

**Backend:**
```powershell
Copy-Item backend\.env.example backend\.env
```

**Frontend:**
```powershell
Copy-Item frontend\.env.example frontend\.env
```

### Paso 3: Configurar credenciales en `backend/.env`

Edita el archivo y reemplaza con tus datos:
```env
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST/DBNAME?ssl=require
```

> **⚠️ IMPORTANTE:** 
> - El archivo `.env` **NUNCA** se sube a Git (está en `.gitignore`)
> - Cada integrante tiene su propia copia local
> - Las credenciales quedan privadas en tu máquina

### Paso 4: Frontend está listo
El archivo `frontend/.env` ya apunta correctamente a `http://localhost:8000/api/v1`

## Ejecución local

### Opción 1: En la misma terminal (secuencial)

**Terminal 1 - Backend:**
```powershell
cd backend
python -m venv .venv  # Solo la primera vez
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Luego, en otra terminal:

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm install  # Solo la primera vez
npm run dev
```

### Opción 2: En terminales separadas (recomendado)

**Terminal 1:**
```powershell
cd Proyecto-Software2\backend
python -m venv .venv  # Solo la primera vez
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2:**
```powershell
cd Proyecto-Software2\frontend
npm install  # Solo la primera vez
npm run dev
```

## Acceso a la aplicación

- **Frontend:** http://localhost:5173 (o http://localhost:5174 si 5173 está ocupado)
- **API Backend:** http://localhost:8000/api/v1
- **Documentación API (Swagger):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/v1/health

## API Endpoints

### Health / Estado
- `GET /api/v1/health` - Verifica la conexión con la base de datos

### Incidentes
- `POST /api/v1/incidents` - Crear un nuevo incidente
- `GET /api/v1/incidents` - Listar todos los incidentes (con filtros opcionales)
- `GET /api/v1/incidents/{incident_id}` - Obtener detalle de un incidente

### Parámetros de filtrado en GET /api/v1/incidents:
```
?incident_type=convivencia   # Filtrar por tipo
?status=abierto              # Filtrar por estado
?course=9B                   # Filtrar por curso (búsqueda parcial)
?student_name=Miguel         # Filtrar por estudiante (búsqueda parcial)
?search=conflicto            # Buscar en título o descripción
```

## Comandos útiles

### Frontend (React)
```powershell
npm run dev    # Inicia servidor de desarrollo
npm run build  # Construye para producción
npm run lint   # Verifica código
```

### Backend (FastAPI)
```powershell
uvicorn app.main:app --reload --port 8000  # Inicia servidor
```

## Arquitectura

La aplicación está dividida en capas:

- **`backend/app/api/`** - Rutas y endpoints
- **`backend/app/crud/`** - Operaciones en base de datos
- **`backend/app/models/`** - Modelos SQLAlchemy (tablas DB)
- **`backend/app/schemas/`** - Validación de datos (entrada/salida)
- **`backend/app/core/`** - Configuración y conexión a BD
- **`frontend/src/`** - Componentes React y llamadas API
