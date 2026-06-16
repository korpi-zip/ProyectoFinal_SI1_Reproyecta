# ReProyecta

Plataforma inteligente para gestión, reutilización y aprovechamiento de recursos de proyectos anteriores.

## Arquitectura

```
Usuario → Telegram → LangChain Agent → Tools → PostgreSQL → Respuesta
```

## Stack

- **Frontend**: Telegram Bot (`python-telegram-bot`)
- **Backend**: Python + LangChain Agent
- **Modelo**: Gemini 2.0 Flash (`langchain-google-genai`)
- **Base de datos**: PostgreSQL vía Supabase

## Requisitos

- Python 3.10+
- Cuenta en Supabase (base de datos con tablas creadas)
- API key de Gemini (desde https://aistudio.google.com/app/apikey)
- Token de bot de Telegram (desde https://t.me/botfather)

## Instalación

```powershell
git clone <repo>
cd ReProyecta_LangChain
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Crear archivo `.env`:

```
TELEGRAM_BOT_TOKEN=tu_token
SUPABASE_URL=https://tu_proyecto.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
GEMINI_API_KEY=tu_gemini_api_key
```

Las tablas de base de datos deben existir en Supabase (ver `schema.sql` como referencia).

## Ejecución

```powershell
python -m src.main
```

## Estructura

```
src/
├── main.py                 # Entry point
├── config.py               # Variables de entorno
├── database/
│   ├── connection.py       # Cliente Supabase
│   └── queries.py          # CRUD
├── agent/
│   ├── prompts.py          # System prompt
│   ├── tools.py            # 5 herramientas LangChain
│   ├── memory.py           # Memoria persistente PostgreSQL
│   └── agent.py            # Inicialización del agente
└── bot/
    └── telegram_bot.py     # Handlers de Telegram
```

## Herramientas del agente

| Herramienta | Descripción |
|---|---|
| Buscar Recurso | Busca por nombre en inventario |
| Consultar Inventario | Lista todos los recursos (filtro por categoría) |
| Registrar Recurso | Inserta nuevo recurso con nombre, cantidad, categoría, estado, ubicación, unidad |
| Buscar Recursos Relacionados | Filtra por categoría |
| Consultar Proyectos Anteriores | Lista proyectos registrados |

## Casos de uso

```
Usuario: "Guardar 10 motores DC"
Agente:   Registra el recurso en la base de datos.

Usuario: "¿Cuántos motores tenemos?"
Agente:   Consulta PostgreSQL y responde con datos reales.

Usuario: "Quiero construir un brazo robótico"
Agente:   Revisa inventario y sugiere reutilizar recursos existentes.
```
