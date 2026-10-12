import { useState, useEffect, useRef } from 'react';
import { TelemetryStreamEvent } from '../types';

export function useWebSocket(url: string) {
  const [lastEvent, setLastEvent] = useState<TelemetryStreamEvent | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Determine WS protocol based on window location
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = url.startsWith('ws') ? url : `${protocol}//${window.location.host}${url}`;

    const ws = new WebSocket(wsUrl);
    socketRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const raw = JSON.parse(event.data);
        // Normalize: if backend broadcast an envelope, unpack payload fields to root
        let normalized: TelemetryStreamEvent;
        if (raw && typeof raw === 'object' && raw.payload && typeof raw.payload === 'object') {
          normalized = {
            ...raw.payload,
            event_type: raw.event_type || raw.payload.event_type,
            event_id: raw.event_id || raw.payload.event_id,
            correlation_id: raw.correlation_id || raw.payload.correlation_id,
            timestamp: raw.timestamp || raw.payload.timestamp,
          };
        } else {
          normalized = raw;
        }
        setLastEvent(normalized);
      } catch (e) {
        console.error("WebSocket message parse error", e);
      }
    };

    ws.onerror = () => {
      setIsConnected(false);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  return { lastEvent, isConnected };
}
