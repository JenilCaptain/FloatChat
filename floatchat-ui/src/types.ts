export type MessageRole = 'user' | 'assistant';
export type ResponseType = 'All' | 'Text' | 'Charts' | 'Insights';

export interface RetrievedChunk {
  id: string;
  title: string;
  text: string;
  score: number;
}

export interface ChartPoint {
  label: string;
  value: number;
}

export interface ChartPayload {
  title: string;
  xLabel: string;
  yLabel: string;
  data: ChartPoint[];
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  confidence?: number;
  source?: string;
  retrievedChunks?: RetrievedChunk[];
  chart?: ChartPayload;
  rawJson?: Record<string, unknown>;
}