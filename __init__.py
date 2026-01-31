"""
<<<<<<< HEAD
Gas Town Discord Bot - Channel Management Module
Provides utilities for managing Discord channels per Gas Town rig.
"""
from .channel_manager import ChannelManager

__all__ = ['ChannelManager']
__version__ = '0.1.0'
=======
Gas Town Discord Notification Formatter

Message formatting module for Gas Town events -> Discord embeds.
Used by discord_bot/crew/core for MCP server implementation.
"""

from .formatter import (
    NotificationFormatter,
    EventType,
    format_event,
)

__all__ = [
    "NotificationFormatter",
    "EventType",
    "format_event",
]

__version__ = "0.1.0"
>>>>>>> a68194b (Add notification formatter module with Discord embed support)
