import traceback

import waypoint
from waypoint.proxy.guardrails.init_guardrails import init_guardrails_v2


def test_guardrails_ai():
    waypoint.set_verbose = True
    waypoint.guardrail_name_config_map = {}

    init_guardrails_v2(
        all_guardrails=[
            {
                "guardrail_name": "gibberish-guard",
                "litellm_params": {
                    "guardrail": "guardrails_ai",
                    "guard_name": "gibberish_guard",
                    "mode": "post_call",
                },
            }
        ],
        config_file_path="",
    )
