import asyncio
import json
import logging
from collections import deque
from datetime import datetime, timezone
from typing import Dict, Any, List, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger("edgeshield.websocket")


class ConnectionManager:
    """
    Reliable, non-blocking WebSocket stream manager for edge security events.
    Features:
    - Non-blocking broadcast with per-client timeouts to prevent slow clients from stalling detection
    - Bounded deduplication tracking by event_id
    - Structured WebSocket event envelope contract
    - Stale connection detection and automatic cleanup
    - Backwards-compatible payload fields for existing dashboard consumers
    """
    def __init__(self, send_timeout: float = 0.25):
        self.active_connections: List[WebSocket] = []
        self.send_timeout = send_timeout
        self._seen_event_ids: deque = deque(maxlen=1000)
        self._seen_event_set: Set[str] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Active connections: {len(self.active_connections)}")

    def is_duplicate(self, event_id: str) -> bool:
        """Checks if event_id has already been broadcast to prevent duplicate processing."""
        if not event_id:
            return False
        if event_id in self._seen_event_set:
            return True
        if len(self._seen_event_ids) >= 1000:
            oldest = self._seen_event_ids.popleft()
            self._seen_event_set.discard(oldest)
        self._seen_event_ids.append(event_id)
        self._seen_event_set.add(event_id)
        return False

    async def _send_to_connection(self, connection: WebSocket, message_text: str) -> bool:
        """Sends serialized message to a single connection with timeout protection."""
        try:
            await asyncio.wait_for(connection.send_text(message_text), timeout=self.send_timeout)
            return True
        except Exception:
            return False

    async def broadcast(self, message: dict):
        """
        Broadcasts a dictionary to all active clients concurrently without blocking.
        Slow clients that exceed send_timeout are pruned to preserve edge performance.
        """
        if not self.active_connections:
            return

        message_text = json.dumps(message, default=str)
        tasks = [self._send_to_connection(conn, message_text) for conn in self.active_connections]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        disconnected: List[WebSocket] = []
        for conn, success in zip(self.active_connections, results):
            if success is not True:
                disconnected.append(conn)

        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_envelope(
        self,
        event_type: str,
        event_id: str,
        correlation_id: str,
        payload: Dict[str, Any],
        timestamp: Optional[str] = None
    ):
        """Broadcasts a structured event envelope satisfying the canonical contract."""
        envelope = {
            "event_type": event_type,
            "event_id": event_id,
            "correlation_id": correlation_id,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        await self.broadcast(envelope)


manager = ConnectionManager()
