# SB Luky Text Bot

Telegram bot for @LukyTextBot with exactly three primary text tools.

## Functions

- Count Text: characters, characters without spaces, words, and lines.
- Clean Text: normalizes repeated spaces and removes empty lines.
- Change Case: upper, lower, or title case.

Everything runs inside Telegram. No external links, redirects, payments, gambling, betting, casino, prizes, or unrelated features are included.

## Setup

Python 3.12+ is recommended.

1. Install dependencies: `pip install -r requirements.txt`
2. Set the `BOT_TOKEN` environment variable.
3. Start: `python -m app.main`

## Render

Deploy as a Background Worker. The included `render.yaml` uses `pip install -r requirements.txt` and `python -m app.main`. Add `BOT_TOKEN` as a secret environment variable.

## Profile configuration

On startup the app sets the bot name, short description, description, and clears the bot command list using the Telegram Bot API where supported.

## Compliance-focused checks

Exactly 3 main buttons; all are functional; /start resets state; invalid inputs are handled; no external URLs; no redirect-only functionality; no gambling or real-money gaming features. Telegram Ads approval remains subject to Telegram review and policy.
