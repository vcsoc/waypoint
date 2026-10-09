"""OpenAI Text-to-Speech handler for Unified Guardrails."""

from typing import Final

from waypoint.llms.openai.speech.guardrail_translation.handler import (
    OpenAITextToSpeechHandler,
)
from waypoint.types.utils import CallTypes

guardrail_translation_mappings: Final = {
    CallTypes.speech: OpenAITextToSpeechHandler,
    CallTypes.aspeech: OpenAITextToSpeechHandler,
}

__all__ = ["OpenAITextToSpeechHandler", "guardrail_translation_mappings"]
