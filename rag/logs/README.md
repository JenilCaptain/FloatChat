# RAG Query Logs

This directory contains log files for the RAG system, including:

- **Query logs** (`rag_queries_YYYYMMDD.jsonl`): Complete query-response cycles
- **Retrieval logs** (`retrieval_YYYYMMDD.jsonl`): Document retrieval operations
- **Generation logs** (`generation_YYYYMMDD.jsonl`): LLM answer generation
- **Error logs** (`errors_YYYYMMDD.jsonl`): System errors and exceptions

## Log Format

Logs are stored in JSONL format (one JSON object per line) for easy parsing and analysis.

### Query Log Entry Example

```json
{
  "timestamp": "2026-01-06T10:30:45.123456",
  "query": "What is marine biodiversity?",
  "retrieved_docs": [
    {
      "score": 0.89,
      "document": {
        "text": "Marine biodiversity refers to...",
        "metadata": { "source": "doc1.pdf" }
      }
    }
  ],
  "answer": "Marine biodiversity refers to the variety...",
  "metadata": {
    "retrieval_time": 0.45,
    "generation_time": 2.3
  }
}
```

## Usage

```python
from rag.logs import QueryLogger

logger = QueryLogger(log_dir="logs")
logger.log_query(
    query="What is ocean acidification?",
    retrieved_docs=results,
    answer=response,
    metadata={"retrieval_time": 0.5, "generation_time": 2.1}
)
```

## Benefits

- **Debugging**: Track what documents were retrieved for each query
- **Monitoring**: Analyze system performance and response quality
- **Evaluation**: Build test datasets from production queries
- **Auditing**: Maintain records of system interactions
