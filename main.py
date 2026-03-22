# main.py - Complete RAG Pipeline Setup & Execution

import os
import sys
from pathlib import Path
from datetime import datetime
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from rag.ingestion.loader import DataLoader
from rag.ingestion.chunker import TextChunker
from rag.embeddings.embedder import HuggingFaceEmbedder
from rag.vectordb.qdrant_client import QdrantClient
from rag.retrieval.retriever import Retriever
from rag.llm.ollama_llm import OllamaLLM
from rag.llm.prompt import PromptTemplate
from rag.pipeline.rag_pipeline import RAGPipeline
from rag.utils.config import RAGConfig
from rag.logs.query_logger import QueryLogger


def setup_pipeline(config: RAGConfig, force_reindex: bool = False) -> RAGPipeline:
    """
    Initialize and setup the complete RAG pipeline.
    
    Args:
        config: RAGConfig object with all settings
        force_reindex: If True, re-index data even if collection exists
        
    Returns:
        Initialized RAGPipeline
    """
    print("=" * 80)
    print("SETTING UP RAG PIPELINE")
    print("=" * 80)
    
    # Initialize embedder (needed for both setup and queries)
    print("\nInitializing embedding model...")
    embedder = HuggingFaceEmbedder(model_name=config.embedding.model_name)
    
    # Setup Vector Database
    print("Connecting to Qdrant vector database...")
    vector_db = QdrantClient(
        host=config.vectordb.host,
        port=config.vectordb.port,
        collection_name=config.vectordb.collection_name
    )
    
    # Check if collection already exists
    if vector_db.collection_exists() and not force_reindex:
        print("\n✓ Found existing collection in Qdrant!")
        info = vector_db.get_collection_info()
        print(f"  - Collection: {config.vectordb.collection_name}")
        print(f"  - Vectors: {info.get('vectors_count', 'N/A')}")
        print(f"  - Status: {info.get('status', 'N/A')}")
        print("\n⚡ Skipping data loading and indexing (using existing data)")
        print("   To force re-indexing, delete qdrant_storage/ or pass force_reindex=True")
    else:
        # Full setup: load, chunk, embed, index
        print("\n📊 No existing collection found. Starting full data indexing...")
        
        # 1. Load Data
        print("\n[1/5] Loading data from Parquet files...")
        master_file = Path(config.data_path) / "argo_profiles_reduced.parquet"
        data_loader = DataLoader(str(master_file), auto_transform=True)
        documents = data_loader.load_all_documents()
        print(f"✓ Loaded {len(documents)} documents from master dataset")
        
        # 2. Chunk Documents
        print("\n[2/5] Chunking documents into tokens...")
        chunker = TextChunker(
            chunk_size=config.chunker.chunk_size,
            chunk_overlap=config.chunker.chunk_overlap,
            encoding_name=config.chunker.encoding_name
        )
        chunked_docs = chunker.chunk_documents(documents)
        print(f"✓ Created {len(chunked_docs)} chunks from {len(documents)} documents")
        
        # 3. Generate Embeddings
        print("\n[3/5] Generating embeddings...")
        embeddings = embedder.embed_batch(
            [doc['text'] for doc in chunked_docs],
            batch_size=config.embedding.batch_size
        )
        print(f"✓ Generated embeddings with dimension: {embeddings.shape[1]}")
        
        # 4. Create Collection and Index
        print("\n[4/5] Creating collection and indexing documents...")
        vector_db.create_collection(
            vector_size=embeddings.shape[1],
            distance=config.vectordb.distance_metric
        )
        vector_db.index_documents(chunked_docs, embeddings)
    
    # 5. Initialize Retriever and LLM (always needed)
    print("\n[5/5] Initializing retriever and language model...")
    retriever = Retriever(vector_db, embedder)
    llm = OllamaLLM(
        model_name=config.llm.model_name,
        base_url=config.llm.base_url
    )
    prompt_template = PromptTemplate()
    pipeline = RAGPipeline(retriever, llm, prompt_template)
    print("✓ RAG Pipeline ready!")
    
    print("\n" + "=" * 80)
    print("READY FOR QUERIES")
    print("=" * 80)
    
    return pipeline


def run_interactive_query(pipeline: RAGPipeline, logger: QueryLogger, config: RAGConfig):
    """
    Run interactive query loop.
    
    Args:
        pipeline: RAGPipeline instance
        logger: QueryLogger instance
        config: RAGConfig object
    """
    print("\n" + "=" * 80)
    print("INTERACTIVE RAG QUERY MODE")
    print("=" * 80)
    print("Type 'exit' to quit, 'help' for commands\n")
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if query.lower() == 'exit':
                print("Exiting RAG system...")
                break
            
            if query.lower() == 'help':
                print("\nAvailable commands:")
                print("  exit      - Exit the program")
                print("  help      - Show this help message")
                print("  history   - Show recent queries (last 5)")
                print("\nOtherwise, type your query about oceanographic data.\n")
                continue
            
            if query.lower() == 'history':
                history = logger.get_query_history()
                print(f"\nLast {min(5, len(history))} queries:")
                for entry in history[-5:]:
                    print(f"  - {entry['timestamp']}: {entry['query'][:60]}...")
                print()
                continue
            
            if not query:
                continue
            
            # Execute query
            print("\n[Processing query...]")
            start_time = time.time()

            # # error check:
            # print("hey, in mAIN 1")
            # # passed
            
            result = pipeline.query(
                query,
                top_k=config.retrieval.top_k,
                temperature=config.llm.temperature
            )

            # # error check:
            # print("hey, in mAIN 2") 
            
            
            elapsed_time = time.time() - start_time
            
            # Log the query
            logger.log_query(
                query=query,
                retrieved_docs=result['sources'],
                answer=result['answer'],
                metadata={'processing_time': elapsed_time}
            )
            
            # Display results
            print("\n" + "-" * 80)
            print("ANSWER:")
            print("-" * 80)
            print(result['answer'])
            print("-" * 80)
            print(f"\nSources ({len(result['sources'])} documents retrieved in {elapsed_time:.2f}s):")
            for i, source in enumerate(result['sources'], 1):
                score = source['score']
                metadata = source['document'].get('metadata', {})
                print(f"  [{i}] Score: {score:.3f} | {str(metadata)[:70]}...")
            print()
            
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            import traceback
            print(f"Error: {e}")
            print("\nFull traceback:")
            traceback.print_exc()
            continue


def main():
    """Main function to run the RAG pipeline."""
    
    # Load configuration
    config = RAGConfig()
    
    print(f"\n✓ Configuration loaded:")
    print(f"  - Data path: {config.data_path}")
    print(f"  - LLM model: {config.llm.model_name}")
    print(f"  - Embedding model: {config.embedding.model_name}")
    print(f"  - Chunk size: {config.chunker.chunk_size} tokens")
    print(f"  - Top-K retrieval: {config.retrieval.top_k}")
    
    # Setup RAG Pipeline
    try:
        pipeline = setup_pipeline(config)
    except Exception as e:
        print(f"\n❌ Error setting up pipeline: {e}")
        print("\nMake sure:")
        print("  1. Qdrant is running: docker run -d -p 6333:6333 qdrant/qdrant")
        print("  2. Ollama is running: ollama serve")
        print("  3. Parquet files exist in 'data/' directory")
        return
    
    # Setup logger
    logger = QueryLogger(log_dir=config.logs_path, log_to_file=True, log_to_console=True)
    
    # Run interactive query mode
    run_interactive_query(pipeline, logger, config)


if __name__ == "__main__":
    main()
