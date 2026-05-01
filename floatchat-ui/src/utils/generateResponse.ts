import { ChatMessage } from '../types';
import { temperatureDepthChart } from '../data/mockData';

const chunkTemplates = [
  'Observed values are consistent with the prevailing seasonal baseline.',
  'The data supports a stable thermocline with no strong outlier signal.',
  'Surface variability is mild and does not materially change the interpretation.',
];

export function generateAssistantResponse(input: string): ChatMessage {
  const lower = input.toLowerCase();
  const wantsChart = /temperature|depth|trend|profile|salinity|anomaly/.test(lower);

  const content = lower.includes('salinity')
    ? 'Salinity remains within the expected envelope, with minor surface variation likely driven by local forcing and freshwater influence.'
    : lower.includes('anomaly')
      ? 'I do not see evidence of a major anomaly in the retrieved context. The signal appears steady and consistent with historical patterns.'
      : 'The retrieved context suggests stable oceanographic conditions, with a clear near-surface signal and a predictable decline with depth.';

  return {
    id: `assistant-${Date.now()}`,
    role: 'assistant',
    content,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    confidence: Number((0.82 + Math.min(input.length, 40) / 200).toFixed(2)),
    source: 'Argo dataset',
    retrievedChunks: [
      {
        id: `${Date.now()}-1`,
        title: 'Primary retrieval',
        text: chunkTemplates[0],
        score: 0.95,
      },
      {
        id: `${Date.now()}-2`,
        title: 'Seasonal context',
        text: chunkTemplates[1],
        score: 0.9,
      },
      {
        id: `${Date.now()}-3`,
        title: 'Secondary signal',
        text: chunkTemplates[2],
        score: 0.86,
      },
    ],
    chart: wantsChart ? temperatureDepthChart : undefined,
    rawJson: {
      input,
      confidence: Number((0.82 + Math.min(input.length, 40) / 200).toFixed(2)),
      source: 'Argo dataset',
      chartIncluded: wantsChart,
    },
  };
}