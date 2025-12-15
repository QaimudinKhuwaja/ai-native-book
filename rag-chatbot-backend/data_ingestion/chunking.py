def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Splits a long text into smaller chunks.
    """
    if len(text) <= chunk_size:
        return [text]

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

        # Try to break at sentence boundary if possible
        chunk_text = text[start:end]

        # Find the last sentence ending within the chunk
        last_period = chunk_text.rfind('.')
        last_exclamation = chunk_text.rfind('!')
        last_question = chunk_text.rfind('?')
        last_newline = chunk_text.rfind('\n')
        last_space = chunk_text.rfind(' ')

        # Find the best break point (closest to the end but not after)
        break_points = [bp for bp in [last_period, last_exclamation, last_question, last_newline, last_space] if bp != -1 and bp > 0]
        if break_points and len(chunk_text) > chunk_size - chunk_overlap:  # Only if we need to break within reasonable range
            best_break = max(break_points) + 1  # Include the punctuation/space
            actual_end = start + best_break
        else:
            actual_end = end

        chunk = text[start:actual_end]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)

        # Move start forward, considering overlap
        start = actual_end - chunk_overlap
        if start <= end - chunk_size:  # Ensure we make progress
            start = actual_end

        # Prevent infinite loop in edge cases
        if start == actual_end:
            start += 1

    # Clean up chunks by removing leading/trailing whitespace
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    return chunks
