"""Mistral OCR handler for Unified Guardrails."""

from typing import Final

from waypoint.llms.mistral.ocr.guardrail_translation.handler import OCRHandler
from waypoint.types.utils import CallTypes

guardrail_translation_mappings: Final = {
    CallTypes.ocr: OCRHandler,
    CallTypes.aocr: OCRHandler,
}

__all__ = ["OCRHandler", "guardrail_translation_mappings"]
