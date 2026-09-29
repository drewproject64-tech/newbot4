import asyncio
import logging
import re
from html import escape

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from .config import Settings
from .keyboards import CASE, CLEAN, COUNT, main_menu

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
router = Router()

class TextMode(StatesGroup):
    count = State()
    clean = State()
    case = State()

WELCOME = (
    "<b>Welcome to SB Luky Text bot</b>!\n\n"
    "Use one of the three text tools below:\n\n"
    "🔢 Count Text — count characters, words, and lines.\n"
    "🧹 Clean Text — normalize spacing and remove blank lines.\n"
    "🔤 Change Case — convert text to upper, lower, or title case.\n\n"
    "Send /start anytime to return to the main menu."
)

async def configure_bot(bot: Bot, settings: Settings) -> None:
    await bot.set_my_name(name=settings.bot_name)
    await bot.set_my_short_description(short_description=settings.about[:120])
    await bot.set_my_description(description=settings.description[:512])
    await bot.set_my_commands([])

@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME, reply_markup=main_menu())

@router.message(F.text == COUNT)
async def count_prompt(message: Message, state: FSMContext) -> None:
    await state.set_state(TextMode.count)
    await message.answer("Send the text you want to count.")

@router.message(TextMode.count)
async def count_text(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Please send text as a normal text message.")
        return
    value = message.text
    words = re.findall(r"\S+", value, flags=re.UNICODE)
    lines = value.count("\n") + 1
    non_space = sum(not ch.isspace() for ch in value)
    await state.clear()
    await message.answer(
        "<b>Text count</b>\n\n"
        f"Characters: <b>{len(value)}</b>\n"
        f"Characters without spaces: <b>{non_space}</b>\n"
        f"Words: <b>{len(words)}</b>\n"
        f"Lines: <b>{lines}</b>"
    )

@router.message(F.text == CLEAN)
async def clean_prompt(message: Message, state: FSMContext) -> None:
    await state.set_state(TextMode.clean)
    await message.answer("Send the text you want to clean. Repeated spaces and blank lines will be removed.")

@router.message(TextMode.clean)
async def clean_text(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Please send text as a normal text message.")
        return
    lines = []
    for line in message.text.splitlines():
        normalized = re.sub(r"[ \t]+", " ", line).strip()
        if normalized:
            lines.append(normalized)
    result = "\n".join(lines)
    await state.clear()
    if not result:
        await message.answer("No usable text was found. Please send some text and try again.")
        return
    await message.answer(f"<b>Cleaned text</b>\n\n<code>{escape(result)}</code>")

@router.message(F.text == CASE)
async def case_prompt(message: Message, state: FSMContext) -> None:
    await state.set_state(TextMode.case)
    await message.answer(
        "Send your text using one of these formats:\n\n"
        "<code>upper | your text</code>\n"
        "<code>lower | your text</code>\n"
        "<code>title | your text</code>"
    )

@router.message(TextMode.case)
async def change_case(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Please send text as a normal text message.")
        return
    raw = message.text.strip()
    if "|" not in raw:
        await message.answer("Use <code>upper | text</code>, <code>lower | text</code>, or <code>title | text</code>.")
        return
    mode, value = (part.strip() for part in raw.split("|", 1))
    mode = mode.lower()
    if mode not in {"upper", "lower", "title"} or not value:
        await message.answer("Use <code>upper | text</code>, <code>lower | text</code>, or <code>title | text</code>.")
        return
    result = {"upper": value.upper(), "lower": value.lower(), "title": value.title()}[mode]
    await state.clear()
    await message.answer(f"<b>{mode.title()} case</b>\n\n<code>{escape(result)}</code>")

@router.message()
async def fallback(message: Message, state: FSMContext) -> None:
    if await state.get_state():
        await message.answer("Please send the text requested by the selected tool, or send /start to reset.")
    else:
        await message.answer("Please choose one of the three text tools below, or send /start.", reply_markup=main_menu())

async def main() -> None:
    settings = Settings.from_env()
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    try:
        await configure_bot(bot, settings)
        me = await bot.get_me()
        logging.info("Started @%s", me.username)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
