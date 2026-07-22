import os

from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    "",
).strip()

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    "",
).strip()

SCRAPE_INTERVAL_MINUTES = int(
    os.getenv(
        "SCRAPE_INTERVAL_MINUTES",
        "30",
    )
)


if not TELEGRAM_TOKEN:
    raise RuntimeError(
        "A variável de ambiente TELEGRAM_TOKEN "
        "não foi definida."
    )

if not TELEGRAM_CHAT_ID:
    raise RuntimeError(
        "A variável de ambiente TELEGRAM_CHAT_ID "
        "não foi definida."
    )

if SCRAPE_INTERVAL_MINUTES <= 0:
    raise RuntimeError(
        "SCRAPE_INTERVAL_MINUTES deve ser maior que zero."
    )
