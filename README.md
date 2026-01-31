# Gas Town Discord Notification Formatter

Message formatting module for Gas Town events → Discord embeds.

## Purpose

This module provides the `NotificationFormatter` class that converts Gas Town events (nudge, broadcast, convoy updates, escalations) into Discord embed objects for the MCP server.

**Division of responsibility:**
- **This module (notify):** Message formatting only
- **Core crew:** MCP server implementation and Discord bot integration

## Quick Start

```python
from notify import NotificationFormatter, format_event

# Format a nudge event
embed = format_event(
    "nudge",
    from_agent="discord_bot/crew/notify",
    to_agent="mayor/",
    message="Status update",
    rig="discord_bot"
)

# Send to Discord (handled by core crew)
```

## Supported Event Types

- **Nudge:** Direct agent-to-agent messages
- **Broadcast:** Town-wide or rig-wide announcements
- **Mail:** Async messages with subjects
- **Convoy Updates:** Batch work progress tracking
- **Escalations:** Critical issues requiring attention
- **Handoffs:** Context cycling between sessions
- **Completions:** Work completion notifications
- **Generic:** Fallback for custom events

## Documentation

- `USAGE.md` - Comprehensive usage guide
- `examples.py` - Working examples for all event types
- `formatter.py` - Core implementation

## Testing

```bash
python3 examples.py
```

