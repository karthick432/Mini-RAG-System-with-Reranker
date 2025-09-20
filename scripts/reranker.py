def hybrid_reranker(query, baseline_results, chunks, alpha=0.6):
    """
    Args:
        query (str)
        baseline_results (list of dict): [{'score', 'doc_name', 'chunk_index'}]
        chunks (dict): {(doc_name, chunk_index): text}
        alpha (float): weight for vector score vs keyword score
    Returns:
        List of dict with reranked results
    """
    results = []
    q_tokens = set(query.lower().split())
    for r in baseline_results:
        chunk_text = chunks[(r['doc_name'], r['chunk_index'])].lower()
        kw_score = sum(1 for t in q_tokens if t in chunk_text) / max(len(q_tokens), 1)
        final_score = alpha * r['score'] + (1 - alpha) * kw_score
        results.append({**r, "final_score": final_score})
    return sorted(results, key=lambda x: x['final_score'], reverse=True)
