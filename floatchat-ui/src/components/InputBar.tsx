import { FormEvent, KeyboardEvent } from 'react';

interface InputBarProps {
  value: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSend: () => void;
}

export function InputBar({ value, loading, onChange, onSend }: InputBarProps) {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSend();
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      onSend();
    }
  };

  return (
    <footer className="border-t border-slate-800/80 bg-slate-950/85 px-4 py-4 backdrop-blur-xl sm:px-6 lg:px-8">
      <form onSubmit={handleSubmit} className="mx-auto flex w-full max-w-5xl items-end gap-3">
        <div className="flex-1 rounded-2xl border border-slate-800 bg-slate-900/70 px-4 py-3 shadow-soft focus-within:border-sky-500/60">
          <textarea
            value={value}
            onChange={(event) => onChange(event.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder="Type your message and press Enter..."
            className="max-h-40 w-full resize-none border-0 bg-transparent text-[15px] leading-7 text-slate-100 outline-none placeholder:text-slate-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !value.trim()}
          className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-sky-500 text-white shadow-soft transition hover:-translate-y-0.5 hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-50"
          aria-label="Send message"
        >
          <span className="text-lg">➤</span>
        </button>
      </form>
    </footer>
  );
}