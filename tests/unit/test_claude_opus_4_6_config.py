"""
Validate Claude Opus 4.6 model configuration entries.
"""


import waypoint


def test_opus_4_6_bedrock_converse_registration():
    assert "anthropic.claude-opus-4-6-v1" in waypoint.BEDROCK_CONVERSE_MODELS
    assert "global.anthropic.claude-opus-4-6-v1" in waypoint.bedrock_converse_models
    assert "us.anthropic.claude-opus-4-6-v1" in waypoint.bedrock_converse_models
    assert "eu.anthropic.claude-opus-4-6-v1" in waypoint.bedrock_converse_models
    assert "au.anthropic.claude-opus-4-6-v1" in waypoint.bedrock_converse_models
