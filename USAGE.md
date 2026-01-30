# Channel Manager Usage Guide

The `ChannelManager` class provides channel management utilities for the Discord bot.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import discord
from channel_manager import ChannelManager

# Initialize with your Discord guild
guild = client.get_guild(guild_id)
channel_manager = ChannelManager(guild)

# Get or create a channel for a Gas Town rig
channel = await channel_manager.get_or_create_channel("discord_bot")

# Send a message to that channel
await channel.send("Hello from Gas Town!")

# List all rig -> channel mappings
mappings = channel_manager.list_mappings()
print(mappings)  # {'discord_bot': 123456789, 'gastown': 987654321}

# Get channel ID without creating
channel_id = channel_manager.get_channel_id("discord_bot")

# Delete a channel
deleted = await channel_manager.delete_channel("old_rig")
```

## Integration with MCP Server

The core bot can use ChannelManager in the MCP `send_discord_message` tool:

```python
from mcp.server import Server
from channel_manager import ChannelManager

@server.tool()
async def send_discord_message(rig_name: str, message: str):
    """Send a message to the Discord channel for a specific rig."""
    channel = await channel_manager.get_or_create_channel(rig_name)
    await channel.send(message)
    return f"Message sent to {rig_name} channel"
```

## Channel Naming

Channels are automatically named with the `gt-` prefix and sanitized:
- `discord_bot` → `gt-discord-bot`
- `gastown` → `gt-gastown`
- `My Project` → `gt-my-project`

## Persistence

Channel mappings are stored in `channel_mappings.json` (gitignored). The file persists across bot restarts and is automatically managed by the ChannelManager.

## API Reference

### `ChannelManager(guild, mappings_file='channel_mappings.json')`
Initialize the manager with a Discord guild.

### `async get_or_create_channel(rig_name: str) -> discord.TextChannel`
Get existing channel or create new one for a rig. Automatically updates mappings.

### `get_channel_id(rig_name: str) -> Optional[int]`
Get channel ID for a rig without creating a channel.

### `list_mappings() -> Dict[str, int]`
Get all rig name to channel ID mappings.

### `async delete_channel(rig_name: str) -> bool`
Delete a channel and remove its mapping. Returns True if deleted.
