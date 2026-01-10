# precision_at_k.py - Precision@K metric for RAG evaluation

from typing import List, Set, Union


def precision_at_k(retrieved_docs: List[str], relevant_docs: Set[str], k: int = 5) -> float:
    """
    Calculate Precision@K metric.
    
    Precision@K measures the proportion of retrieved documents that are relevant
    among the top-k retrieved documents.
    
    Formula: Precision@K = (Number of relevant documents in top-K) / K
    
    Args:
        retrieved_docs: List of retrieved document IDs (in ranked order)
        relevant_docs: Set of ground truth relevant document IDs
        k: Number of top documents to consider
        
    Returns:
        Precision@K score (between 0 and 1)
        
    Example:
        >>> retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        >>> relevant = {"doc1", "doc3", "doc6"}
        >>> precision_at_k(retrieved, relevant, k=5)
        0.4  # 2 out of 5 retrieved docs are relevant
    """
    if k <= 0:
        raise ValueError("k must be positive")
    
    if not retrieved_docs:
        return 0.0
    
    # Consider only top-k documents
    top_k_docs = retrieved_docs[:k]
    
    # Count how many retrieved docs are relevant
    relevant_retrieved = sum(1 for doc in top_k_docs if doc in relevant_docs)
    
    # Calculate precision
    precision = relevant_retrieved / k
    
    return precision


def mean_precision_at_k(
    all_retrieved_docs: List[List[str]], 
    all_relevant_docs: List[Set[str]], 
    k: int = 5
) -> float:
    """
    Calculate Mean Precision@K across multiple queries.
    
    Args:
        all_retrieved_docs: List of retrieved document lists for each query
        all_relevant_docs: List of relevant document sets for each query
        k: Number of top documents to consider
        
    Returns:
        Mean Precision@K score across all queries
        
    Example:
        >>> retrieved = [
        ...     ["doc1", "doc2", "doc3"],
        ...     ["doc4", "doc5", "doc6"]
        ... ]
        >>> relevant = [
        ...     {"doc1", "doc3"},
        ...     {"doc5", "doc7"}
        ... ]
        >>> mean_precision_at_k(retrieved, relevant, k=3)
        0.5  # Average of (2/3) and (1/3)
    """
    if len(all_retrieved_docs) != len(all_relevant_docs):
        raise ValueError("Number of retrieved and relevant document lists must match")
    
    if not all_retrieved_docs:
        return 0.0
    
    precisions = [
        precision_at_k(retrieved, relevant, k)
        for retrieved, relevant in zip(all_retrieved_docs, all_relevant_docs)
    ]
    
    return sum(precisions) / len(precisions)


def precision_at_various_k(
    retrieved_docs: List[str], 
    relevant_docs: Set[str], 
    k_values: List[int] = [1, 3, 5, 10]
) -> dict:
    """
    Calculate Precision@K for multiple k values.
    
    Args:
        retrieved_docs: List of retrieved document IDs (in ranked order)
        relevant_docs: Set of ground truth relevant document IDs
        k_values: List of k values to evaluate
        
    Returns:
        Dictionary mapping k to Precision@K score
        
    Example:
        >>> retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        >>> relevant = {"doc1", "doc3", "doc5"}
        >>> precision_at_various_k(retrieved, relevant, k_values=[1, 3, 5])
        {1: 1.0, 3: 0.667, 5: 0.6}
    """
    results = {}
    
    for k in k_values:
        if k <= len(retrieved_docs):
            results[k] = precision_at_k(retrieved_docs, relevant_docs, k)
        else:
            # If k > number of retrieved docs, use all retrieved docs
            results[k] = precision_at_k(retrieved_docs, relevant_docs, len(retrieved_docs))
    
    return results
