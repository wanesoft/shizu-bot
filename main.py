import logging
import asyncio
import sys

from bot.ai_bot import AiBot


async def main() -> None:
    bot = AiBot()
    await bot.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())