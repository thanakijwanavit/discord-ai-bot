"""
Discord Bot MCP Server for Gas Town notifications.

This MCP server exposes a 'send_discord_message' tool that allows Gas Town agents
to send notifications to the seer through Discord. Messages are routed to channels
based on project/rig.
"""

import discord
import logging
import sys
import asyncio
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('discord_bot')


class DiscordClient:
    """Discord client for sending messages."""

    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.messages = True

        self.client = discord.Client(intents=intents)
        self.ready = asyncio.Event()

        # Register event handlers
        @self.client.event
        async def on_ready():
            logger.info(f'Discord client connected as {self.client.user} (ID: {self.client.user.id})')
            logger.info(f'Connected to {len(self.client.guilds)} guilds')
            self.ready.set()

        @self.client.event
        async def on_error(event_method: str, *args, **kwargs):
            logger.error(f'Discord error in {event_method}', exc_info=True)

    async def start(self):
        """Start the Discord client."""
        await self.client.start(config.token)

    async def wait_until_ready(self):
        """Wait until the Discord client is ready."""
        await self.ready.wait()

    async def send_message(self, channel_name: str, message: str, rig_name: Optional[str] = None) -> str:
        """
        Send a message to a Discord channel.

        Args:
            channel_name: Name of the channel to send to
            message: Message content to send
            rig_name: Optional rig name for channel routing

        Returns:
            Success message with channel info
        """
        await self.wait_until_ready()

        # Find the channel by name
        channel = None
        for guild in self.client.guilds:
            for ch in guild.channels:
                if isinstance(ch, discord.TextChannel) and ch.name == channel_name:
                    channel = ch
                    break
            if channel:
                break

        if not channel:
            raise ValueError(f"Channel '{channel_name}' not found")

        # Prepare message with rig prefix if provided
        full_message = message
        if rig_name:
            full_message = f"[{rig_name}] {message}"

        # Send the message
        await channel.send(full_message)
        logger.info(f"Sent message to #{channel_name} in {channel.guild.name}")

        return f"Message sent to #{channel_name}"


# Global Discord client instance
discord_client = DiscordClient()


async def main():
    """Main entry point - runs both MCP server and Discord client."""

    # Create MCP server
    server = Server("discord-bot")

    # Define the send_discord_message tool
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="send_discord_message",
                description="Send a notification message to a Discord channel. Use this to notify the seer about Gas Town events, agent updates, or important information.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel_name": {
                            "type": "string",
                            "description": "Name of the Discord channel to send to (without #)"
                        },
                        "message": {
                            "type": "string",
                            "description": "The message content to send"
                        },
                        "rig_name": {
                            "type": "string",
                            "description": "Optional rig name to prefix the message (e.g., 'discord_bot', 'gastown')"
                        }
                    },
                    "required": ["channel_name", "message"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name != "send_discord_message":
            raise ValueError(f"Unknown tool: {name}")

        channel_name = arguments.get("channel_name")
        message = arguments.get("message")
        rig_name = arguments.get("rig_name")

        if not channel_name or not message:
            raise ValueError("channel_name and message are required")

        try:
            result = await discord_client.send_message(channel_name, message, rig_name)
            return [TextContent(type="text", text=result)]
        except Exception as e:
            error_msg = f"Failed to send message: {str(e)}"
            logger.error(error_msg)
            return [TextContent(type="text", text=error_msg)]

    # Start Discord client in background
    discord_task = asyncio.create_task(discord_client.start())

    try:
        # Run MCP server with stdio transport
        logger.info("Starting MCP server on stdio...")
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"MCP server error: {e}", exc_info=True)
    finally:
        # Clean shutdown
        discord_task.cancel()
        try:
            await discord_task
        except asyncio.CancelledError:
            pass


if __name__ == '__main__':
    asyncio.run(main())
