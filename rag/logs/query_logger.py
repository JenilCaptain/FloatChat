# query_logger.py - Logging for RAG queries and responses

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class QueryLogger:
    """Logs RAG queries, retrieved documents, and answers for debugging and monitoring."""
    
    def __init__(self, log_dir: str = "logs", log_to_file: bool = True, log_to_console: bool = True):
        """
        Initialize the query logger.
        
        Args:
            log_dir: Directory to store log files
            log_to_file: Whether to log to file
            log_to_console: Whether to log to console
        """
        self.log_dir = Path(log_dir)
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        
        # Create logs directory if it doesn't exist
        if self.log_to_file:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logger
        self.logger = logging.getLogger("RAGQueryLogger")
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers = []
        
        # Add console handler
        if self.log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # Add file handler
        if self.log_to_file:
            log_file = self.log_dir / f"rag_queries_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def log_query(
        self, 
        query: str, 
        retrieved_docs: List[Dict[str, Any]], 
        answer: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a complete RAG query-response cycle.
        
        Args:
            query: User's query
            retrieved_docs: List of retrieved documents with scores
            answer: Generated answer
            metadata: Additional metadata (e.g., retrieval time, generation time)
        """
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "query": query,
            "retrieved_docs": retrieved_docs,
            "answer": answer,
            "metadata": metadata or {}
        }
        
        # Log to console/file
        self.logger.info(f"Query: {query}")
        self.logger.info(f"Retrieved {len(retrieved_docs)} documents")
        self.logger.info(f"Answer: {answer[:100]}...")  # First 100 chars
        
        # Save detailed JSON log
        if self.log_to_file:
            json_log_file = self.log_dir / f"rag_queries_{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(json_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def log_retrieval(self, query: str, retrieved_docs: List[Dict[str, Any]], retrieval_time: float):
        """
        Log only the retrieval step.
        
        Args:
            query: User's query
            retrieved_docs: List of retrieved documents with scores
            retrieval_time: Time taken for retrieval (in seconds)
        """
        self.logger.info(
            f"Retrieval - Query: {query} | Retrieved: {len(retrieved_docs)} docs | Time: {retrieval_time:.3f}s"
        )
        
        if self.log_to_file:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "retrieval",
                "query": query,
                "retrieved_docs": retrieved_docs,
                "retrieval_time": retrieval_time
            }
            
            json_log_file = self.log_dir / f"retrieval_{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(json_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def log_generation(self, query: str, context: str, answer: str, generation_time: float):
        """
        Log only the generation step.
        
        Args:
            query: User's query
            context: Context provided to LLM
            answer: Generated answer
            generation_time: Time taken for generation (in seconds)
        """
        self.logger.info(
            f"Generation - Query: {query} | Answer length: {len(answer)} chars | Time: {generation_time:.3f}s"
        )
        
        if self.log_to_file:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "generation",
                "query": query,
                "context": context,
                "answer": answer,
                "generation_time": generation_time
            }
            
            json_log_file = self.log_dir / f"generation_{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(json_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def log_error(self, query: str, error: Exception, stage: str = "unknown"):
        """
        Log errors during RAG pipeline execution.
        
        Args:
            query: User's query that caused the error
            error: Exception that was raised
            stage: Stage where error occurred (retrieval, generation, etc.)
        """
        self.logger.error(f"Error in {stage} - Query: {query} | Error: {str(error)}")
        
        if self.log_to_file:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "error",
                "stage": stage,
                "query": query,
                "error": str(error),
                "error_type": type(error).__name__
            }
            
            json_log_file = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(json_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_query_history(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve query history from logs.
        
        Args:
            date: Date in YYYYMMDD format (default: today)
            
        Returns:
            List of query log entries
        """
        if not self.log_to_file:
            raise RuntimeError("File logging is not enabled")
        
        date_str = date or datetime.now().strftime('%Y%m%d')
        json_log_file = self.log_dir / f"rag_queries_{date_str}.jsonl"
        
        if not json_log_file.exists():
            return []
        
        history = []
        with open(json_log_file, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line))
        
        return history
