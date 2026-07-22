import asyncio
import logging
import time
from typing import Any

from app.config import SCRAPE_INTERVAL_MINUTES
from app.monitor.search_manager import SearchManager
from app.notifications import TelegramNotifier


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = SCRAPE_INTERVAL_MINUTES * 60


def log_run_result(
    result: dict[str, Any],
    alerts_sent: int,
) -> None:
    logger.info(
        (
            "Busca concluída | "
            "pesquisas=%s | "
            "keywords=%s | "
            "encontrados=%s | "
            "aceitos=%s | "
            "ignorados=%s | "
            "novos=%s | "
            "atualizados=%s | "
            "inalterados=%s | "
            "históricos=%s | "
            "alertas=%s"
        ),
        result["searches_processed"],
        result["keywords_processed"],
        result["found"],
        result["accepted"],
        result["ignored"],
        result["inserted"],
        result["updated"],
        result["unchanged"],
        result["price_history_created"],
        alerts_sent,
    )


def run_cycle(
    manager: SearchManager,
    notifier: TelegramNotifier,
) -> None:
    logger.info(
        "Iniciando busca de anúncios."
    )

    result = manager.run()

    alerts_sent = asyncio.run(
        notifier.send_run_events(result)
    )

    log_run_result(
        result=result,
        alerts_sent=alerts_sent,
    )


def start_scheduler() -> None:
    manager = SearchManager()
    notifier = TelegramNotifier()

    logger.info(
        "Scheduler iniciado com intervalo de %s minutos.",
        SCRAPE_INTERVAL_MINUTES,
    )

    try:
        while True:
            try:
                run_cycle(
                    manager=manager,
                    notifier=notifier,
                )
            except Exception:
                logger.exception(
                    "Erro durante o ciclo do monitor."
                )

            logger.info(
                "Aguardando %s minutos até a próxima busca.",
                SCRAPE_INTERVAL_MINUTES,
            )

            time.sleep(
                INTERVAL_SECONDS
            )
    except KeyboardInterrupt:
        logger.info(
            "Scheduler interrompido pelo usuário."
        )


if __name__ == "__main__":
    start_scheduler()
