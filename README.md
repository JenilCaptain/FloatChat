# AgroOcean Project - RAG Pipeline

## 📌 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline for oceanographic data analysis using Argo float profiles. The system transforms raw oceanographic measurements into a searchable knowledge base and provides AI-powered question-answering capabilities.

## 🚀 Quick Start

### 0. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
# source venv/bin/activate
```

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Services (in separate terminals)

```bash
# Terminal 1: Vector Database
docker run -d -p 6333:6333 qdrant/qdrant

# Terminal 2: Language Model Server
ollama serve

# Terminal 3: Run Pipeline
python main.py
```

### 3. Ask Questions

```
Query: What is the average temperature at different depths?
Query: Tell me about salinity patterns in tropical regions
Query: Which areas have the highest water pressure?
```

## 📁 Project Structure

```
AgroOcean Project/
├── data/                           # Your oceanographic data
│   ├── argo_profiles_master.parquet      (749K profiles)
│   └── argo_profiles_reduced.parquet     (56K aggregates)
├── rag/                            # RAG system components
│   ├── ingestion/
│   │   ├── loader.py              # Parquet loading + transform
│   │   └── chunker.py             # Token-based chunking
│   ├── embeddings/
│   │   └── embedder.py            # HuggingFace embeddings
│   ├── vectordb/
│   │   └── qdrant_client.py       # Qdrant integration
│   ├── retrieval/
│   │   └── retriever.py           # Similarity search
│   ├── llm/
│   │   ├── ollama_llm.py          # Mistral 7B wrapper
│   │   └── prompt.py              # Prompt templates
│   ├── pipeline/
│   │   └── rag_pipeline.py        # Main orchestration
│   ├── evaluation/
│   │   ├── precision_at_k.py
│   │   └── recall_at_k.py
│   ├── logs/
│   │   └── query_logger.py        # Query logging
│   └── utils/
│       └── config.py              # Configuration
├── logs/                           # Query logs (auto-created)
├── main.py                         # Entry point
├── requirements.txt                # Dependencies
└── Documentation/
    ├── QUICK_START.md             # Quick reference
    ├── SETUP_GUIDE.md             # Comprehensive setup
    ├── PATH_CONFIGURATION.md      # Configuration details
    └── [4 more guides]
```

## 🔧 Configuration

All paths are automatically configured in `rag/utils/config.py`:

```python
data_path: str = "data"              # Parquet files location
logs_path: str = "logs"              # Query logs location
vectordb: "localhost:6333"           # Qdrant database
llm: "phi3"     # Language model
```

## 📊 System Architecture

```
Parquet Data (data/)
    ↓
[DataLoader] Auto-transform to text
    ↓
[TextChunker] Token-based (500 tokens)
    ↓
[HuggingFaceEmbedder] Normalized vectors
    ↓
[QdrantClient] Index with UUID
    ↓
[Retriever] Similarity search
    ↓
[OllamaLLM] Generate answer (Mistral 7B)
    ↓
[QueryLogger] Save to logs/
```

## ✨ Key Features

✅ **Automatic Data Transformation** - Oceanographic data → RAG-ready text
✅ **Token-Aware Chunking** - Better semantic coherence than character splitting
✅ **Normalized Embeddings** - Optimal cosine similarity
✅ **UUID Tracking** - No data loss on re-indexing
✅ **Anti-Hallucination** - Forced citation of sources
✅ **Comprehensive Logging** - JSONL logs for debugging
✅ **Evaluation Metrics** - Precision@K and Recall@K
✅ **Interactive Interface** - Chat-like query mode

## 📚 Documentation

| Document                                               | Purpose               |
| ------------------------------------------------------ | --------------------- |
| [QUICK_START.md](QUICK_START.md)                       | 5-minute overview     |
| [SETUP_GUIDE.md](SETUP_GUIDE.md)                       | Comprehensive setup   |
| [PATH_CONFIGURATION.md](PATH_CONFIGURATION.md)         | Configuration details |
| [CONFIGURATION_COMPLETE.md](CONFIGURATION_COMPLETE.md) | Completion checklist  |
| [CONFIGURATION_SUMMARY.md](CONFIGURATION_SUMMARY.md)   | Visual overview       |
| [README_DOCUMENTATION.md](README_DOCUMENTATION.md)     | Documentation index   |
| [FINAL_SUMMARY.md](FINAL_SUMMARY.md)                   | Summary               |

## 🛠️ Requirements

**External Services:**

- Docker (for Qdrant)
- Ollama (for LLM serving)
- Python 3.8+
- 8GB+ RAM

**Python Packages:** See [requirements.txt](requirements.txt)

## 📖 Data Format

### Input (Parquet)

- **Master:** 749,465 individual profiles with detailed measurements
- **Reduced:** 55,819 monthly aggregates by grid cells

### Auto-Transformation

```
Raw: {temperature: 28.86, salinity: 35.35, latitude: -0.1, longitude: 77.2}
    ↓
Text: "Oceanographic measurement recorded on 2002-11-21. Location:
Latitude -0.1°, Longitude 77.2°. Temperature: 28.86°C. Salinity: 35.35 PSU."
```

## 🔍 Evaluation

Evaluate RAG quality using built-in metrics:

```python
from rag.evaluation.precision_at_k import precision_at_k
from rag.evaluation.recall_at_k import recall_at_k

precision = precision_at_k(retrieved_ids, relevant_ids, k=5)
recall = recall_at_k(retrieved_ids, relevant_ids, k=5)
```

## 🐛 Troubleshooting

**"Connection refused"** → Start Qdrant: `docker run -d -p 6333:6333 qdrant/qdrant`

**"Model not found"** → Pull model: `ollama pull phi3`

**"No module named..."** → Install dependencies: `pip install -r requirements.txt`

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more help.

## 📝 Log Files

Query logs are automatically saved in JSONL format:

```
logs/
├── rag_queries_20260128.jsonl       # Complete query-response cycles
├── retrieval_20260128.jsonl         # Retrieved documents
├── generation_20260128.jsonl        # LLM generation details
└── errors_20260128.jsonl            # Error logs
```

## 🎯 Example Queries

Once running, ask questions like:

- "What is the average temperature at different depths?"
- "Tell me about salinity patterns in tropical regions"
- "Which areas have the highest water pressure?"
- "Describe seasonal variations in oceanographic parameters"

## ✅ Status

**Configuration:** ✅ Complete
**All Paths:** ✅ Correct
**Components:** ✅ Integrated
**Ready to Run:** ✅ Yes

## 🚀 Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Start Qdrant: `docker run -d -p 6333:6333 qdrant/qdrant`
3. Start Ollama: `ollama serve`
4. Run pipeline: `python main.py`
5. Start querying your oceanographic data!

## 📞 Support

- Check module docstrings: `python -c "from rag.ingestion.loader import DataLoader; help(DataLoader)"`
- Read documentation files in the root directory
- Check inline comments in source files

## 📄 License

[See LICENSE file](LICENSE)

## 👥 Team

6th Semester Group Project - AgroOcean

---

**Last Updated:** January 28, 2026
**Status:** ✅ Ready for Production
