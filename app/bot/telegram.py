import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
)

from app.bot.handlers import (
    search_command,
    start_command,
    status_command,
)
from app.config import TELEGRAM_TOKEN


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)


def create_application() -> Application:
    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "status",
            status_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "search",
            search_command,
        )
    )

    return application


def start_bot() -> None:
    application = create_application()

    logging.info(
        "Bot do Telegram iniciado."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    start_bot()
