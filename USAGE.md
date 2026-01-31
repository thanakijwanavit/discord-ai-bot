# Gas Town Notification Formatter Usage

Message formatting module for Gas Town events → Discord embeds.

## Overview

This module provides `NotificationFormatter` class that converts Gas Town events (nudge, broadcast, convoy updates, escalations) into Discord embed objects for the core crew's MCP server.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from formatter import NotificationFormatter, format_event

# Option 1: Use the formatter class
formatter = NotificationFormatter()
embed = formatter.format_nudge(
    from_agent="discord_bot/crew/notify",
    to_agent="discord_bot/crew/core",
    message="Check your hook",
    rig="discord_bot"
)

# Option 2: Use the convenience function
embed = format_event(
    "nudge",
    from_agent="discord_bot/crew/notify",
    to_agent="mayor/",
    message="Status update",
    rig="discord_bot"
)
```

## Supported Event Types

- Nudge (💬) - Direct messages between agents
- Broadcast (📢) - Town-wide or rig-wide broadcasts
- Mail (📧) - Async messages with subjects
- Convoy Updates (🚚) - Batch work progress tracking
- Escalations (🚨) - Critical issues requiring attention
- Handoff (🤝) - Context cycling between sessions
- Completion (✅) - Work completion notifications

## Color Scheme

| Event Type | Color | Hex Code |
|------------|-------|----------|
| Nudge | Discord Blurple | #5865F2 |
| Broadcast | Yellow | #FEE75C |
| Mail | Green | #57F287 |
| Convoy Update | Pink | #EB459E |
| Escalation | Red | #ED4245 |
| Handoff | Dark Green | #3BA55D |
| Completion | Green | #57F287 |

## Integration with Core

The core crew's MCP server should import and use the formatter:

```python
from notify.formatter import NotificationFormatter, format_event

formatter = NotificationFormatter()
embed = format_event("nudge", from_agent="...", to_agent="...", message="...")
await channel.send(embed=discord.Embed.from_dict(embed))
```

See `examples.py` for working examples of all event types.
