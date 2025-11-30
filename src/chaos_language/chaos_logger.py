"""Utilities for capturing timestamped CHAOS runtime events."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional


Formatter = Callable[["LogEntry"], str]
Clock = Callable[[], datetime.datetime]


@dataclass
class LogEntry:
    """A single log line enriched with timestamp and semantic channel."""

    timestamp: datetime.datetime
    channel: str
    message: str

    def render(self, formatter: Optional[Formatter] = None) -> str:
        """Render the entry as text using the provided formatter."""

        if formatter is None:
            return default_formatter(self)
        return formatter(self)


def default_formatter(entry: LogEntry) -> str:
    """Default textual representation used by :class:`ChaosLogger`."""

    timestamp = entry.timestamp.isoformat()
    if not entry.channel or entry.channel == "GENERAL":
        return f"[{timestamp}] {entry.message}"
    return f"[{timestamp}] {entry.channel}: {entry.message}"


class ChaosLogger:
    """Collects structured log entries for symbols, emotions, and narrative.

    The logger keeps an in-memory ring buffer of :class:`LogEntry` objects. It can
    be configured with a custom clock (useful for deterministic testing), a
    maximum number of retained entries, and a formatter that controls export
    layout. All convenience logging helpers delegate to :meth:`log` while tagging
    the appropriate channel name.
    """

    def __init__(
        self,
        *,
        clock: Optional[Clock] = None,
        max_entries: Optional[int] = None,
        formatter: Optional[Formatter] = None,
    ) -> None:
        self._clock: Clock = clock or datetime.datetime.now
        self._max_entries = max_entries
        self._formatter = formatter
        self._logs: List[LogEntry] = []

    def __iter__(self) -> Iterable[LogEntry]:
        return iter(self._logs)

    def log(self, message: str, *, channel: str = "GENERAL") -> None:
        """Record a message under the supplied channel."""

        entry = LogEntry(timestamp=self._clock(), channel=channel, message=message)
        self._logs.append(entry)
        if self._max_entries is not None and len(self._logs) > self._max_entries:
            # Drop the oldest entry to preserve a bounded history.
            self._logs.pop(0)

    def log_symbol(self, name: str, value: str) -> None:
        """Log a structured symbol update."""

        self.log(f"{name} = {value}", channel="SYMBOL")

    def log_emotion(self, emotion: str) -> None:
        """Log an emotion change."""

        self.log(emotion, channel="EMOTION")

    def log_narrative(self, chaosfield: str) -> None:
        """Log a truncated snapshot of the narrative chaosfield."""

        snippet = f"{chaosfield[:60]}..." if len(chaosfield) > 60 else chaosfield
        self.log(snippet, channel="NARRATIVE")

    def tail(self, count: int) -> List[LogEntry]:
        """Return the ``count`` most recent log entries."""

        if count <= 0:
            return []
        return self._logs[-count:]

    def export(
        self,
        *,
        channel: Optional[str] = None,
        formatter: Optional[Formatter] = None,
        delimiter: str = "\n",
    ) -> str:
        """Export the log buffer as a newline-delimited string."""

        entries = (
            entry for entry in self._logs if channel is None or entry.channel == channel
        )
        formatter = formatter or self._formatter
        return delimiter.join(entry.render(formatter) for entry in entries)
