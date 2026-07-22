import html
from typing import Any

from telegram import Bot
from telegram.constants import ParseMode

from app.config import (
    TELEGRAM_CHAT_ID,
    TELEGRAM_TOKEN,
)
from app.domain import Listing


class TelegramNotifier:
    """Envia alertas automáticos pelo Telegram."""

    def __init__(
        self,
        token: str = TELEGRAM_TOKEN,
        chat_id: str = TELEGRAM_CHAT_ID,
    ) -> None:
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_run_events(
        self,
        result: dict[str, Any],
    ) -> int:
        sent = 0

        for event in result.get(
            "new_listings",
            [],
        ):
            await self.send_new_listing(
                search_name=event["search_name"],
                keyword=event["keyword"],
                listing=event["listing"],
            )

            sent += 1

        for event in result.get(
            "price_drops",
            [],
        ):
            await self.send_price_drop(
                search_name=event["search_name"],
                keyword=event["keyword"],
                listing=event["listing"],
                previous_price=event[
                    "previous_price"
                ],
            )

            sent += 1

        return sent

    async def send_new_listing(
        self,
        search_name: str,
        keyword: str,
        listing: Listing,
    ) -> None:
        title = html.escape(listing.title)
        search = html.escape(search_name)
        keyword_text = html.escape(keyword)
        url = html.escape(
            listing.url,
            quote=True,
        )

        message = "\n".join(
            [
                "🆕 <b>Novo anúncio</b>",
                "",
                f"<b>Pesquisa:</b> {search}",
                f"<b>Termo:</b> {keyword_text}",
                "",
                f"<b>{title}</b>",
                f"💴 {self.format_price(listing.price)}",
                "",
                (
                    f'🔗 <a href="{url}">'
                    "Abrir anúncio"
                    "</a>"
                ),
            ]
        )

        await self._send(message)

    async def send_price_drop(
        self,
        search_name: str,
        keyword: str,
        listing: Listing,
        previous_price: int,
    ) -> None:
        title = html.escape(listing.title)
        search = html.escape(search_name)
        keyword_text = html.escape(keyword)
        url = html.escape(
            listing.url,
            quote=True,
        )

        percentage = self.calculate_percentage_drop(
            previous_price=previous_price,
            current_price=listing.price,
        )

        message = "\n".join(
            [
                "📉 <b>Queda de preço</b>",
                "",
                f"<b>Pesquisa:</b> {search}",
                f"<b>Termo:</b> {keyword_text}",
                "",
                f"<b>{title}</b>",
                (
                    "<b>Preço anterior:</b> "
                    f"{self.format_price(previous_price)}"
                ),
                (
                    "<b>Preço atual:</b> "
                    f"{self.format_price(listing.price)}"
                ),
                f"<b>Queda:</b> {percentage:.1f}%",
                "",
                (
                    f'🔗 <a href="{url}">'
                    "Abrir anúncio"
                    "</a>"
                ),
            ]
        )

        await self._send(message)

    async def _send(
        self,
        message: str,
    ) -> None:
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    @staticmethod
    def format_price(
        price: int,
    ) -> str:
        formatted = f"{price:,}".replace(
            ",",
            ".",
        )

        return f"¥{formatted}"

    @staticmethod
    def calculate_percentage_drop(
        previous_price: int,
        current_price: int,
    ) -> float:
        if previous_price <= 0:
            return 0.0

        return (
            (previous_price - current_price)
            / previous_price
            * 100
        )
