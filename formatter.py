"""
Gas Town Notification Formatter

Formats Gas Town events (nudge, broadcast, convoy updates, escalations)
into Discord embeds for the core crew's MCP server.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class EventType(Enum):
    """Gas Town event types"""
    NUDGE = "nudge"
    BROADCAST = "broadcast"
    MAIL = "mail"
    CONVOY_UPDATE = "convoy_update"
    ESCALATION = "escalation"
    HANDOFF = "handoff"
    COMPLETION = "completion"


class NotificationFormatter:
    """
    Formats Gas Town events into Discord embed objects.

    Usage:
        formatter = NotificationFormatter()
        embed = formatter.format_nudge(
            from_agent="discord_bot/crew/notify",
            to_agent="discord_bot/crew/core",
            message="Check your hook",
            rig="discord_bot"
        )
    """

    # Color scheme for different event types
    COLORS = {
        EventType.NUDGE: 0x5865F2,          # Discord Blurple
        EventType.BROADCAST: 0xFEE75C,      # Yellow
        EventType.MAIL: 0x57F287,           # Green
        EventType.CONVOY_UPDATE: 0xEB459E,  # Pink
        EventType.ESCALATION: 0xED4245,     # Red
        EventType.HANDOFF: 0x3BA55D,        # Dark Green
        EventType.COMPLETION: 0x57F287,     # Green
    }

    def format_nudge(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        rig: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format a nudge event.

        Args:
            from_agent: Source agent (e.g., "discord_bot/crew/notify")
            to_agent: Target agent (e.g., "discord_bot/crew/core")
            message: Nudge message content
            rig: Optional rig name for routing
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        embed = {
            "title": "💬 Agent Nudge",
            "description": message,
            "color": self.COLORS[EventType.NUDGE],
            "fields": [
                {"name": "From", "value": f"`{from_agent}`", "inline": True},
                {"name": "To", "value": f"`{to_agent}`", "inline": True},
            ],
            "timestamp": timestamp.isoformat(),
            "footer": {"text": f"Rig: {rig}" if rig else "Gas Town"}
        }

        return embed

    def format_broadcast(
        self,
        from_agent: str,
        message: str,
        rig: Optional[str] = None,
        target_scope: str = "workers",
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format a broadcast event.

        Args:
            from_agent: Broadcasting agent
            message: Broadcast message
            rig: Optional rig filter
            target_scope: "workers", "all", or specific rig
            timestamp: Optional timestamp

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        scope_display = {
            "workers": "All Workers",
            "all": "All Agents (including infrastructure)",
        }.get(target_scope, target_scope)

        embed = {
            "title": "📢 Broadcast",
            "description": message,
            "color": self.COLORS[EventType.BROADCAST],
            "fields": [
                {"name": "From", "value": f"`{from_agent}`", "inline": True},
                {"name": "Scope", "value": scope_display, "inline": True},
            ],
            "timestamp": timestamp.isoformat(),
            "footer": {"text": f"Rig: {rig}" if rig else "Town-wide"}
        }

        return embed

    def format_mail(
        self,
        from_agent: str,
        to_agent: str,
        subject: str,
        message: str,
        mail_id: Optional[str] = None,
        priority: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format a mail event.

        Args:
            from_agent: Sender
            to_agent: Recipient
            subject: Mail subject
            message: Mail body
            mail_id: Optional bead ID
            priority: Optional priority level
            timestamp: Optional timestamp

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        fields = [
            {"name": "From", "value": f"`{from_agent}`", "inline": True},
            {"name": "To", "value": f"`{to_agent}`", "inline": True},
        ]

        if priority:
            fields.append({"name": "Priority", "value": priority, "inline": True})

        if mail_id:
            fields.append({"name": "Mail ID", "value": f"`{mail_id}`", "inline": False})

        embed = {
            "title": f"📧 {subject}",
            "description": message[:4096] if len(message) > 4096 else message,
            "color": self.COLORS[EventType.MAIL],
            "fields": fields,
            "timestamp": timestamp.isoformat(),
        }

        return embed

    def format_convoy_update(
        self,
        convoy_id: str,
        convoy_name: str,
        status: str,
        message: str,
        completed: Optional[int] = None,
        total: Optional[int] = None,
        rig: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format a convoy update event.

        Args:
            convoy_id: Convoy bead ID
            convoy_name: Convoy title/name
            status: Status update
            message: Update details
            completed: Optional completed task count
            total: Optional total task count
            rig: Optional rig name
            timestamp: Optional timestamp

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        fields = [
            {"name": "Convoy ID", "value": f"`{convoy_id}`", "inline": True},
            {"name": "Status", "value": status, "inline": True},
        ]

        if completed is not None and total is not None:
            progress = f"{completed}/{total}"
            percentage = int((completed / total) * 100) if total > 0 else 0
            progress_bar = self._create_progress_bar(percentage)
            fields.append({
                "name": "Progress",
                "value": f"{progress_bar} {progress} ({percentage}%)",
                "inline": False
            })

        embed = {
            "title": f"🚚 Convoy: {convoy_name}",
            "description": message,
            "color": self.COLORS[EventType.CONVOY_UPDATE],
            "fields": fields,
            "timestamp": timestamp.isoformat(),
            "footer": {"text": f"Rig: {rig}" if rig else "Gas Town"}
        }

        return embed

    def format_escalation(
        self,
        from_agent: str,
        issue: str,
        severity: str,
        details: str,
        bead_id: Optional[str] = None,
        rig: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format an escalation event.

        Args:
            from_agent: Escalating agent
            issue: Issue summary
            severity: Severity level (low, medium, high, critical)
            details: Detailed description
            bead_id: Optional related bead ID
            rig: Optional rig name
            timestamp: Optional timestamp

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        severity_emoji = {
            "low": "ℹ️",
            "medium": "⚠️",
            "high": "🔴",
            "critical": "🚨"
        }.get(severity.lower(), "⚠️")

        fields = [
            {"name": "From", "value": f"`{from_agent}`", "inline": True},
            {"name": "Severity", "value": f"{severity_emoji} {severity.upper()}", "inline": True},
        ]

        if bead_id:
            fields.append({"name": "Related Bead", "value": f"`{bead_id}`", "inline": False})

        embed = {
            "title": f"🚨 Escalation: {issue}",
            "description": details[:4096] if len(details) > 4096 else details,
            "color": self.COLORS[EventType.ESCALATION],
            "fields": fields,
            "timestamp": timestamp.isoformat(),
            "footer": {"text": f"Rig: {rig}" if rig else "Gas Town"}
        }

        return embed

    def format_handoff(
        self,
        from_agent: str,
        subject: str,
        message: str,
        hooked_work: Optional[str] = None,
        rig: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format a handoff event.

        Args:
            from_agent: Agent handing off
            subject: Handoff subject
            message: Handoff context/notes
            hooked_work: Optional hooked bead/molecule ID
            rig: Optional rig name
            timestamp: Optional timestamp

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        fields = [
            {"name": "From", "value": f"`{from_agent}`", "inline": True},
        ]

        if hooked_work:
            fields.append({"name": "Hooked Work", "value": f"`{hooked_work}`", "inline": True})

        embed = {
            "title": f"🤝 Handoff: {subject}",
            "description": message[:4096] if len(message) > 4096 else message,
            "color": self.COLORS[EventType.HANDOFF],
            "fields": fields,
            "timestamp": timestamp.isoformat(),
            "footer": {"text": f"Rig: {rig}" if rig else "Gas Town"}
        }

        return embed

    def format_completion(
        self,
        agent: str,
        bead_id: str,
        bead_title: str,
        summary: str,
        rig: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format a work completion event.

        Args:
            agent: Completing agent
            bead_id: Completed bead ID
            bead_title: Bead title
            summary: Completion summary
            rig: Optional rig name
            timestamp: Optional timestamp

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        embed = {
            "title": f"✅ Completed: {bead_title}",
            "description": summary,
            "color": self.COLORS[EventType.COMPLETION],
            "fields": [
                {"name": "Agent", "value": f"`{agent}`", "inline": True},
                {"name": "Bead ID", "value": f"`{bead_id}`", "inline": True},
            ],
            "timestamp": timestamp.isoformat(),
            "footer": {"text": f"Rig: {rig}" if rig else "Gas Town"}
        }

        return embed

    def format_generic(
        self,
        title: str,
        message: str,
        event_type: EventType = EventType.NUDGE,
        fields: Optional[List[Dict[str, Any]]] = None,
        rig: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Format a generic event (fallback).

        Args:
            title: Notification title
            message: Notification message
            event_type: Event type for color coding
            fields: Optional additional fields
            rig: Optional rig name
            timestamp: Optional timestamp

        Returns:
            Discord embed dict
        """
        timestamp = timestamp or datetime.utcnow()

        embed = {
            "title": title,
            "description": message,
            "color": self.COLORS.get(event_type, 0x5865F2),
            "timestamp": timestamp.isoformat(),
        }

        if fields:
            embed["fields"] = fields

        if rig:
            embed["footer"] = {"text": f"Rig: {rig}"}

        return embed

    @staticmethod
    def _create_progress_bar(percentage: int, length: int = 10) -> str:
        """
        Create a text-based progress bar.

        Args:
            percentage: Progress percentage (0-100)
            length: Bar length in characters

        Returns:
            Progress bar string
        """
        filled = int((percentage / 100) * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"


# Convenience function for quick formatting
def format_event(event_type: str, **kwargs) -> Dict[str, Any]:
    """
    Convenience function to format an event by type.

    Args:
        event_type: Event type string (nudge, broadcast, mail, etc.)
        **kwargs: Event-specific parameters

    Returns:
        Discord embed dict

    Example:
        embed = format_event(
            "nudge",
            from_agent="discord_bot/crew/notify",
            to_agent="mayor/",
            message="Status update",
            rig="discord_bot"
        )
    """
    formatter = NotificationFormatter()

    formatters = {
        "nudge": formatter.format_nudge,
        "broadcast": formatter.format_broadcast,
        "mail": formatter.format_mail,
        "convoy_update": formatter.format_convoy_update,
        "convoy": formatter.format_convoy_update,  # alias
        "escalation": formatter.format_escalation,
        "handoff": formatter.format_handoff,
        "completion": formatter.format_completion,
    }

    format_func = formatters.get(event_type.lower())
    if not format_func:
        # Fallback to generic formatter
        return formatter.format_generic(
            title=kwargs.get("title", "Gas Town Event"),
            message=kwargs.get("message", ""),
            rig=kwargs.get("rig")
        )

    return format_func(**kwargs)
