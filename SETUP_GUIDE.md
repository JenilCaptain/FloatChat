# RAG Pipeline Setup & Configuration Guide

## Project Structure

```
AgroOcean Project/
├── data/                           # Data directory
│   ├── argo_profiles_master.parquet     # Main dataset (749K rows)
│   └── argo_profiles_reduced.parquet    # Reduced dataset (56K rows)
├── rag/                            # RAG system
│   ├── ingestion/
│   │   ├── loader.py               # Loads Parquet files
│   │   └── chunker.py              # Token-based chunking
│   ├── embeddings/
│   │   └── embedder.py             # HuggingFace embeddings
│   ├── vectordb/
│   │   └── qdrant_client.py        # Vector database
│   ├── retrieval/
│   │   └── retriever.py            # Document retrieval
│   ├── llm/
│   │   ├── ollama_llm.py           # LLM wrapper
│   │   └── prompt.py               # Prompt templates
│   ├── pipeline/
│   │   └── rag_pipeline.py         # Main RAG pipeline
│   ├── evaluation/
│   │   ├── precision_at_k.py       # Precision metrics
│   │   └── recall_at_k.py          # Recall metrics
│   ├── logs/
│   │   └── query_logger.py         # Query logging
│   └── utils/
│       └── config.py               # Configuration
├── logs/                           # Generated logs (created at runtime)
├── main.py                         # Main entry point
└── requirements.txt                # Dependencies
```

## Configuration Files

### Default Paths (in `rag/utils/config.py`)

```python
data_path: str = "data"                    # Points to ./data/ directory
logs_path: str = "logs"                    # Creates ./logs/ directory
vectordb_path: str = "vectordb"            # For future Qdrant persistence
```

### Environment Variables (Optional)

You can override defaults using environment variables:

```bash
# Data paths
export DATA_PATH="data"
export LOGS_PATH="logs"

# Embedding settings
export EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
export EMBEDDING_BATCH_SIZE="32"

# Vector DB settings
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"
export COLLECTION_NAME="documents"

# LLM settings
export LLM_MODEL="phi3"
export OLLAMA_URL="http://localhost:11434"
export LLM_TEMPERATURE="0.7"

# Chunking settings
export CHUNK_SIZE="500"
export CHUNK_OVERLAP="100"
export ENCODING_NAME="cl100k_base"

# Retrieval settings
export TOP_K="5"
export SIMILARITY_THRESHOLD="0.5"
```

## Prerequisites

### 1. Python Dependencies

**First, create a virtual environment (Recommended):**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

**Then install dependencies:**

```bash
pip install -r requirements.txt
```

**Key packages:**

- `pandas` - Data loading (Parquet files)
- `sentence-transformers` - Embeddings
- `qdrant-client` - Vector database
- `ollama` - LLM interface
- `tiktoken` - Token counting
- `pyarrow` - Parquet support

### 2. Services to Run

#### Qdrant Vector Database

```bash
# Option 1: Docker (Recommended)
docker run -d -p 6333:6333 qdrant/qdrant

# Option 2: Download & run standalone
# See: https://qdrant.tech/documentation/quick_start/
```

#### Ollama LLM Server

```bash
# Install Ollama from: https://ollama.ai

# Pull and run the model
ollama pull phi3
ollama serve

# In another terminal, verify:
curl http://localhost:11434/api/tags
```

#### HuggingFace Model (Auto-downloaded)

The embedding model `sentence-transformers/all-MiniLM-L6-v2` will be automatically downloaded and cached on first use.

## Running the Pipeline

### Quick Start

```bash
# From project root directory
python main.py
```

This will:

1. Load Parquet files from `data/`
2. Transform oceanographic data to text
3. Chunk documents into tokens
4. Generate embeddings
5. Index in Qdrant
6. Start interactive query mode

### Example Queries

```
Query: What is the average temperature in the surface layer?
Query: Tell me about salinity measurements at tropical locations
Query: Which regions have the highest pressure readings?
Query: Describe the oceanographic conditions in the Indian Ocean
```

## Output & Logs

### Logs Directory Structure

```
logs/
├── rag_queries_20260128.jsonl       # Complete query-response cycles
├── retrieval_20260128.jsonl         # Retrieved document metadata
├── generation_20260128.jsonl        # LLM generation logs
└── errors_20260128.jsonl            # Error logs
```

### Log Format (JSONL)

Each line is a JSON object:

```json
{
  "timestamp": "2026-01-28T10:30:45.123456",
  "query": "What is the average temperature?",
  "retrieved_docs": [
    {
      "score": 0.89,
      "document": {
        "text": "...",
        "metadata": {...}
      }
    }
  ],
  "answer": "Based on the retrieved documents...",
  "metadata": {
    "retrieval_time": 0.45,
    "generation_time": 2.3
  }
}
```

## Data Format Transformation

### Input (Parquet)

```
Master file: date, latitude, longitude, temperature, salinity, depth_m, platform...
Reduced file: month, lat_bin, lon_bin, temperature, salinity, depth_zone...
```

### Output (RAG Format)

```python
{
    "text": "Oceanographic measurement recorded on 2002-11-21. Location: Latitude -0.1°, Longitude 77.2°. Temperature: 28.86°C. Salinity: 35.35 PSU.",
    "metadata": {
        "source_file": "argo_profiles_master.parquet",
        "date": "2002-11-21",
        "latitude": -0.1,
        "longitude": 77.2,
        ...
    }
}
```

## Troubleshooting

### "Connection refused" Error

```
Error: Error connecting to Qdrant at localhost:6333
```

**Fix:** Start Qdrant service first

```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

### "Model not found" Error

```
Error in chat completion: ... model not found
```

**Fix:** Pull the model in Ollama

```bash
ollama pull phi3
ollama serve
```

### "No module named 'sentence_transformers'" Error

```
Fix: pip install sentence-transformers
```

### Slow Processing

- First time: Model downloads will take time
- Subsequent runs: Should be faster (cached)
- Reduce TOP_K for faster retrieval
- Use reduced dataset: `data/argo_profiles_reduced.parquet`

## Configuration Customization

Edit `rag/utils/config.py` to change:

```python
# Use reduced dataset (faster testing)
data_path: str = "data/argo_profiles_reduced.parquet"

# Faster retrieval
retrieval: RetrievalConfig = RetrievalConfig(
    top_k=3,  # Retrieve only 3 documents
    similarity_threshold=0.6  # Higher threshold
)

# Faster chunking
chunk_size: int = 300  # Smaller chunks

# Different LLM
llm.model_name: str = "llama2"
```

## Performance Tips

1. **Use reduced dataset first:**

   ```python
   loader = DataLoader("data/argo_profiles_reduced.parquet")
   ```

2. **Adjust chunk size** for quality vs speed trade-off:
   - Smaller chunks (300): Faster, more specific
   - Larger chunks (800): Slower, more context

3. **Reduce retrieval count:**

   ```python
   config.retrieval.top_k = 3  # Instead of 5
   ```

4. **Use GPU embeddings** (if available):
   - SentenceTransformer automatically uses GPU

## Next Steps

1. ✅ Configure paths (default: `data/` and `logs/`)
2. ✅ Install dependencies
3. ✅ Start Qdrant and Ollama services
4. ✅ Run `python main.py`
5. 📊 Evaluate using `rag/evaluation/` metrics
6. 📝 Check logs in `logs/` directory

---

For more details, see individual module documentation in the `rag/` directory.
