import pytest


@pytest.mark.asyncio
async def test_langfuse_double_logging():
    import waypoint

    waypoint.set_verbose = True
    waypoint.success_callback = ["langfuse"]
    waypoint.failure_callback = ["langfuse"]  # logs errors to langfuse

    models = ["gpt-4o-mini", "claude-3-5-haiku-20241022"]

    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]

    resp = await waypoint.acompletion(
        model=models[0],
        messages=messages,
        temperature=0.0,
        fallbacks=models[1:],
        # metadata={"generation_name": "test-gen", "project": "litellm-test"},
    )
    return resp
