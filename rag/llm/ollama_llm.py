# ollama_llm.py - LLM wrapper

from typing import Optional, Dict, Any


class OllamaLLM:
    """Wrapper for Ollama LLM."""
    
    def __init__(self, model_name: str = "phi3", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama LLM.
        
        Args:
            model_name: Name of the Ollama model to use
            base_url: Base URL for Ollama API
        """
        self.model_name = model_name
        self.base_url = base_url
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Ollama client."""
        try:
            import ollama
            self.client = ollama
            print(f"Initialized Ollama client with model: {self.model_name}")
        except ImportError:
            print("ollama not installed. Run: pip install ollama")
        except Exception as e:
            print(f"Error initializing Ollama: {e}")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: Optional[int] = None) -> str:
        """
        Generate text using Ollama.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        if self.client is None:
            raise RuntimeError("Ollama client not initialized")
        
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': temperature,
                    'num_predict': max_tokens
                } if max_tokens else {'temperature': temperature}
            )
            
            return response['response']
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""
    
    def chat(self, messages: list, temperature: float = 0.7) -> str:
        """
        Chat completion using Ollama.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        if self.client is None:
            raise RuntimeError("Ollama client not initialized")
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                options={'temperature': temperature}
            )
            
            return response['message']['content']
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return ""
    
    def stream_generate(self, prompt: str, temperature: float = 0.7):
        """
        Stream generation using Ollama.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            
        Yields:
            Generated text chunks
        """
        if self.client is None:
            raise RuntimeError("Ollama client not initialized")
        
        try:
            stream = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                stream=True,
                options={'temperature': temperature}
            )
            
            for chunk in stream:
                yield chunk['response']
        except Exception as e:
            print(f"Error in streaming: {e}")
