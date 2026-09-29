import React, { useState, useEffect, useRef } from 'react';
import {
  Sparkles, X, Send, Bot, Shield, BookOpen, AlertTriangle,
  Monitor, Cpu, Activity, ExternalLink, CheckCircle2, AlertCircle,
  Loader2, RefreshCw, ArrowRight, CornerDownLeft
} from 'lucide-react';
import { CopilotContextType, CopilotResponse, Alert, Device } from '../../types';
import { apiService } from '../../services/api';

interface AICopilotDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  activeContext: CopilotContextType;
  selectedAlert?: Alert | null;
  selectedDevice?: Device | null;
  selectedDocId?: string;
  selectedDocPage?: number;
  onNavigateToDocumentPage?: (docId: string, pageNum: number) => void;
}

export const AICopilotDrawer: React.FC<AICopilotDrawerProps> = ({
  isOpen,
  onClose,
  activeContext,
  selectedAlert,
  selectedDevice,
  selectedDocId = 'DOC-IEEE-EDGESHIELD-2026',
  selectedDocPage = 1,
  onNavigateToDocumentPage,
}) => {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState<Array<{
    sender: 'user' | 'copilot';
    text?: string;
    response?: CopilotResponse;
    timestamp: string;
    loading?: boolean;
    error?: string;
  }>>([]);

  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, isLoading]);

  // Context-specific suggested prompt questions
  const getSuggestedPrompts = () => {
    switch (activeContext) {
      case 'research':
        return [
          'What datasets were used for the intrusion detection experiments?',
          'Why is Isolation Forest executed before XGBoost in the pipeline?',
          'What was the edge latency benchmark achieved on NVIDIA Jetson?'
        ];
      case 'incident':
        return [
          'Explain this security incident in clinical terms.',
          'What evidence supports the classification of this attack?',
          'What is the recommended containment procedure for this device?'
        ];
      case 'device':
        return [
          'Why is this device assigned its current risk score?',
          'What unusual network activity has this device generated?',
          'What clinical protocols (e.g., Modbus, MQTT) does this device use?'
        ];
      case 'architecture':
        return [
          'Why do we use Isolation Forest before XGBoost?',
          'How does EdgeShield guarantee zero cloud data leakage?',
          'What edge hardware gateways are supported?'
        ];
      default:
        return [
          'Explain the current hospital IoT telemetry health.',
          'What are the primary attack vectors targeting medical devices?'
        ];
    }
  };

  const handleSend = async (questionToSend?: string) => {
    const text = questionToSend || query;
    if (!text.trim() || isLoading) return;

    const userMessageTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setChatHistory(prev => [...prev, {
      sender: 'user',
      text,
      timestamp: userMessageTime
    }]);

    setQuery('');
    setIsLoading(true);

    // Build context payload
    let contextData: any = {};
    if (activeContext === 'incident' && selectedAlert) {
      contextData = {
        alert_id: selectedAlert.alert_id,
        threat_type: selectedAlert.threat_type,
        severity: selectedAlert.severity,
        source_ip: selectedAlert.source_ip,
        target_device_id: selectedAlert.target_device_id,
        target_device_name: selectedAlert.target_device_name || 'Medical IoT Asset',
        key_features: selectedAlert.key_features || {},
        anomaly_score: selectedAlert.anomaly_score
      };
    } else if (activeContext === 'device' && selectedDevice) {
      contextData = {
        device_id: selectedDevice.device_id,
        name: selectedDevice.name,
        category: selectedDevice.category,
        risk_score: selectedDevice.risk_score,
        location: selectedDevice.location,
        status: selectedDevice.status,
        protocol: selectedDevice.protocol
      };
    } else if (activeContext === 'architecture') {
      contextData = {
        component: 'Isolation Forest + XGBoost Edge Pipeline'
      };
    }

    try {
      const response: CopilotResponse = await apiService.queryCopilot({
        context_type: activeContext,
        query: text,
        context_id: selectedDocId,
        context_data: contextData
      });

      setChatHistory(prev => [...prev, {
        sender: 'copilot',
        response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } catch (e: any) {
      setChatHistory(prev => [...prev, {
        sender: 'copilot',
        error: 'Local AI service unavailable. Detection functionality remains operational.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full sm:w-[460px] bg-card/95 backdrop-blur-xl border-l shadow-2xl flex flex-col transition-all duration-300 animate-in slide-in-from-right">
      {/* Header & Active Context Pill */}
      <div className="p-4 border-b flex items-center justify-between bg-card/60">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-medical-teal to-emerald-500 text-white shadow-glow-teal">
            <Sparkles className="h-4 w-4" />
          </div>
          <div>
            <div className="text-sm font-extrabold flex items-center space-x-2">
              <span>EdgeShield AI Copilot</span>
              <span className="text-[10px] font-mono uppercase bg-emerald-500/20 text-emerald-500 px-2 py-0.5 rounded-full font-bold">
                Local SLM
              </span>
            </div>
            <div className="text-[11px] text-muted-foreground">
              Privacy-preserving medical IoT security assistant
            </div>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-1.5 rounded-xl hover:bg-secondary text-muted-foreground hover:text-foreground transition-all"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Dynamic Context Banner */}
      <div className="px-4 py-2.5 bg-secondary/70 border-b flex items-center justify-between text-xs">
        <div className="flex items-center space-x-2 overflow-hidden">
          <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
            Current Context:
          </span>
          {activeContext === 'research' && (
            <span className="flex items-center space-x-1 font-semibold text-medical-teal truncate">
              <BookOpen className="h-3.5 w-3.5 shrink-0" />
              <span className="truncate">Research Doc (Page {selectedDocPage})</span>
            </span>
          )}
          {activeContext === 'incident' && (
            <span className="flex items-center space-x-1 font-semibold text-rose-500 truncate">
              <AlertTriangle className="h-3.5 w-3.5 shrink-0" />
              <span className="truncate">Incident {selectedAlert?.alert_id || 'Active'}</span>
            </span>
          )}
          {activeContext === 'device' && (
            <span className="flex items-center space-x-1 font-semibold text-blue-500 truncate">
              <Monitor className="h-3.5 w-3.5 shrink-0" />
              <span className="truncate">{selectedDevice?.name || 'Device'}</span>
            </span>
          )}
          {activeContext === 'architecture' && (
            <span className="flex items-center space-x-1 font-semibold text-purple-500 truncate">
              <Cpu className="h-3.5 w-3.5 shrink-0" />
              <span>Dual-Stage ML Engine</span>
            </span>
          )}
          {activeContext === 'telemetry' && (
            <span className="flex items-center space-x-1 font-semibold text-emerald-500 truncate">
              <Activity className="h-3.5 w-3.5 shrink-0" />
              <span>Live Telemetry Stream</span>
            </span>
          )}
        </div>

        <span className="text-[10px] font-mono text-muted-foreground shrink-0 ml-2">
          HIPAA Zero-Leakage
        </span>
      </div>

      {/* Chat Messages Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
        {/* Empty State / Initial Greeting */}
        {chatHistory.length === 0 && (
          <div className="space-y-4 py-4">
            <div className="p-4 rounded-2xl bg-secondary/50 border space-y-2">
              <div className="font-bold text-foreground flex items-center space-x-1.5">
                <Bot className="h-4 w-4 text-medical-teal" />
                <span>EdgeShield AI Copilot Ready</span>
              </div>
              <p className="text-muted-foreground leading-relaxed text-[11px]">
                I can assist you with explaining active security anomalies, identifying anomalous telemetry evidence,
                cross-referencing IEEE research paper benchmarks, and guiding containment procedures.
              </p>
            </div>

            {/* Suggested Questions */}
            <div className="space-y-2">
              <div className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
                Suggested Inquiries for Current Context:
              </div>
              <div className="space-y-1.5">
                {getSuggestedPrompts().map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSend(prompt)}
                    className="w-full text-left p-2.5 rounded-xl border bg-card hover:border-medical-teal/60 hover:bg-secondary/60 transition-all text-foreground text-xs flex items-center justify-between group"
                  >
                    <span>{prompt}</span>
                    <ArrowRight className="h-3.5 w-3.5 opacity-0 group-hover:opacity-100 text-medical-teal transition-opacity" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Message Thread */}
        {chatHistory.map((msg, i) => (
          <div key={i} className={`flex flex-col space-y-1.5 ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
            {msg.sender === 'user' ? (
              <div className="max-w-[85%] bg-medical-teal text-white p-3 rounded-2xl rounded-tr-sm shadow-sm">
                <p className="whitespace-pre-wrap">{msg.text}</p>
                <div className="text-[10px] text-white/70 text-right mt-1 font-mono">{msg.timestamp}</div>
              </div>
            ) : (
              <div className="max-w-[95%] bg-card border shadow-subtle p-4 rounded-2xl rounded-tl-sm space-y-3">
                {msg.error ? (
                  <div className="flex items-center space-x-2 text-rose-500">
                    <AlertCircle className="h-4 w-4 shrink-0" />
                    <span>{msg.error}</span>
                  </div>
                ) : (
                  msg.response && (
                    <>
                      {/* 1. Summary */}
                      <div>
                        <div className="font-bold text-foreground text-xs mb-1">Summary</div>
                        <p className="text-muted-foreground leading-relaxed">{msg.response.summary}</p>
                      </div>

                      {/* 2. Evidence from actual data / telemetry / paper */}
                      {msg.response.evidence && (
                        <div className="p-2.5 rounded-xl bg-secondary/80 border text-[11px] space-y-1">
                          <div className="font-semibold text-foreground flex items-center space-x-1.5">
                            <Shield className="h-3.5 w-3.5 text-medical-teal" />
                            <span>Telemetry / Factual Evidence:</span>
                          </div>
                          <div className="text-muted-foreground font-mono text-[10px] leading-relaxed">
                            {msg.response.evidence}
                          </div>
                        </div>
                      )}

                      {/* 3. Analysis */}
                      {msg.response.analysis && (
                        <div>
                          <div className="font-bold text-foreground text-xs mb-1">Clinical Analysis</div>
                          <p className="text-muted-foreground leading-relaxed">{msg.response.analysis}</p>
                        </div>
                      )}

                      {/* 4. Recommended Mitigation */}
                      {msg.response.recommended_mitigation && (
                        <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-[11px] space-y-1">
                          <div className="font-bold text-amber-600 dark:text-amber-400">Recommended Containment</div>
                          <div className="text-muted-foreground whitespace-pre-line leading-relaxed">
                            {msg.response.recommended_mitigation}
                          </div>
                        </div>
                      )}

                      {/* 5. Provenance Sources & Citations */}
                      {msg.response.sources && msg.response.sources.length > 0 && (
                        <div className="pt-2 border-t space-y-1.5">
                          <div className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                            Information Provenance:
                          </div>
                          <div className="flex flex-wrap gap-1.5">
                            {msg.response.sources.map((src, idx) => (
                              <span
                                key={idx}
                                className={`px-2 py-0.5 rounded-md text-[10px] font-mono font-semibold ${
                                  src.type === 'Research Document'
                                    ? 'bg-purple-500/15 text-purple-600 dark:text-purple-400 border border-purple-500/20'
                                    : src.type === 'Security Telemetry'
                                    ? 'bg-blue-500/15 text-blue-600 dark:text-blue-400 border border-blue-500/20'
                                    : 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20'
                                }`}
                              >
                                [{src.type}]: {src.detail}
                              </span>
                            ))}
                          </div>

                          {/* Interactive [Open Source Page] Button */}
                          {msg.response.page_reference && onNavigateToDocumentPage && (
                            <div className="pt-1">
                              <button
                                onClick={() => {
                                  onNavigateToDocumentPage(
                                    selectedDocId || 'DOC-IEEE-EDGESHIELD-2026',
                                    msg.response?.page_reference || 1
                                  );
                                  onClose();
                                }}
                                className="flex items-center space-x-1.5 text-medical-teal hover:underline text-[11px] font-bold"
                              >
                                <span>Open Source Document at Page {msg.response.page_reference}</span>
                                <ExternalLink className="h-3 w-3" />
                              </button>
                            </div>
                          )}
                        </div>
                      )}

                      <div className="text-[10px] text-muted-foreground font-mono flex items-center justify-between pt-1">
                        <span>Engine: {msg.response.ai_engine_used}</span>
                        <span>{msg.timestamp}</span>
                      </div>
                    </>
                  )
                )}
              </div>
            )}
          </div>
        ))}

        {/* Loading Spinner */}
        {isLoading && (
          <div className="flex items-center space-x-2.5 p-3 rounded-xl bg-secondary/60 border text-xs text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin text-medical-teal" />
            <span>
              {activeContext === 'research'
                ? 'Retrieving research document passages & validating grounding...'
                : 'Analyzing incident telemetry context...'}
            </span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input Bar */}
      <div className="p-4 border-t bg-card/60">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center space-x-2"
        >
          <input
            type="text"
            placeholder={`Ask Copilot about ${activeContext}...`}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            className="flex-1 bg-secondary border text-xs rounded-xl px-3.5 py-2.5 focus:ring-1 focus:ring-medical-teal outline-none disabled:opacity-60"
          />
          <button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="p-2.5 bg-medical-teal hover:bg-medical-teal-dark disabled:opacity-40 text-white rounded-xl shadow-glow-teal transition-all"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
        <div className="text-[10px] text-muted-foreground text-center mt-2 font-mono">
          EdgeShield AI local SLM • Offline Privacy Preserved
        </div>
      </div>
    </div>
  );
};
