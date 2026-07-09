import time
import logging

from app.monitor.search_manager import SearchManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


INTERVAL = 30 * 60  # 30 minutos



def start_scheduler():

    manager = SearchManager()


    while True:

        try:

            logging.info(
                "Iniciando busca de leilões..."
            )


            result = manager.run()


            logging.info(
                f"Busca finalizada: {result}"
            )


        except Exception as e:

            logging.error(
                f"Erro no monitor: {e}"
            )


        logging.info(
            f"Aguardando {INTERVAL/60} minutos..."
        )


        time.sleep(
            INTERVAL
        )
