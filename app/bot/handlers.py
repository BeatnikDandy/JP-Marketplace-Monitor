import asyncio
import html
import logging
from typing import Any

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.monitor.search_manager import SearchManager


logger = logging.getLogger(__name__)

manager = SearchManager()


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    await update.message.reply_text(
        "🤖 JP Marketplace Monitor\n\n"
        "Comandos disponíveis:\n"
        "/search <termo> — pesquisar no Yahoo Auctions\n"
        "/status — verificar o funcionamento do bot"
    )


async def status_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    await update.message.reply_text(
        "✅ Bot ativo.\n"
        "Marketplace disponível: Yahoo Auctions Japan."
    )


async def search_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    keyword = " ".join(context.args).strip()

    if not keyword:
        await update.message.reply_text(
            "Use o comando neste formato:\n"
            "/search オメガ デビル"
        )
        return

    status_message = await update.message.reply_text(
        f"🔎 Pesquisando por: {keyword}"
    )

    try:
        items = await asyncio.to_thread(
            manager.search_now,
            keyword,
        )
    except Exception:
        logger.exception(
            "Erro ao pesquisar por %s",
            keyword,
        )

        await status_message.edit_text(
            "❌ Não foi possível concluir a pesquisa."
        )
        return

    if not items:
        await status_message.edit_text(
            f"Não encontrei resultados válidos para:\n{keyword}"
        )
        return

    await status_message.edit_text(
        f"✅ Encontrei {len(items)} resultados.\n"
        "Exibindo os primeiros 5:"
    )

    for position, item in enumerate(
        items[:5],
        start=1,
    ):
        message = format_listing(
            position=position,
            item=item,
        )

        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )


def format_listing(
    position: int,
    item: dict[str, Any],
) -> str:
    title = html.escape(
        str(item.get("title") or "Sem título")
    )

    url = html.escape(
        str(item.get("url") or "")
    )

    price = format_price(
        item.get("price")
    )

    lines = [
        f"<b>{position}. {title}</b>",
        f"💴 {price}",
    ]

    if url:
        lines.append(
            f'🔗 <a href="{url}">Abrir anúncio</a>'
        )

    return "\n".join(lines)


def format_price(value: Any) -> str:
    if value is None:
        return "Preço não informado"

    try:
        numeric_value = int(value)
    except (TypeError, ValueError):
        return html.escape(str(value))

    return f"¥{numeric_value:,}".replace(",", ".")
