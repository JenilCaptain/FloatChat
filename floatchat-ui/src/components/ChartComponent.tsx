import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { ChartPayload } from '../types';

interface ChartComponentProps {
  chart: ChartPayload;
}

export function ChartComponent({ chart }: ChartComponentProps) {
  return (
    <div className="mt-4 rounded-2xl border border-slate-800 bg-slate-950/70 p-4 shadow-soft">
      <div className="mb-3">
        <p className="text-sm font-semibold text-slate-100">{chart.title}</p>
        <p className="text-xs text-slate-500">{chart.xLabel} vs {chart.yLabel}</p>
      </div>
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chart.data} margin={{ top: 8, right: 8, bottom: 4, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="label" tick={{ fill: '#94a3b8', fontSize: 12 }} stroke="#334155" />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} stroke="#334155" />
            <Tooltip
              contentStyle={{
                background: '#020617',
                border: '1px solid #334155',
                borderRadius: '14px',
                color: '#e2e8f0',
              }}
            />
            <Line type="monotone" dataKey="value" stroke="#38bdf8" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}