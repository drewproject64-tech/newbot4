from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

COUNT = "🔢 Count Text"
CLEAN = "🧹 Clean Text"
CASE = "🔤 Change Case"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=COUNT)], [KeyboardButton(text=CLEAN)], [KeyboardButton(text=CASE)]],
        resize_keyboard=True,
        input_field_placeholder="Choose a text tool…",
    )
