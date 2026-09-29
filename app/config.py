import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    bot_token: str
    bot_name: str = "SB Luky Text bot"
    bot_username: str = "@LukyTextBot"
    about: str = "Text tools for counting, cleaning, and changing text case."
    description: str = ("SB Luky Text bot provides three simple text utilities inside Telegram: "
                        "count text, clean spacing, and change text case.")

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError("BOT_TOKEN environment variable is required.")
        return cls(bot_token=token)
