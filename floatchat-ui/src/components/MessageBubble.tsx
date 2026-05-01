import { ChartComponent } from './ChartComponent';
import { RetrievedContext } from './RetrievedContext';
import { MetadataPanel } from './MetadataPanel';
import { ChatMessage, ResponseType } from '../types';

interface MessageBubbleProps {
  message: ChatMessage;
  showMetadata: boolean;
  showRawJson: boolean;
  responseType: ResponseType;
}

export function MessageBubble({ message, showMetadata, showRawJson, responseType }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const showChart = responseType === 'All' || responseType === 'Charts';
  const showText = responseType === 'All' || responseType === 'Text' || responseType === 'Insights';

  return (
    <div className={`flex animate-fadeUp ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[92%] sm:max-w-[78%] ${isUser ? 'ml-auto' : 'mr-auto'}`}>
        <div
          className={`rounded-2xl px-5 py-4 shadow-soft ring-1 ${
            isUser
              ? 'bg-sky-500/90 text-white ring-sky-400/20'
              : 'bg-slate-900/90 text-slate-100 ring-slate-800'
          }`}
        >
          <div className="flex items-center justify-between gap-4 text-xs text-slate-400">
            <span className={`font-semibold uppercase tracking-[0.2em] ${isUser ? 'text-sky-50/80' : 'text-sky-300'}`}>
              {isUser ? 'You' : 'Assistant'}
            </span>
            <span>{message.timestamp}</span>
          </div>

          {showText ? (
            <p className={`mt-3 whitespace-pre-wrap text-[15px] leading-7 ${isUser ? 'text-white' : 'text-slate-200'}`}>
              {message.content}
            </p>
          ) : null}

          {!isUser && showMetadata ? <MetadataPanel confidence={message.confidence} source={message.source} /> : null}
          {!isUser && showChart && message.chart ? <ChartComponent chart={message.chart} /> : null}
          {!isUser && message.retrievedChunks ? <RetrievedContext chunks={message.retrievedChunks} /> : null}
          {!isUser && message.rawJson ? (
            <details className="mt-4 rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
              <summary className="cursor-pointer list-none text-sm font-semibold text-slate-200">Raw JSON</summary>
              <pre className="mt-3 overflow-x-auto text-xs leading-6 text-slate-400">
                {JSON.stringify(message.rawJson, null, 2)}
              </pre>
            </details>
          ) : null}
        </div>
      </div>
    </div>
  );
}