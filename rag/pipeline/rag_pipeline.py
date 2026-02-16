# rag_pipeline.py - end-to-end RAG flow

from typing import Dict, Any, Optional


class RAGPipeline:
    """End-to-end RAG pipeline orchestrator."""
    
    def __init__(self, retriever, llm, prompt_template):
        """
        Initialize RAG pipeline.
        
        Args:
            retriever: Document retriever instance
            llm: Language model instance
            prompt_template: Prompt template instance
        """
        self.retriever = retriever
        self.llm = llm
        self.prompt_template = prompt_template
    
    def query(self, question: str, top_k: int = 5, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Execute full RAG pipeline for a query.
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            temperature: LLM sampling temperature
            
        Returns:
            Dictionary containing answer and metadata
        """
        
        # error checks
        # print(type(self.retriever))
        # print(hasattr(self.retriever, "retrieve"))
        # print(dir(self.retriever))
        # passed

        # # error check:
        # print("hey, in rag_pipeline 1 line 36")
        # # Debug vector_db object
        # print(f"Vector DB type: {type(self.retriever.vector_db)}")
        # print(f"Has search method: {hasattr(self.retriever.vector_db, 'search')}")
        # print(f"Vector DB methods: {[m for m in dir(self.retriever.vector_db) if not m.startswith('_')]}")
        # # passed

        # Step 1: Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(question, top_k=top_k)

        # # error check:
        # print("hey, in rag_pipeline 2 line 42")
        
        if not retrieved_docs:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "sources": [],
                "question": question
            }
        
        # Step 2: Format context from retrieved documents
        context = self.prompt_template.format_context_from_results(retrieved_docs)
        
        # Step 3: Generate prompt
        prompt = self.prompt_template.format_rag_prompt(question, context)
        
        # Step 4: Generate answer using LLM
        answer = self.llm.generate(prompt, temperature=temperature)
        
        # Step 5: Return result with metadata
        return {
            "answer": answer,
            "sources": retrieved_docs,
            "question": question,
            "context": context
        }
    
    def query_with_chat(self, question: str, top_k: int = 5, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Execute RAG pipeline using chat completion.
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            temperature: LLM sampling temperature
            
        Returns:
            Dictionary containing answer and metadata
        """
        # Retrieve and format context

        

        retrieved_docs = self.retriever.retrieve(question, top_k=top_k)
        
        # # error check:
        # print("hey, in rag_pipeline 2")

        if not retrieved_docs:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "sources": [],
                "question": question
            }
        
        context = self.prompt_template.format_context_from_results(retrieved_docs)
        
        # Format chat messages
        messages = self.prompt_template.format_chat_messages(question, context)
        
        # Generate answer
        answer = self.llm.chat(messages, temperature=temperature)
        
        return {
            "answer": answer,
            "sources": retrieved_docs,
            "question": question,
            "context": context
        }
    
    def stream_query(self, question: str, top_k: int = 5, temperature: float = 0.7):
        """
        Stream RAG pipeline response.
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            temperature: LLM sampling temperature
            
        Yields:
            Answer chunks
        """
        # Retrieve and format context
        retrieved_docs = self.retriever.retrieve(question, top_k=top_k)
        
        if not retrieved_docs:
            yield "I couldn't find any relevant information to answer your question."
            return
        
        context = self.prompt_template.format_context_from_results(retrieved_docs)
        prompt = self.prompt_template.format_rag_prompt(question, context)
        
        # Stream answer
        for chunk in self.llm.stream_generate(prompt, temperature=temperature):
            yield chunk
