from langchain_core.messages import HumanMessage, SystemMessage

from app.config import get_settings
from app.core.llm_factory import create_llm
from app.core.token_counter import count_messages_tokens


def sliding_window(messages: list, window_size: int | None = None) -> list:
    """Keep only the last N messages.

    Args:
        messages: List of messages
        window_size: Number of messages to keep (default from config)

    Returns:
        Trimmed message list
    """
    settings = get_settings()
    size = window_size or settings.SLIDING_WINDOW_SIZE
    return messages[-size:]


async def summarize_messages(messages: list) -> str:
    """Summarize older messages to reduce context size.

    Args:
        messages: Messages to summarize

    Returns:
        Summary text
    """
    llm = create_llm(temperature=0.3)

    # Create summarization prompt
    conversation_text = "\n".join(
        f"{msg.type}: {msg.content[:200]}" for msg in messages
    )

    prompt = f"""Summarize the following conversation in 2-3 sentences, preserving key information:

{conversation_text}

Summary:"""

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content


async def manage_context(messages: list) -> tuple[list, str]:
    """Manage context window by combining sliding window and summarization.

    Returns:
        Tuple of (managed_messages, context_summary)
    """
    settings = get_settings()
    context_summary = ""

    # Check if we need to summarize
    total_tokens = count_messages_tokens(messages)

    if total_tokens > settings.SUMMARY_THRESHOLD_TOKENS:
        # Split messages: old (to summarize) and recent (to keep)
        split_point = len(messages) // 2
        old_messages = messages[:split_point]
        recent_messages = messages[split_point:]

        # Summarize old messages
        context_summary = await summarize_messages(old_messages)

        # Keep recent messages with summary as system context
        messages = [
            SystemMessage(content=f"Previous conversation context: {context_summary}")
        ] + recent_messages

    # Apply sliding window as safety net
    messages = sliding_window(messages)

    return messages, context_summary
