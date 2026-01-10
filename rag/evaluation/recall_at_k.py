# recall_at_k.py - Recall@K metric for RAG evaluation

from typing import List, Set


def recall_at_k(retrieved_docs: List[str], relevant_docs: Set[str], k: int = 5) -> float:
    """
    Calculate Recall@K metric.
    
    Recall@K measures the proportion of relevant documents that are retrieved
    among the top-k retrieved documents.
    
    Formula: Recall@K = (Number of relevant documents in top-K) / (Total number of relevant documents)
    
    Args:
        retrieved_docs: List of retrieved document IDs (in ranked order)
        relevant_docs: Set of ground truth relevant document IDs
        k: Number of top documents to consider
        
    Returns:
        Recall@K score (between 0 and 1)
        
    Example:
        >>> retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        >>> relevant = {"doc1", "doc3", "doc6"}
        >>> recall_at_k(retrieved, relevant, k=5)
        0.667  # 2 out of 3 relevant docs are retrieved
    """
    if k <= 0:
        raise ValueError("k must be positive")
    
    if not relevant_docs:
        return 0.0
    
    if not retrieved_docs:
        return 0.0
    
    # Consider only top-k documents
    top_k_docs = retrieved_docs[:k]
    
    # Count how many relevant docs were retrieved
    relevant_retrieved = sum(1 for doc in top_k_docs if doc in relevant_docs)
    
    # Calculate recall
    recall = relevant_retrieved / len(relevant_docs)
    
    return recall


def mean_recall_at_k(
    all_retrieved_docs: List[List[str]], 
    all_relevant_docs: List[Set[str]], 
    k: int = 5
) -> float:
    """
    Calculate Mean Recall@K across multiple queries.
    
    Args:
        all_retrieved_docs: List of retrieved document lists for each query
        all_relevant_docs: List of relevant document sets for each query
        k: Number of top documents to consider
        
    Returns:
        Mean Recall@K score across all queries
        
    Example:
        >>> retrieved = [
        ...     ["doc1", "doc2", "doc3"],
        ...     ["doc4", "doc5", "doc6"]
        ... ]
        >>> relevant = [
        ...     {"doc1", "doc3"},
        ...     {"doc5", "doc7"}
        ... ]
        >>> mean_recall_at_k(retrieved, relevant, k=3)
        0.75  # Average of (2/2) and (1/2)
    """
    if len(all_retrieved_docs) != len(all_relevant_docs):
        raise ValueError("Number of retrieved and relevant document lists must match")
    
    if not all_retrieved_docs:
        return 0.0
    
    recalls = [
        recall_at_k(retrieved, relevant, k)
        for retrieved, relevant in zip(all_retrieved_docs, all_relevant_docs)
    ]
    
    return sum(recalls) / len(recalls)


def recall_at_various_k(
    retrieved_docs: List[str], 
    relevant_docs: Set[str], 
    k_values: List[int] = [1, 3, 5, 10]
) -> dict:
    """
    Calculate Recall@K for multiple k values.
    
    Args:
        retrieved_docs: List of retrieved document IDs (in ranked order)
        relevant_docs: Set of ground truth relevant document IDs
        k_values: List of k values to evaluate
        
    Returns:
        Dictionary mapping k to Recall@K score
        
    Example:
        >>> retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        >>> relevant = {"doc1", "doc3", "doc5"}
        >>> recall_at_various_k(retrieved, relevant, k_values=[1, 3, 5])
        {1: 0.333, 3: 0.667, 5: 1.0}
    """
    results = {}
    
    for k in k_values:
        if k <= len(retrieved_docs):
            results[k] = recall_at_k(retrieved_docs, relevant_docs, k)
        else:
            # If k > number of retrieved docs, use all retrieved docs
            results[k] = recall_at_k(retrieved_docs, relevant_docs, len(retrieved_docs))
    
    return results


def f1_score_at_k(retrieved_docs: List[str], relevant_docs: Set[str], k: int = 5) -> float:
    """
    Calculate F1 score at K (harmonic mean of Precision@K and Recall@K).
    
    Formula: F1@K = 2 * (Precision@K * Recall@K) / (Precision@K + Recall@K)
    
    Args:
        retrieved_docs: List of retrieved document IDs (in ranked order)
        relevant_docs: Set of ground truth relevant document IDs
        k: Number of top documents to consider
        
    Returns:
        F1@K score (between 0 and 1)
        
    Example:
        >>> retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        >>> relevant = {"doc1", "doc3", "doc6"}
        >>> f1_score_at_k(retrieved, relevant, k=5)
        0.5  # Harmonic mean of precision (0.4) and recall (0.667)
    """
    from .precision_at_k import precision_at_k
    
    precision = precision_at_k(retrieved_docs, relevant_docs, k)
    recall = recall_at_k(retrieved_docs, relevant_docs, k)
    
    if precision + recall == 0:
        return 0.0
    
    f1 = 2 * (precision * recall) / (precision + recall)
    
    return f1
