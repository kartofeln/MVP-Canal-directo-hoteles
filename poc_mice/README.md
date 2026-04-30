# POC MICE — stack completo

Orquestación **FastAPI** + **PostgreSQL** + ingesta **DataForSEO** + brief **Claude** + **Kapso** (envío opcional y webhook).

## Requisitos

- Docker Desktop (para Postgres)
- Python 3.11+
- Cuenta **DataForSEO** (login + password API)
- (Opcional) **Anthropic** API key para `/v1/brief/generate`
- (Opcional) **Kapso** API key y número de prueba

## Paso 1 — Base de datos

**Opción A — Sin Docker (rápido):** en `.env` deja  
`DATABASE_URL=sqlite:///./mice_poc.db`  
Se crea el archivo `mice_poc.db` en `poc_mice` al arrancar la API.

**Opción B — PostgreSQL con Docker:** instala y abre **Docker Desktop**, luego:

```powershell
cd c:\Workspaces\Sector_turístico_linkedin\poc_mice
docker compose up -d
```

En `.env` usa:  
`DATABASE_URL=postgresql+psycopg2://mice:mice_dev@127.0.0.1:5433/mice_poc`  

Si ves `Connection refused` en el puerto 5433, el contenedor no está levantado o Docker no está en marcha.

## Paso 2 — Entorno Python

```powershell
cd c:\Workspaces\Sector_turístico_linkedin\poc_mice
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Paso 3 — Variables de entorno

Copia `.env.example` a `.env` y rellena al menos:

- `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`

Opcional:

- `ANTHROPIC_API_KEY`
- `KAPSO_API_KEY`, `KAPSO_TEST_TO`
- `KAPSO_WEBHOOK_SECRET` (y envía el mismo valor en header `X-Webhook-Secret` al probar el webhook)

## Paso 4 — Arrancar la API

**Opción A (recomendada en Windows):** dentro de `poc_mice` ejecuta:

```powershell
.\run_api.ps1
```

Fija solo `PYTHONPATH` y la carpeta correcta. Al arrancar, en consola debe verse **`POC MICE  build=2026-03-29c`**. Luego abre **http://127.0.0.1:8000/meta-poc**; si da **404**, sigues usando otro servidor u otro puerto.

**Opción B — manual:** desde `poc_mice` con el venv activado:

```powershell
$env:PYTHONPATH = "$PWD"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación interactiva: **http://127.0.0.1:8010/docs** si usas `run_api.ps1` (puerto **8010** por defecto).

**WinError 10013** al usar el puerto 8000: Windows u otro programa bloquea ese puerto. `run_api.ps1` usa **8010**; o manualmente: `uvicorn ... --port 8010`. Otro puerto: `$env:POC_PORT='8020'; .\run_api.ps1`

(Si abres la raíz del servidor te redirige a `/docs`.)

### Guía rápida Swagger (si no lo has usado nunca)

1. **Antes de nada:** en PowerShell debe seguir corriendo `uvicorn` y verse algo como `Uvicorn running on http://127.0.0.1:8000`. Si cerraste la ventana, vuelve al paso 4 y arranca otra vez.
2. Abre el navegador (Chrome o Edge) y escribe exactamente: **http://127.0.0.1:8000/docs** (con **http**, no https).
3. Verás una lista de secciones (**ingest**, **snapshots**, etc.). Cada línea es un endpoint.
4. Para **POST** (por ejemplo ingest): haz clic en la fila → botón **Try it out** → si pide *Request body*, escribe `{}` → **Execute**. Abajo aparece **Response** con código 200 o un error.
5. Para **descargar el CSV** sin depender del parámetro: en Swagger busca **GET** `/v1/snapshots/latest/csv` → **Try it out** → **Execute**. O pega en el navegador: **http://127.0.0.1:8000/v1/snapshots/latest/csv**
6. Si el navegador dice que **no puede conectar**, el servidor no está arrancado o el puerto no es 8000.

## Probar sin DataForSEO (demo local)

Si no obtienes filas de la API real, puedes **probar todo el flujo** (snapshots, CSV, Excel) con números **ficticios**:

1. En `poc_mice/.env` pon `POC_ALLOW_FAKE_DATA=1` y reinicia `uvicorn`.
2. En `/docs`: **POST** `/v1/ingest/demo-local` (sin cuerpo o `{}`).
3. **GET** `/v1/snapshots/latest` o abre **http://127.0.0.1:8000/csv**

**No uses esos números en LinkedIn como datos de mercado**; solo sirven para ver que el pipeline funciona.

## Paso 5 — Flujo POC

1. **Ingesta** (gasta crédito DataForSEO — 3 mercados × 1 llamada cada uno con el batch por defecto):

   `POST /v1/ingest/run`  
   Cuerpo vacío `{}` o personaliza mercados (ver esquema en `/docs`).

2. **Ver últimos datos guardados**:

   `GET /v1/snapshots/latest`

3. **Export para LinkedIn / Excel (sin API keys en el archivo)**:

   - `GET /v1/snapshots/latest?download=csv` o `?download=md` (mismo endpoint que el JSON; en Swagger verás el parámetro **download**).
   - **Atajo corto:** `GET /csv` → http://127.0.0.1:8000/csv (mismo CSV que `/v1/snapshots/latest/csv`).
   - `GET /v1/snapshots/latest/csv` y `GET /v1/snapshots/latest/md` (sin punto en la URL).
   - Por run: `GET /v1/snapshots/by-run/{run_id}/csv` y `.../md`.

   Abre la URL en el navegador con la API en marcha.

4. **Brief con Claude** (requiere `ANTHROPIC_API_KEY`):

   `POST /v1/brief/generate`  
   JSON: `{"send_whatsapp": false}`  
   Con WhatsApp: `{"send_whatsapp": true}` (requiere `KAPSO_*` configurado; el endpoint de Kapso puede requerir ajuste según tu cuenta — ver `app/services/kapso_notify.py`).

5. **Webhook Kapso** (URL pública en producción con ngrok/Cloudflare Tunnel):

   `POST /webhooks/kapso`

## Personalización

- Keywords y mercados por defecto: `app/default_mice_targets.py`
- Lógica conversacional en webhook: `app/routers/webhooks.py`

## Tablas

Creadas al arrancar (`create_all`): `ingestion_runs`, `keyword_snapshots`.

## Parar Postgres

```powershell
docker compose down
```
