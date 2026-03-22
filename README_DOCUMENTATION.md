# 📚 RAG Pipeline Documentation Index

## 🚀 Start Here

1. **[QUICK_START.md](QUICK_START.md)** - 5-minute overview
   - What's been done
   - How to run
   - Example queries

2. **[CONFIGURATION_SUMMARY.md](CONFIGURATION_SUMMARY.md)** - Visual overview
   - Component diagram
   - Data flow
   - Configuration checklist

## 📖 Comprehensive Guides

3. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Full setup & configuration
   - Prerequisites
   - Services to run
   - Environment variables
   - Troubleshooting

4. **[PATH_CONFIGURATION.md](PATH_CONFIGURATION.md)** - Path details
   - What changed
   - Where changes were made
   - File modifications summary

5. **[CONFIGURATION_COMPLETE.md](CONFIGURATION_COMPLETE.md)** - Completion checklist
   - All changes summary
   - Directory structure
   - Verification steps

## 🔧 Technical Reference

### Configuration

- **File:** `rag/utils/config.py`
- **Data path:** `"data"`
- **Logs path:** `"logs"`
- **Vector DB:** `localhost:6333`
- **LLM:** `phi3`

### Main Entry Point

- **File:** `main.py`
- **Command:** `python main.py`
- **Features:** Full pipeline setup + interactive query mode

### Dependencies

- **File:** `requirements.txt`
- **Install:** `pip install -r requirements.txt`

## 📁 System Architecture

### Data Pipeline

```
data/*.parquet
  ↓ (DataLoader)
text + metadata
  ↓ (TextChunker - token-based)
chunks
  ↓ (HuggingFaceEmbedder - normalized)
embeddings
  ↓ (QdrantClient - UUID-based)
indexed vectors
  ↓ (Retriever - similarity search)
results
  ↓ (OllamaLLM - Mistral 7B)
answer
  ↓ (QueryLogger)
logs/
```

### Module Descriptions

#### Ingestion

- **loader.py** - Reads Parquet files, auto-transforms to RAG format
- **chunker.py** - Token-based text splitting (500 tokens, 100 overlap)

#### Embeddings

- **embedder.py** - HuggingFace embeddings with normalization

#### Vector Database

- **qdrant_client.py** - Qdrant integration with UUID tracking

#### Retrieval

- **retriever.py** - Similarity search and document retrieval

#### LLM

- **ollama_llm.py** - Ollama wrapper for Mistral 7B
- **prompt.py** - Prompt templates with anti-hallucination guardrail

#### Pipeline

- **rag_pipeline.py** - End-to-end orchestration

#### Evaluation

- **precision_at_k.py** - Precision metrics
- **recall_at_k.py** - Recall metrics and F1 score

#### Logging

- **query_logger.py** - JSONL-based query logging

#### Utils

- **config.py** - Centralized configuration

## 🎯 Quick Reference

### How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start services
docker run -d -p 6333:6333 qdrant/qdrant  # Terminal 1
ollama serve                               # Terminal 2

# 3. Run pipeline
python main.py                             # Terminal 3
```

### Data Sources

- `data/argo_profiles_master.parquet` (749,465 profiles)
- `data/argo_profiles_reduced.parquet` (55,819 aggregated records)

### Output

- Logs: `logs/rag_queries_YYYYMMDD.jsonl`
- Format: JSONL (one JSON object per line)

### Key Settings

- Data path: `data/`
- Chunk size: 500 tokens
- Top-K retrieval: 5 documents
- LLM temperature: 0.7
- Vector similarity: Cosine (normalized)

## ✅ Configuration Status

| Component          | Status      | Details                       |
| ------------------ | ----------- | ----------------------------- |
| Data loading       | ✅ Complete | Parquet + auto-transform      |
| Text chunking      | ✅ Complete | Token-based, 500 tokens       |
| Embeddings         | ✅ Complete | Normalized, cosine similarity |
| Vector DB          | ✅ Complete | Qdrant with UUID tracking     |
| LLM integration    | ✅ Complete | Mistral 7B with guardrails    |
| Query logging      | ✅ Complete | JSONL format to logs/         |
| Evaluation metrics | ✅ Complete | Precision & recall @K         |
| Entry point        | ✅ Complete | main.py with full setup       |

## 🚨 External Requirements

Only install/run these (everything else is configured):

1. **Docker** - For Qdrant container

   ```bash
   docker run -d -p 6333:6333 qdrant/qdrant
   ```

2. **Ollama** - For LLM serving
   ```bash
   ollama pull phi3
   ollama serve
   ```

## 📊 Files Created/Modified

### New Files (✨)

- `main.py` - Main entry point
- `requirements.txt` - Python dependencies
- `quick_start.ps1` - Setup script
- `SETUP_GUIDE.md` - Comprehensive guide
- `PATH_CONFIGURATION.md` - Configuration details
- `QUICK_START.md` - Quick reference
- `CONFIGURATION_COMPLETE.md` - Checklist
- `CONFIGURATION_SUMMARY.md` - Visual summary
- `README_DOCUMENTATION.md` - This file

### Modified Files (✏️)

- `rag/utils/config.py` - Updated paths
- `rag/ingestion/loader.py` - Parquet support
- `rag/ingestion/chunker.py` - Token-based chunking
- `rag/embeddings/embedder.py` - Normalized embeddings
- `rag/vectordb/qdrant_client.py` - UUID support
- `rag/llm/ollama_llm.py` - Mistral default
- `rag/llm/prompt.py` - Anti-hallucination guardrail

## 🔍 Document Navigation

### For Quick Setup

→ [QUICK_START.md](QUICK_START.md)

### For Full Configuration

→ [SETUP_GUIDE.md](SETUP_GUIDE.md)

### For Visual Overview

→ [CONFIGURATION_SUMMARY.md](CONFIGURATION_SUMMARY.md)

### For Path Details

→ [PATH_CONFIGURATION.md](PATH_CONFIGURATION.md)

### For Completion Checklist

→ [CONFIGURATION_COMPLETE.md](CONFIGURATION_COMPLETE.md)

## 💡 Example Queries

Once running, ask:

- "What is the average temperature at different depths?"
- "Tell me about salinity patterns in tropical regions"
- "Which areas have the highest water pressure?"
- "Describe the oceanographic conditions in the Indian Ocean"
- "What are the seasonal variations in temperature?"

## 🛠️ Troubleshooting

**"Connection refused"**
→ Start Qdrant: `docker run -d -p 6333:6333 qdrant/qdrant`

**"Model not found"**
→ Pull model: `ollama pull phi3`

**"No module named 'sentence_transformers'"**
→ Install: `pip install sentence-transformers`

**Slow first run?**
→ Normal - embedding model downloads (~100MB). Next runs are fast.

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

## 📞 Support

All modules have detailed docstrings:

```python
from rag.ingestion.loader import DataLoader
help(DataLoader.load_parquet)
```

Check inline comments in source files for implementation details.

## ✨ Summary

Your RAG pipeline is **fully configured** with:

- ✅ Correct data paths (`data/` → `logs/`)
- ✅ Parquet file support with auto-transform
- ✅ Token-aware chunking
- ✅ Normalized embeddings
- ✅ UUID-based tracking
- ✅ Mistral 7B LLM
- ✅ Anti-hallucination guardrails
- ✅ Query logging system
- ✅ Evaluation metrics
- ✅ Interactive interface

**Ready to run:**

```bash
python main.py
```

---

**Last Updated:** January 28, 2026
**Status:** ✅ Ready for Production
