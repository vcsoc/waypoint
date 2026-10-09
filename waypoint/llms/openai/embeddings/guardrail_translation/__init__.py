"""OpenAI Embeddings handler for Unified Guardrails."""

from typing import Final

from waypoint.llms.openai.embeddings.guardrail_translation.handler import (
    OpenAIEmbeddingsHandler,
)
from waypoint.types.utils import CallTypes

guardrail_translation_mappings: Final = {
    CallTypes.embedding: OpenAIEmbeddingsHandler,
    CallTypes.aembedding: OpenAIEmbeddingsHandler,
}

__all__ = ["OpenAIEmbeddingsHandler", "guardrail_translation_mappings"]
