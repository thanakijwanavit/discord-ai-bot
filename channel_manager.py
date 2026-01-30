"""
Channel Manager for Discord Bot
Handles dynamic channel creation and mapping for Gas Town rigs.
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict
import discord


class ChannelManager:
    """Manages Discord channel creation and rig-to-channel mappings."""

    def __init__(self, guild: discord.Guild, mappings_file: str = "channel_mappings.json"):
        """
        Initialize the ChannelManager.

        Args:
            guild: The Discord guild (server) to manage channels in
            mappings_file: Path to JSON file for storing rig -> channel ID mappings
        """
        self.guild = guild
        self.mappings_file = Path(mappings_file)
        self.mappings: Dict[str, int] = {}
        self._load_mappings()

    def _load_mappings(self) -> None:
        """Load channel mappings from JSON file."""
        if self.mappings_file.exists():
            try:
                with open(self.mappings_file, 'r') as f:
                    self.mappings = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load mappings from {self.mappings_file}: {e}")
                self.mappings = {}
        else:
            self.mappings = {}

    def _save_mappings(self) -> None:
        """Save channel mappings to JSON file."""
        try:
            with open(self.mappings_file, 'w') as f:
                json.dump(self.mappings, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save mappings to {self.mappings_file}: {e}")

    async def get_or_create_channel(self, rig_name: str) -> discord.TextChannel:
        """
        Get existing channel for a rig or create a new one.

        Args:
            rig_name: Name of the Gas Town rig (e.g., 'discord_bot', 'gastown')

        Returns:
            The Discord text channel for this rig
        """
        # Check if we have a cached mapping
        if rig_name in self.mappings:
            channel_id = self.mappings[rig_name]
            channel = self.guild.get_channel(channel_id)

            # If channel still exists, return it
            if channel and isinstance(channel, discord.TextChannel):
                return channel
            else:
                # Channel was deleted, remove from mappings
                del self.mappings[rig_name]
                self._save_mappings()

        # Search for existing channel by name
        channel_name = self._sanitize_channel_name(rig_name)
        for channel in self.guild.text_channels:
            if channel.name == channel_name:
                # Found existing channel, update mapping
                self.mappings[rig_name] = channel.id
                self._save_mappings()
                return channel

        # Channel doesn't exist, create it
        return await self._create_channel(rig_name)

    async def _create_channel(self, rig_name: str) -> discord.TextChannel:
        """
        Create a new Discord channel for a rig.

        Args:
            rig_name: Name of the Gas Town rig

        Returns:
            The newly created Discord text channel
        """
        channel_name = self._sanitize_channel_name(rig_name)

        # Create channel with topic describing its purpose
        channel = await self.guild.create_text_channel(
            name=channel_name,
            topic=f"Notifications from Gas Town rig: {rig_name}"
        )

        # Save mapping
        self.mappings[rig_name] = channel.id
        self._save_mappings()

        # Send initial message
        await channel.send(f"🚂 **Gas Town Rig Channel Created**\nThis channel receives notifications from the `{rig_name}` rig.")

        return channel

    @staticmethod
    def _sanitize_channel_name(rig_name: str) -> str:
        """
        Convert rig name to valid Discord channel name.
        Discord channel names must be lowercase, alphanumeric with hyphens/underscores.

        Args:
            rig_name: The rig name to sanitize

        Returns:
            Sanitized channel name
        """
        # Convert to lowercase
        name = rig_name.lower()

        # Replace spaces with hyphens
        name = name.replace(' ', '-')

        # Remove invalid characters (keep alphanumeric, hyphens, underscores)
        name = ''.join(c for c in name if c.isalnum() or c in '-_')

        # Prefix with 'gt-' to indicate Gas Town origin
        return f"gt-{name}"

    def get_channel_id(self, rig_name: str) -> Optional[int]:
        """
        Get the Discord channel ID for a rig without creating a channel.

        Args:
            rig_name: Name of the Gas Town rig

        Returns:
            Channel ID if mapping exists, None otherwise
        """
        return self.mappings.get(rig_name)

    def list_mappings(self) -> Dict[str, int]:
        """
        Get all rig -> channel ID mappings.

        Returns:
            Dictionary of rig names to channel IDs
        """
        return self.mappings.copy()

    async def delete_channel(self, rig_name: str) -> bool:
        """
        Delete a channel for a rig.

        Args:
            rig_name: Name of the Gas Town rig

        Returns:
            True if channel was deleted, False if it didn't exist
        """
        if rig_name not in self.mappings:
            return False

        channel_id = self.mappings[rig_name]
        channel = self.guild.get_channel(channel_id)

        if channel:
            await channel.delete()

        # Remove from mappings
        del self.mappings[rig_name]
        self._save_mappings()

        return True
