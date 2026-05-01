import { RetrievedChunk } from '../types';

interface RetrievedContextProps {
  chunks: RetrievedChunk[];
}

export function RetrievedContext({ chunks }: RetrievedContextProps) {
  return (
    <details className="mt-4 rounded-2xl border border-slate-800 bg-slate-950/50 p-4">
      <summary className="cursor-pointer list-none text-sm font-semibold text-slate-200">
        Retrieved Context
        <span className="ml-2 text-xs text-slate-500">Top {chunks.length}</span>
      </summary>
      <div className="mt-4 grid gap-3">
        {chunks.map((chunk) => (
          <div key={chunk.id} className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <p className="text-sm font-medium text-slate-100">{chunk.title}</p>
              <span className="rounded-full bg-sky-500/15 px-2 py-1 text-xs font-semibold text-sky-300">
                {chunk.score.toFixed(2)}
              </span>
            </div>
            <p className="mt-2 text-sm leading-6 text-slate-400">{chunk.text}</p>
          </div>
        ))}
      </div>
    </details>
  );
}