#!/usr/bin/env python3
"""
Example usage of the NotificationFormatter.

Run this file to see formatted output for all event types.
"""

import json
from datetime import datetime
from formatter import NotificationFormatter, format_event, EventType


def print_embed(title: str, embed: dict):
    """Pretty print an embed for demonstration."""
    print(f"\n{'='*60}")
    print(f"Example: {title}")
    print('='*60)
    print(json.dumps(embed, indent=2))


def main():
    """Demonstrate all formatter methods."""
    formatter = NotificationFormatter()

    # Example 1: Nudge
    print_embed(
        "Nudge Event",
        formatter.format_nudge(
            from_agent="discord_bot/crew/core",
            to_agent="discord_bot/crew/notify",
            message="Formatter module looks good! Proceeding with MCP integration.",
            rig="discord_bot"
        )
    )

    # Example 2: Broadcast
    print_embed(
        "Broadcast Event",
        formatter.format_broadcast(
            from_agent="mayor/",
            message="🎉 Discord notification system is now live! Use the send_discord_message MCP tool to notify the seer.",
            target_scope="all",
            rig=None
        )
    )

    # Example 3: Mail
    print_embed(
        "Mail Event",
        formatter.format_mail(
            from_agent="discord_bot/crew/notify",
            to_agent="--human",
            subject="Notification Formatter Complete",
            message="The NotificationFormatter module has been completed with support for all Gas Town event types:\n\n"
                   "• Nudge\n• Broadcast\n• Mail\n• Convoy Updates\n• Escalations\n• Handoffs\n• Completions\n\n"
                   "Ready for core crew to integrate into the MCP server.",
            mail_id="hq-abc123",
            priority="normal"
        )
    )

    # Example 4: Convoy Update
    print_embed(
        "Convoy Update (In Progress)",
        formatter.format_convoy_update(
            convoy_id="db-conv-001",
            convoy_name="Discord Integration Sprint",
            status="in_progress",
            message="Making steady progress on the notification system. Formatter complete, MCP server next.",
            completed=2,
            total=5,
            rig="discord_bot"
        )
    )

    print_embed(
        "Convoy Update (Complete)",
        formatter.format_convoy_update(
            convoy_id="db-conv-001",
            convoy_name="Discord Integration Sprint",
            status="completed",
            message="All tasks completed! Discord notification system is fully operational.",
            completed=5,
            total=5,
            rig="discord_bot"
        )
    )

    # Example 5: Escalations
    print_embed(
        "Escalation (Low)",
        formatter.format_escalation(
            from_agent="discord_bot/polecats/alpha-1",
            issue="Slow test suite",
            severity="low",
            details="Tests are taking 30s to run, could be optimized but not blocking work.",
            bead_id="db-456",
            rig="discord_bot"
        )
    )

    print_embed(
        "Escalation (Critical)",
        formatter.format_escalation(
            from_agent="discord_bot/witness",
            issue="Polecat completely stuck",
            severity="critical",
            details="Polecat alpha-3 has been idle for 15 minutes with no progress. "
                   "Last action was 'Running tests' but process appears frozen. "
                   "Manual intervention required.",
            bead_id="db-789",
            rig="discord_bot"
        )
    )

    # Example 6: Handoff
    print_embed(
        "Handoff Event",
        formatter.format_handoff(
            from_agent="discord_bot/crew/notify",
            subject="Context cycling - formatter complete",
            message="Completed the NotificationFormatter module with all event types. "
                   "Module is ready for core crew to integrate. Next session should "
                   "focus on testing integration and documentation updates.",
            hooked_work="db-d6o",
            rig="discord_bot"
        )
    )

    # Example 7: Completion
    print_embed(
        "Completion Event",
        formatter.format_completion(
            agent="discord_bot/crew/notify",
            bead_id="db-d6o",
            bead_title="Notification System Integration - Formatter Module",
            summary="Created NotificationFormatter class with support for all Gas Town event types. "
                   "Includes comprehensive documentation and examples. Ready for MCP server integration.",
            rig="discord_bot"
        )
    )

    # Example 8: Generic (Fallback)
    print_embed(
        "Generic Event",
        formatter.format_generic(
            title="🔧 System Event",
            message="A custom event occurred that doesn't fit other categories.",
            event_type=EventType.NUDGE,
            fields=[
                {"name": "Status", "value": "Operational", "inline": True},
                {"name": "Component", "value": "Discord Bot", "inline": True},
            ],
            rig="discord_bot"
        )
    )

    # Example 9: Using the convenience function
    print_embed(
        "Convenience Function (format_event)",
        format_event(
            "nudge",
            from_agent="discord_bot/crew/notify",
            to_agent="mayor/",
            message="Using the convenience function is easier!",
            rig="discord_bot"
        )
    )

    print("\n" + "="*60)
    print("All examples complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
