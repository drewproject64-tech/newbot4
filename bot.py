"""Compatibility entry point for Render deployments still using 'python bot.py'.
The production application lives in app.main.
"""
from app.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
