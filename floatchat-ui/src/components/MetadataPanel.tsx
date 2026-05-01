interface MetadataPanelProps {
  confidence?: number;
  source?: string;
}

export function MetadataPanel({ confidence, source }: MetadataPanelProps) {
  return (
    <div className="mt-4 flex flex-wrap gap-2">
      <span className="rounded-full border border-slate-700 bg-slate-900 px-3 py-1 text-xs font-semibold text-slate-300">
        Confidence {confidence?.toFixed(2)}
      </span>
      <span className="rounded-full border border-slate-700 bg-slate-900 px-3 py-1 text-xs font-semibold text-slate-300">
        Source {source}
      </span>
    </div>
  );
}