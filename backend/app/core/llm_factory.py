from langchain_openai import ChatOpenAI
from app.config import get_settings


def create_llm(temperature: float | None = None, max_tokens: int | None = None) -> ChatOpenAI:
    """Create a pluggable LLM instance.

    Supports MiMo, OpenAI, DeepSeek - all use OpenAI-compatible API format.
    Switch providers by changing LLM_BASE_URL and LLM_API_KEY in .env.
    """
    settings = get_settings()

    return ChatOpenAI(
        base_url=settings.LLM_BASE_URL,
        api_key=settings.LLM_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=temperature if temperature is not None else settings.LLM_TEMPERATURE,
        max_tokens=max_tokens or settings.LLM_MAX_TOKENS,
    )
