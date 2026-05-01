import { ChatMessage, ChartPayload, RetrievedChunk } from '../types';

export const responseTypes = ['All', 'Text', 'Charts', 'Insights'] as const;

export const initialRetrievedChunks: RetrievedChunk[] = [
  {
    id: 'c1',
    title: 'Argo profile summary',
    text: 'Temperature decreases steadily below the mixed layer, indicating a stable thermocline.',
    score: 0.95,
  },
  {
    id: 'c2',
    title: 'Regional seasonality',
    text: 'The local basin shows a mild surface warming trend during late summer and early fall.',
    score: 0.91,
  },
  {
    id: 'c3',
    title: 'Confidence note',
    text: 'Anomaly levels remain within the expected range for the selected sampling window.',
    score: 0.87,
  },
];

export const temperatureDepthChart: ChartPayload = {
  title: 'Temperature vs Depth',
  xLabel: 'Depth (m)',
  yLabel: 'Temperature (°C)',
  data: [
    { label: '0', value: 24.7 },
    { label: '50', value: 22.3 },
    { label: '100', value: 19.6 },
    { label: '200', value: 16.2 },
    { label: '500', value: 10.4 },
    { label: '1000', value: 4.2 },
  ],
};

export const initialMessages: ChatMessage[] = [
  {
    id: 'm1',
    role: 'assistant',
    content:
      'FloatChat is ready. Ask about ocean temperature, salinity, depth, anomalies, or seasonal patterns and I will return a retrieval-augmented summary.',
    timestamp: '09:42',
    confidence: 0.93,
    source: 'Argo dataset',
    retrievedChunks: initialRetrievedChunks,
    chart: temperatureDepthChart,
    rawJson: {
      confidence: 0.93,
      source: 'Argo dataset',
      retrievedCount: 3,
    },
  },
];

export const demoQuerySuggestions = [
  'What does the latest Argo profile show?',
  'Show temperature vs depth for the region.',
  'Summarize any ocean anomalies this week.',
];