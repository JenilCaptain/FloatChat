# loader.py - reads processed Parquet files

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import json


class DataLoader:
    """Loads processed Parquet data for ingestion and transforms into RAG format."""
    
    def __init__(self, data_path: str, auto_transform: bool = True):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the Parquet data file or directory
            auto_transform: Automatically transform oceanographic data to text format
        """
        self.data_path = Path(data_path)
        self.auto_transform = auto_transform
    
    def _transform_row_to_text(self, row: Dict[str, Any]) -> str:
        """
        Transform a single data row into descriptive text.
        
        Args:
            row: Dictionary containing oceanographic data
            
        Returns:
            Formatted text description
        """
        text_parts = []
        
        # Handle master file format (detailed profiles)
        if 'date' in row and 'latitude' in row:
            text_parts.append(f"Oceanographic measurement recorded on {row.get('date', 'unknown date')}")
            text_parts.append(f"Location: Latitude {row.get('latitude', 'N/A')}°, Longitude {row.get('longitude', 'N/A')}°")
            
            if 'depth_m' in row and pd.notna(row['depth_m']):
                text_parts.append(f"Depth: {row['depth_m']} meters")
            elif 'pressure' in row and pd.notna(row['pressure']):
                text_parts.append(f"Pressure: {row['pressure']} dbar")
            
            if 'temperature' in row and pd.notna(row['temperature']):
                text_parts.append(f"Temperature: {row['temperature']:.2f}°C")
            
            if 'salinity' in row and pd.notna(row['salinity']):
                text_parts.append(f"Salinity: {row['salinity']:.2f} PSU")
            
            if 'platform' in row:
                text_parts.append(f"Platform ID: {row['platform']}")
        
        # Handle reduced file format (aggregated data)
        elif 'month' in row and 'lat_bin' in row:
            text_parts.append(f"Aggregated oceanographic data for {row.get('month', 'unknown period')}")
            text_parts.append(f"Grid location: Latitude bin {row.get('lat_bin', 'N/A')}°, Longitude bin {row.get('lon_bin', 'N/A')}°")
            
            if 'depth_zone' in row:
                text_parts.append(f"Depth zone: {row['depth_zone']}")
            
            if 'temperature' in row and pd.notna(row['temperature']):
                text_parts.append(f"Average temperature: {row['temperature']:.2f}°C")
            
            if 'salinity' in row and pd.notna(row['salinity']):
                text_parts.append(f"Average salinity: {row['salinity']:.2f} PSU")
        
        # Fallback for any other format
        else:
            text_parts.append("Oceanographic measurement:")
            for key, value in row.items():
                if pd.notna(value) and key not in ['text', 'metadata']:
                    text_parts.append(f"{key}: {value}")
        
        return ". ".join(text_parts) + "."
    
    def _extract_metadata(self, row: Dict[str, Any], source_file: str) -> Dict[str, Any]:
        """
        Extract metadata from a data row.
        
        Args:
            row: Dictionary containing oceanographic data
            source_file: Name of the source file
            
        Returns:
            Metadata dictionary
        """
        metadata = {
            'source_file': source_file
        }
        
        # Add relevant metadata fields based on available columns
        metadata_fields = ['date', 'latitude', 'longitude', 'depth_m', 'pressure', 
                          'platform', 'cycle', 'data_mode', 'month', 'lat_bin', 
                          'lon_bin', 'depth_zone']
        
        for field in metadata_fields:
            if field in row and pd.notna(row[field]):
                # Convert to native Python types for JSON serialization
                value = row[field]
                if isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
                    value = str(value)
                elif isinstance(value, pd.Period):
                    value = str(value.to_timestamp())  # Convert Period to Timestamp then to string
                elif isinstance(value, (pd.Int64Dtype, pd.Float64Dtype)):
                    value = float(value) if pd.notna(value) else None
                metadata[field] = value
        
        return metadata
    
    def load_parquet(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load a single Parquet file and transform to RAG format.
        
        Args:
            file_path: Path to the Parquet file
            
        Returns:
            List of document dictionaries (one per row)
        """
        try:
            df = pd.read_parquet(file_path)
        except Exception as e:
            raise ValueError(f"Error reading Parquet file {file_path}: {e}")
        
        # Check if already in RAG format
        has_rag_format = {'text', 'metadata'}.issubset(df.columns)
        
        if has_rag_format and not self.auto_transform:
            # Already in correct format
            documents = df.to_dict('records')
        elif self.auto_transform:
            # Transform oceanographic data to RAG format
            documents = []
            source_file_name = Path(file_path).name
            
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                
                # Generate text and metadata
                doc = {
                    'text': self._transform_row_to_text(row_dict),
                    'metadata': self._extract_metadata(row_dict, source_file_name)
                }
                documents.append(doc)
            
            print(f"Transformed {len(documents)} rows from {source_file_name} into RAG format")
        else:
            raise ValueError(f"File {file_path} does not have required 'text' and 'metadata' columns and auto_transform is disabled")
        
        return documents
    
    def load_all_documents(self) -> List[Dict[str, Any]]:
        """
        Load all Parquet documents from the specified path.
        
        Returns:
            List of document dictionaries
        """
        documents = []
        
        if self.data_path.is_file():
            documents.extend(self.load_parquet(self.data_path))
        elif self.data_path.is_dir():
            for parquet_file in self.data_path.glob('*.parquet'):
                documents.extend(self.load_parquet(parquet_file))
        
        return documents
