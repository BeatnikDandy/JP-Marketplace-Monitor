import os


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()

if not TELEGRAM_TOKEN:
    raise RuntimeError(
        "A variável de ambiente TELEGRAM_TOKEN não foi definida."
    )
