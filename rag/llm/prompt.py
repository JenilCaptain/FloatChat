# prompt.py - system + RAG prompt

from typing import List, Dict, Any


class PromptTemplate:
    """Handles prompt templates for RAG system."""
    
    SYSTEM_PROMPT = f"""
    You are an expert RAG assistant that retrieves relevant context, reasons step-by-step, validates answers with sources, and avoids hallucination.

    Rules:
    - Accurate and based on the given context
    - Clear and concise
    - Informative and helpful
    - Avoid Hallucinations
    - Honest about limitations (if context doesn't contain relevant information)

    Handle every user query in a structured resoning style in the internal process:

    Analyze: Analyze each of the user query proeprly what he's trying to ask about
    Similarity Search: Based on the user query try searching the top content which is similar and only relevant to that query.
    Validate: Validate the fetched answers based on the user query.
    Give Result: At last based on the validation provide the user with the relevanted fetched information

    Output Format:
    Provide concise and upto point answers to the user in simple json format

    Tone of Answer:
    Don't have an over-friendly tone and be precise and concise and avoid hallucinations.

    Always cite information from the context when answering questions.
    If you cannot cite a source number, say "Source not found in context".

    """

    RAG_PROMPT_TEMPLATE = """
    Context: {context}

    Question: {question}

    Instructions: Answer the question based on the context provided above. If the context doesn't contain enough information to answer the question, say so clearly.

    Answer:

    """

    def __init__(self, system_prompt: str = None):
        """
        Initialize prompt template.
        
        Args:
            system_prompt: Custom system prompt (optional)
        """
        self.system_prompt = system_prompt or self.SYSTEM_PROMPT
    
    def format_rag_prompt(self, question: str, context: str) -> str:
        """
        Format RAG prompt with context and question.
        
        Args:
            question: User's question
            context: Retrieved context from documents
            
        Returns:
            Formatted prompt string
        """
        return self.RAG_PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )
    
    def format_chat_messages(self, question: str, context: str) -> List[Dict[str,str]]:
        """
        Format messages for chat-based LLM.
        
        Args:
            question: User's question
            context: Retrieved context from documents
            
        Returns:
            List of message dictionaries
        """
        user_content = f"""
        Context: {context}

        Question: {question}

        Please answer the question based on the context provided above."""
        
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content}
        ]
    
    def format_context_from_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieved results into context string.
        
        Args:
            results: List of retrieved documents with scores
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for idx, result in enumerate(results, 1):
            doc = result.get('document', {})
            text = doc.get('text', '')
            metadata = doc.get('metadata', {})
            
            context_part = f"[Source {idx}]\n{text}"
            
            if metadata:
                context_part += f"\nMetadata: {metadata}"
            
            context_parts.append(context_part)
        
        return "\n\n".join(context_parts)
