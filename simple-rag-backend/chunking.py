def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Splits a long text into smaller chunks with overlap to maintain context.
    
    Args:
        text (str): The input text to chunk
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Number of characters to overlap between chunks
    
    Returns:
        List[str]: List of text chunks
    """
    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If we're at the end, include the rest
        if end >= len(text):
            chunk = text[start:]
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
            break

        # Try to break at sentence or paragraph boundaries if possible
        chunk_text = text[start:end]

        # Find the last sentence ending within the chunk
        last_period = chunk_text.rfind('.')
        last_exclamation = chunk_text.rfind('!')
        last_question = chunk_text.rfind('?')
        last_newline = chunk_text.rfind('\n')
        last_space = chunk_text.rfind(' ')

        # Find the best break point (closest to the end but not after)
        break_points = [bp for bp in [last_period, last_exclamation, last_question, last_newline, last_space] 
                       if bp != -1 and bp > len(chunk_text) // 2]  # Look for break points in the latter half
        
        if break_points:
            best_break = max(break_points) + 1  # Include the punctuation/space
            actual_end = start + best_break
        else:
            actual_end = end

        chunk = text[start:actual_end]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)

        # Move start forward, considering overlap
        start = actual_end - chunk_overlap
        
        # Ensure we make progress to prevent infinite loops
        if start <= 0:
            start = actual_end
        elif start >= len(text):
            break

    # Clean up chunks by removing leading/trailing whitespace and filter empty chunks
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    return chunks