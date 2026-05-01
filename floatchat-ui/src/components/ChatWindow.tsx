import { useEffect, useMemo, useRef } from 'react';
import { ChatMessage, ResponseType } from '../types';
import { MessageBubble } from './MessageBubble';
import { InputBar } from './InputBar';

interface ChatWindowProps {
  messages: ChatMessage[];
  inputValue: string;
  loading: boolean;
  responseType: ResponseType;
  showMetadata: boolean;
  showRawJson: boolean;
  onInputChange: (value: string) => void;
  onSend: () => void;
}

export function ChatWindow({
  messages,
  inputValue,
  loading,
  responseType,
  showMetadata,
  showRawJson,
  onInputChange,
  onSend,
}: ChatWindowProps) {
  const scrollerRef = useRef<HTMLDivElement>(null);
  const displayMessages = useMemo(() => messages, [messages]);

  useEffect(() => {
    scrollerRef.current?.scrollTo({ top: scrollerRef.current.scrollHeight, behavior: 'smooth' });
  }, [displayMessages, loading]);

  return (
    <main className="flex min-h-screen flex-1 flex-col bg-gradient-to-b from-slate-950/60 to-slate-950">
      <header className="border-b border-slate-800/80 bg-slate-950/60 px-5 py-5 backdrop-blur-xl sm:px-6 lg:px-8">
        <div className="mx-auto flex w-full max-w-5xl flex-col gap-1">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-sky-300">Chat</p>
          <h1 className="text-2xl font-semibold tracking-tight text-slate-50 sm:text-3xl">
            AI Oceanography Assistant – Get instant insights on ocean data
          </h1>
          <p className="max-w-2xl text-sm leading-6 text-slate-400">
            Explore retrieved context, charts, and concise explanations from the FloatChat RAG workflow.
          </p>
        </div>
      </header>

      <section ref={scrollerRef} className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto flex w-full max-w-5xl flex-col gap-5 pb-40">
          {displayMessages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              responseType={responseType}
              showMetadata={showMetadata}
              showRawJson={showRawJson}
            />
          ))}

          {loading ? (
            <div className="flex justify-start">
              <div className="rounded-2xl border border-slate-800 bg-slate-900/90 px-5 py-4 shadow-soft">
                <div className="flex items-center gap-2 text-sm text-slate-400">
                  <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-sky-400 [animation-delay:-0.2s]" />
                  <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-sky-400 [animation-delay:-0.1s]" />
                  <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-sky-400" />
                  <span className="ml-2">Generating response...</span>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </section>

      <InputBar value={inputValue} loading={loading} onChange={onInputChange} onSend={onSend} />
    </main>
  );
}