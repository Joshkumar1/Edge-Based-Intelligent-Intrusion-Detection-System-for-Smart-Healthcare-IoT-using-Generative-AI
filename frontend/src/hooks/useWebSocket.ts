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
        const parsed: TelemetryStreamEvent = JSON.parse(event.data);
        setLastEvent(parsed);
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
