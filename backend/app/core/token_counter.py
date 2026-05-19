try:
    import tiktoken
    _encoder = tiktoken.get_encoding("cl100k_base")
except ImportError:
    _encoder = None


def count_tokens(text: str) -> int:
    """Count tokens in text.

    Uses tiktoken if available, otherwise estimates based on characters.
    """
    if _encoder:
        return len(_encoder.encode(text))

    # Rough estimate: ~4 characters per token
    return len(text) // 4


def count_messages_tokens(messages: list) -> int:
    """Count total tokens in a list of messages.

    Args:
        messages: List of message objects with content attribute

    Returns:
        Total token count
    """
    total = 0
    for msg in messages:
        if hasattr(msg, "content"):
            total += count_tokens(str(msg.content))
        # Add overhead for message formatting
        total += 4
    return total
