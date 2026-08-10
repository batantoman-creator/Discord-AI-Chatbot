import os
from typing import Optional, Any

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import COMMANDS, EVENT_HANDLERS
from bot_utilities.config_loader import config

load_dotenv()

class AIBot(commands.AutoShardedBot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if config['AUTO_SHARDING']:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(shard_count=1, *args, **kwargs)

    async def setup_hook(self) -> None:
        for cog in COMMANDS:
            cog_name = cog.split('.')[-1]
            print(f'Loaded Command {cog_name}')
            await self.load_extension(f'{cog}')
        for cog in EVENT_HANDLERS:
            cog_name = cog.split('.')[-1]
            print(f'Loaded Event Handler {cog_name}')
            await self.load_extension(f'{cog}')
        print('If syncing commands is taking longer than usual you are being ratelimited')
        await self.tree.sync()
        print(f'Loaded {len(self.commands)} commands')

bot = AIBot(command_prefix=[], intents=discord.Intents.all(), help_command=None)

# Lấy trực tiếp token từ biến môi trường của Railway, không dùng input() để tránh crash
TOKEN = os.getenv('DISCORD_TOKEN') or os.environ.get('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("LỖI: Chưa cấu hình biến DISCORD_TOKEN trong phần Variables của Railway!")

bot.run(TOKEN, reconnect=True)
