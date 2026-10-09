"""
Registry mapping the callback class string to the class type.

This is used to get the class type from the callback class string.

Example:
    "datadog" -> DataDogLogger
    "prometheus" -> PrometheusLogger
"""

from typing import Final

from waypoint import _custom_logger_compatible_callbacks_literal
from waypoint.integrations.agentops import AgentOps
from waypoint.integrations.anthropic_cache_control_hook import AnthropicCacheControlHook
from waypoint.integrations.argilla import ArgillaLogger
from waypoint.integrations.azure_sentinel.azure_sentinel import AzureSentinelLogger
from waypoint.integrations.azure_storage.azure_storage import AzureBlobStorageLogger
from waypoint.integrations.bitbucket import BitBucketPromptManager
from waypoint.integrations.braintrust_logging import BraintrustLogger
from waypoint.integrations.cloudzero.cloudzero import CloudZeroLogger
from waypoint.integrations.datadog.datadog import DataDogLogger
from waypoint.integrations.datadog.datadog_llm_obs import DataDogLLMObsLogger
from waypoint.integrations.datadog.datadog_metrics import DatadogMetricsLogger
from waypoint.integrations.deepeval import DeepEvalLogger
from waypoint.integrations.dotprompt import DotpromptManager
from waypoint.integrations.focus.focus_logger import FocusLogger
from waypoint.integrations.galileo import GalileoObserve
from waypoint.integrations.gcs_bucket.gcs_bucket import GCSBucketLogger
from waypoint.integrations.gcs_pubsub.pub_sub import GcsPubSubLogger
from waypoint.integrations.gitlab import GitLabPromptManager
from waypoint.integrations.humanloop import HumanloopLogger
from waypoint.integrations.lago import LagoLogger
from waypoint.integrations.langfuse.langfuse_prompt_management import (
    LangfusePromptManagement,
)
from waypoint.integrations.langsmith import LangsmithLogger
from waypoint.integrations.literal_ai import LiteralAILogger
from waypoint.integrations.mavvrik_focus.mavvrik_focus_logger import MavvrikFocusLogger
from waypoint.integrations.mlflow import MlflowLogger
from waypoint.integrations.newrelic import NewRelicLogger
from waypoint.integrations.openmeter import OpenMeterLogger
from waypoint.integrations.opentelemetry import OpenTelemetry
from waypoint.integrations.opik.opik import OpikLogger
from waypoint.integrations.pointfive import PointFiveLogger
from waypoint.integrations.posthog import PostHogLogger
from waypoint.integrations.prometheus import PrometheusLogger
from waypoint.integrations.s3_v2 import S3Logger
from waypoint.integrations.sqs import SQSLogger
from waypoint.integrations.vantage.vantage_logger import VantageLogger
from waypoint.integrations.vector_store_integrations.vector_store_pre_call_hook import (
    VectorStorePreCallHook,
)
from waypoint.integrations.waypoint_agent import LiteLLMAgentModelResolver
from waypoint.integrations.zerobus import ZerobusLogger
from waypoint.proxy.hooks.dynamic_rate_limiter import (  # noqa: F401  # legacy module exports
    PROXY_DynamicRateLimitHandler,
    _PROXY_DynamicRateLimitHandler,  # pyright: ignore[reportPrivateUsage,reportUnusedImport]  # backwards-compatible package export
)
from waypoint.proxy.hooks.dynamic_rate_limiter_v3 import (  # noqa: F401  # legacy module exports
    PROXY_DynamicRateLimitHandlerV3,
    _PROXY_DynamicRateLimitHandlerV3,  # pyright: ignore[reportPrivateUsage,reportUnusedImport]  # backwards-compatible package export
)


class CustomLoggerRegistry:
    """
    Registry mapping the callback class string to the class type.
    """

    CALLBACK_CLASS_STR_TO_CLASS_TYPE = {
        "lago": LagoLogger,
        "openmeter": OpenMeterLogger,
        "braintrust": BraintrustLogger,
        "galileo": GalileoObserve,
        "langsmith": LangsmithLogger,
        "literalai": LiteralAILogger,
        "litellm_agent": LiteLLMAgentModelResolver,
        "prometheus": PrometheusLogger,
        "datadog": DataDogLogger,
        "datadog_llm_observability": DataDogLLMObsLogger,
        "datadog_metrics": DatadogMetricsLogger,
        "gcs_bucket": GCSBucketLogger,
        "opik": OpikLogger,
        "argilla": ArgillaLogger,
        "opentelemetry": OpenTelemetry,
        "azure_sentinel": AzureSentinelLogger,
        "azure_storage": AzureBlobStorageLogger,
        "humanloop": HumanloopLogger,
        # OTEL compatible loggers
        "logfire": OpenTelemetry,
        "arize": OpenTelemetry,
        "langfuse_otel": OpenTelemetry,
        "arize_phoenix": OpenTelemetry,
        "langtrace": OpenTelemetry,
        "weave_otel": OpenTelemetry,
        "levo": OpenTelemetry,
        "signoz": OpenTelemetry,
        "mlflow": MlflowLogger,
        "langfuse": LangfusePromptManagement,
        "otel": OpenTelemetry,
        "gcs_pubsub": GcsPubSubLogger,
        "anthropic_cache_control_hook": AnthropicCacheControlHook,
        "agentops": AgentOps,
        "deepeval": DeepEvalLogger,
        "s3_v2": S3Logger,
        "pointfive": PointFiveLogger,
        "zerobus": ZerobusLogger,
        "aws_sqs": SQSLogger,
        "dynamic_rate_limiter": PROXY_DynamicRateLimitHandler,
        "dynamic_rate_limiter_v3": PROXY_DynamicRateLimitHandlerV3,
        "vector_store_pre_call_hook": VectorStorePreCallHook,
        "dotprompt": DotpromptManager,
        "bitbucket": BitBucketPromptManager,
        "gitlab": GitLabPromptManager,
        "cloudzero": CloudZeroLogger,
        "focus": FocusLogger,
        "mavvrik": MavvrikFocusLogger,
        "vantage": VantageLogger,
        "posthog": PostHogLogger,
        "newrelic": NewRelicLogger,
    }

    try:
        from waypoint_enterprise.enterprise_callbacks.pagerduty.pagerduty import (
            PagerDutyAlerting,
        )
        from waypoint_enterprise.enterprise_callbacks.send_emails.resend_email import (
            ResendEmailLogger,
        )
        from waypoint_enterprise.enterprise_callbacks.send_emails.sendgrid_email import (
            SendGridEmailLogger,
        )
        from waypoint_enterprise.enterprise_callbacks.send_emails.smtp_email import (
            SMTPEmailLogger,
        )

        from waypoint.integrations.generic_api.generic_api_callback import (
            GenericAPILogger,
        )

        enterprise_loggers = {
            "pagerduty": PagerDutyAlerting,
            "generic_api": GenericAPILogger,
            "resend_email": ResendEmailLogger,
            "sendgrid_email": SendGridEmailLogger,
            "smtp_email": SMTPEmailLogger,
        }
        CALLBACK_CLASS_STR_TO_CLASS_TYPE.update(enterprise_loggers)
    except ImportError:
        pass  # enterprise not installed

    @classmethod
    def get_callback_str_from_class_type(cls, class_type: type) -> str | None:
        """
        Get the callback string from the class type.

        Args:
            class_type: The class type to find the string for

        Returns:
            str: The callback string, or None if not found
        """
        for (
            callback_str,
            callback_class,
        ) in cls.CALLBACK_CLASS_STR_TO_CLASS_TYPE.items():
            if callback_class == class_type:
                return callback_str
        return None

    @classmethod
    def get_all_callback_strs_from_class_type(cls, class_type: type) -> list[str]:
        """
        Get all callback strings that map to the same class type.
        Some class types (like OpenTelemetry) have multiple string mappings.

        Args:
            class_type: The class type to find all strings for

        Returns:
            list: List of callback strings that map to the class type
        """
        callback_strs: Final[list[str]] = []
        for (
            callback_str,
            callback_class,
        ) in cls.CALLBACK_CLASS_STR_TO_CLASS_TYPE.items():
            if callback_class == class_type:
                callback_strs.append(callback_str)
        return callback_strs

    @classmethod
    def get_class_type_for_custom_logger_name(
        cls,
        custom_logger_name: _custom_logger_compatible_callbacks_literal,
    ) -> type:
        """
        Get the class type for a given custom logger name
        """
        return cls.CALLBACK_CLASS_STR_TO_CLASS_TYPE[custom_logger_name]
