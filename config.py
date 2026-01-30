"""
Configuration management for Discord bot.
Handles bot token loading and validation.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Bot configuration loaded from environment variables."""

    def __init__(self):
        self.bot_token = os.getenv('DISCORD_BOT_TOKEN')

        if not self.bot_token:
            raise ValueError(
                "DISCORD_BOT_TOKEN not found in environment. "
                "Please create a .env file based on .env.example"
            )

    @property
    def token(self) -> str:
        """Get the bot token."""
        return self.bot_token


# Global config instance
config = Config()
