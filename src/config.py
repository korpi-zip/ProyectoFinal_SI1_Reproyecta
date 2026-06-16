import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    @classmethod
    def validate(cls):
        missing = []
        for name in dir(cls):
            if name.isupper() and not name.startswith("_"):
                value = getattr(cls, name)
                if isinstance(value, str) and not value:
                    missing.append(name)
        if missing:
            raise ValueError(
                f"Faltan variables de entorno: {', '.join(missing)}. "
                f"Revisa tu archivo .env"
            )
