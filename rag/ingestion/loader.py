# loader.py - reads processed JSON

import json
from pathlib import Path
from typing import List, Dict, Any


class DataLoader:
    """Loads processed JSON data for ingestion."""
    
    def __init__(self, data_path: str):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the JSON data file or directory
        """
        self.data_path = Path(data_path)
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        """
        Load a single JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Parsed JSON data as dictionary
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            doc = json.load(f)
            
            # Validate document schema
            required_keys = {"text", "metadata"}
            if not required_keys.issubset(doc.keys()):
                raise ValueError(f"Invalid document format: {file_path}")
            
            return doc
    
    def load_all_documents(self) -> List[Dict[str, Any]]:
        """
        Load all JSON documents from the specified path.
        
        Returns:
            List of document dictionaries
        """
        documents = []
        
        if self.data_path.is_file():
            documents.append(self.load_json(self.data_path))
        elif self.data_path.is_dir():
            for json_file in self.data_path.glob('*.json'):
                documents.append(self.load_json(json_file))
        
        return documents
