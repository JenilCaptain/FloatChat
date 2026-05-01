import { useMemo, useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatWindow } from './components/ChatWindow';
import { generateAssistantResponse } from './utils/generateResponse';
import { demoQuerySuggestions, initialMessages } from './data/mockData';
import { ChatMessage, ResponseType } from './types';

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const [responseType, setResponseType] = useState<ResponseType>('All');
  const [showMetadata, setShowMetadata] = useState(true);
  const [showRawJson, setShowRawJson] = useState(false);
  const [loading, setLoading] = useState(false);
  const [totalQueries, setTotalQueries] = useState(0);
  const [lastQueryTime, setLastQueryTime] = useState('09:42');

  const canSend = inputValue.trim().length > 0 && !loading;

  const handleSend = () => {
    if (!canSend) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((current) => [...current, userMessage]);
    setInputValue('');
    setLoading(true);
    setTotalQueries((current) => current + 1);
    setLastQueryTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));

    window.setTimeout(() => {
      const assistantMessage = generateAssistantResponse(userMessage.content);
      setMessages((current) => [...current, assistantMessage]);
      setLoading(false);
    }, 900);
  };

  const handleClearHistory = () => {
    setMessages(initialMessages);
    setInputValue('');
    setLoading(false);
    setTotalQueries(0);
    setLastQueryTime('09:42');
  };

  const helperHints = useMemo(() => demoQuerySuggestions, []);

  return (
    <div className="flex min-h-screen flex-col xl:flex-row">
      <Sidebar
        responseType={responseType}
        showMetadata={showMetadata}
        showRawJson={showRawJson}
        onResponseTypeChange={setResponseType}
        onShowMetadataChange={setShowMetadata}
        onShowRawJsonChange={setShowRawJson}
        onClearHistory={handleClearHistory}
        totalQueries={totalQueries}
        lastQueryTime={lastQueryTime}
      />

      <div className="relative flex min-h-screen flex-1 flex-col">
        <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-sky-500/10 to-transparent" />
        <ChatWindow
          messages={messages}
          inputValue={inputValue}
          loading={loading}
          responseType={responseType}
          showMetadata={showMetadata}
          showRawJson={showRawJson}
          onInputChange={setInputValue}
          onSend={handleSend}
        />

        <div className="pointer-events-none absolute bottom-24 left-1/2 hidden -translate-x-1/2 rounded-full border border-slate-800 bg-slate-950/80 px-4 py-2 text-xs text-slate-500 shadow-soft md:block">
          Suggestions: {helperHints.join(' · ')}
        </div>
      </div>
    </div>
  );
}