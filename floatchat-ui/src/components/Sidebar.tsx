import { ResponseType } from '../types';
import { responseTypes } from '../data/mockData';

interface SidebarProps {
  responseType: ResponseType;
  showMetadata: boolean;
  showRawJson: boolean;
  onResponseTypeChange: (value: ResponseType) => void;
  onShowMetadataChange: (value: boolean) => void;
  onShowRawJsonChange: (value: boolean) => void;
  onClearHistory: () => void;
  totalQueries: number;
  lastQueryTime: string;
}

export function Sidebar({
  responseType,
  showMetadata,
  showRawJson,
  onResponseTypeChange,
  onShowMetadataChange,
  onShowRawJsonChange,
  onClearHistory,
  totalQueries,
  lastQueryTime,
}: SidebarProps) {
  return (
    <aside className="w-full border-r border-slate-800/80 bg-slate-950/90 px-5 py-6 backdrop-blur xl:h-screen xl:w-[320px]">
      <div className="flex h-full flex-col gap-6">
        <div className="rounded-2xl border border-slate-800 bg-white/5 p-5 shadow-soft">
          <p className="text-xl font-semibold tracking-[0.2em] text-slate-100">🌊 FLOATCHAT</p>
          <p className="mt-2 text-sm leading-6 text-slate-400">AI-powered ocean intelligence dashboard</p>
        </div>

        <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">Response Types</p>
          <select
            value={responseType}
            onChange={(event) => onResponseTypeChange(event.target.value as ResponseType)}
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-200 outline-none transition focus:border-sky-500"
          >
            {responseTypes.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </section>

        <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">Settings</p>
          <div className="space-y-3">
            <label className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3 text-sm text-slate-300">
              <span>Show response metadata</span>
              <input
                type="checkbox"
                checked={showMetadata}
                onChange={(event) => onShowMetadataChange(event.target.checked)}
                className="h-4 w-4 accent-sky-500"
              />
            </label>
            <label className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3 text-sm text-slate-300">
              <span>Show raw JSON</span>
              <input
                type="checkbox"
                checked={showRawJson}
                onChange={(event) => onShowRawJsonChange(event.target.checked)}
                className="h-4 w-4 accent-sky-500"
              />
            </label>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">Chat Controls</p>
          <button
            onClick={onClearHistory}
            className="w-full rounded-xl bg-sky-500 px-4 py-3 text-sm font-semibold text-white shadow-soft transition hover:bg-sky-400"
          >
            Clear History
          </button>
        </section>

        <div className="mt-auto rounded-2xl border border-slate-800 bg-slate-900/40 p-4 text-sm text-slate-400">
          <div className="flex items-center justify-between">
            <span>Total queries</span>
            <span className="font-medium text-slate-200">{totalQueries}</span>
          </div>
          <div className="mt-2 flex items-center justify-between">
            <span>Last query time</span>
            <span className="font-medium text-slate-200">{lastQueryTime || '—'}</span>
          </div>
          <div className="mt-4 border-t border-slate-800 pt-4 text-xs leading-5 text-slate-500">
            <p>FloatChat v1.0</p>
            <p>Built with AI</p>
          </div>
        </div>
      </div>
    </aside>
  );
}