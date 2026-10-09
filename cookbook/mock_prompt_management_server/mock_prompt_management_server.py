#!/usr/bin/env python3
"""
Mock Prompt Management API Server

This is a FastAPI server that implements the Waypoint Generic Prompt Management API
for testing and demonstration purposes.

Usage:
    python mock_prompt_management_server.py

The server will start on http://localhost:8080

Test the endpoint:
    curl "http://localhost:8080/beta/litellm_prompt_management?prompt_id=hello-world-prompt"
"""

import sys
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

# ============================================================================
# Response Models
# ============================================================================


class MessageContent(BaseModel):
    """A single message in the prompt template"""

    role: str = Field(..., description="Message role (system, user, assistant)")
    content: str = Field(
        ..., description="Message content with optional {variable} placeholders"
    )


class PromptResponse(BaseModel):
    """Response format for the prompt management API"""

    prompt_id: str = Field(..., description="The ID of the prompt")
    prompt_template: list[MessageContent] = Field(..., description="Array of messages in OpenAI format")
    prompt_template_model: str | None = Field(None, description="Optional model to use for this prompt")
    prompt_template_optional_params: dict[str, Any] | None = Field(
        None, description="Optional parameters like temperature, max_tokens, etc."
    )


# ============================================================================
# Mock Prompt Database
# ============================================================================

PROMPTS_DB = {
    "hello-world-prompt": {
        "prompt_id": "hello-world-prompt",
        "prompt_template": [
            {
                "role": "system",
                "content": "You are a helpful assistant specialized in {domain}.",
            },
            {"role": "user", "content": "Help me with: {task}"},
        ],
        "prompt_template_model": "gpt-4",
        "prompt_template_optional_params": {"temperature": 0.7, "max_tokens": 500},
    },
    "code-review-prompt": {
        "prompt_id": "code-review-prompt",
        "prompt_template": [
            {
                "role": "system",
                "content": "You are an expert code reviewer with {years_experience} years of experience in {language}.",
            },
            {
                "role": "user",
                "content": "Please review the following code for bugs, security issues, and best practices:\n\n{code}",
            },
        ],
        "prompt_template_model": "gpt-4-turbo",
        "prompt_template_optional_params": {
            "temperature": 0.3,
            "max_tokens": 1500,
        },
    },
    "customer-support-prompt": {
        "prompt_id": "customer-support-prompt",
        "prompt_template": [
            {
                "role": "system",
                "content": "You are a friendly customer support agent for {company_name}. Always be professional, empathetic, and solution-oriented.",
            },
            {
                "role": "user",
                "content": "Customer inquiry: {customer_message}",
            },
        ],
        "prompt_template_model": "gpt-3.5-turbo",
        "prompt_template_optional_params": {
            "temperature": 0.8,
            "max_tokens": 800,
            "top_p": 0.9,
        },
    },
    "data-analysis-prompt": {
        "prompt_id": "data-analysis-prompt",
        "prompt_template": [
            {
                "role": "system",
                "content": "You are a data scientist expert in {analysis_type} analysis.",
            },
            {
                "role": "user",
                "content": "Analyze the following data and provide insights:\n\nDataset: {dataset_name}\nData: {data}",
            },
        ],
        "prompt_template_model": "gpt-4",
        "prompt_template_optional_params": {
            "temperature": 0.5,
            "max_tokens": 2000,
        },
    },
    "creative-writing-prompt": {
        "prompt_id": "creative-writing-prompt",
        "prompt_template": [
            {
                "role": "system",
                "content": "You are a creative writer specializing in {genre} fiction.",
            },
            {
                "role": "user",
                "content": "Write a {length} story about: {topic}",
            },
        ],
        "prompt_template_model": "gpt-4",
        "prompt_template_optional_params": {
            "temperature": 0.9,
            "max_tokens": 3000,
            "top_p": 0.95,
        },
    },
}

# Valid API tokens for authentication (in production, use a secure token store)
VALID_API_TOKENS = {
    "test-token-12345",
    "dev-token-67890",
    "prod-token-abcdef",
}

# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="Mock Prompt Management API",
    description="A mock server implementing the Waypoint Generic Prompt Management API",
    version="1.0.0",
)


def verify_api_key(authorization: str | None = Header(None)) -> bool:
    """
    Verify the API key from the Authorization header.

    Args:
        authorization: Authorization header (Bearer token)

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if authorization is None:
        # Allow requests without authentication for testing
        return True

    # Extract token from "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'",
        )

    token = authorization.replace("Bearer ", "").strip()

    if token not in VALID_API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return True


@app.get("/beta/litellm_prompt_management", response_model=PromptResponse)
async def get_prompt(
    prompt_id: str = Query(..., description="The ID of the prompt to fetch"),
    project_name: str | None = Query(None, description="Optional project name filter"),
    slug: str | None = Query(None, description="Optional slug filter"),
    version: str | None = Query(None, description="Optional version filter"),
    authorization: str | None = Header(None),
) -> PromptResponse:
    """
    Get a prompt by ID with optional filtering.

    This endpoint implements the Waypoint Generic Prompt Management API specification.

    Args:
        prompt_id: The ID of the prompt to fetch
        project_name: Optional project name for filtering
        slug: Optional slug for filtering
        version: Optional version for filtering
        authorization: Optional Bearer token for authentication

    Returns:
        PromptResponse with the prompt template and configuration

    Raises:
        HTTPException: 401 if authentication fails, 404 if prompt not found
    """
    # Verify authentication
    verify_api_key(authorization)

    # Log the request parameters (useful for debugging)
    sys.stdout.write(f"Fetching prompt: {prompt_id}" + "\n")
    if project_name:
        sys.stdout.write(f"  Project: {project_name}" + "\n")
    if slug:
        sys.stdout.write(f"  Slug: {slug}" + "\n")
    if version:
        sys.stdout.write(f"  Version: {version}" + "\n")

    # Check if prompt exists
    if prompt_id not in PROMPTS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt '{prompt_id}' not found. Available prompts: {list(PROMPTS_DB.keys())}",
        )

    # Get the prompt from the database
    prompt_data = PROMPTS_DB[prompt_id]

    # Optional: Apply filtering based on project_name, slug, or version
    # In a real implementation, you might use these to filter prompts by access control
    # or to fetch specific versions from your database

    return PromptResponse(**prompt_data)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mock-prompt-management-api",
        "version": "1.0.0",
    }


@app.get("/prompts")
async def list_prompts(authorization: str | None = Header(None)):
    """
    List all available prompts.

    This is a convenience endpoint (not part of the Waypoint spec) for
    discovering available prompts.
    """
    # Verify authentication
    verify_api_key(authorization)

    prompts_list = [
        {
            "prompt_id": pid,
            "model": p.get("prompt_template_model"),
            "has_variables": any(
                "{" in msg.get("content", "") for msg in p.get("prompt_template", [])
            ),
        }
        for pid, p in PROMPTS_DB.items()
    ]

    return {"prompts": prompts_list, "total": len(prompts_list)}


@app.get("/prompts/{prompt_id}/variables")
async def get_prompt_variables(prompt_id: str, authorization: str | None = Header(None)):
    """
    Get all variables in a prompt template.

    This is a convenience endpoint (not part of the Waypoint spec) for
    discovering what variables a prompt expects.
    """
    # Verify authentication
    verify_api_key(authorization)

    if prompt_id not in PROMPTS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt '{prompt_id}' not found",
        )

    prompt_data = PROMPTS_DB[prompt_id]
    variables = set()

    # Extract variables from the prompt template
    import re

    for message in prompt_data["prompt_template"]:
        content = message.get("content", "")
        # Find all {variable} patterns
        found_vars = re.findall(r"\{(\w+)\}", content)
        variables.update(found_vars)

    return {
        "prompt_id": prompt_id,
        "variables": sorted(list(variables)),
        "example_usage": {
            "prompt_id": prompt_id,
            "prompt_variables": {var: f"<{var}_value>" for var in variables},
        },
    }


@app.post("/prompts")
async def create_prompt(prompt: PromptResponse, authorization: str | None = Header(None)):
    """
    Create a new prompt (convenience endpoint for testing).

    This is NOT part of the Waypoint spec - it's just for testing purposes.
    """
    # Verify authentication
    verify_api_key(authorization)

    if prompt.prompt_id in PROMPTS_DB:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Prompt '{prompt.prompt_id}' already exists",
        )

    PROMPTS_DB[prompt.prompt_id] = prompt.dict()

    return {
        "status": "created",
        "prompt_id": prompt.prompt_id,
        "message": "Prompt created successfully (in-memory only)",
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    sys.stdout.write(str("=" * 70) + "\n")
    sys.stdout.write("Mock Prompt Management API Server" + "\n")
    sys.stdout.write(str("=" * 70) + "\n")
    sys.stdout.write("\nStarting server on http://localhost:8080" + "\n")
    sys.stdout.write(f"\nAvailable prompts: {len(PROMPTS_DB)}" + "\n")
    for prompt_id in PROMPTS_DB:
        sys.stdout.write(f"  - {prompt_id}" + "\n")
    sys.stdout.write(f"\nValid API tokens: {len(VALID_API_TOKENS)}" + "\n")
    sys.stdout.write("  - test-token-12345" + "\n")
    sys.stdout.write("  - dev-token-67890" + "\n")
    sys.stdout.write("  - prod-token-abcdef" + "\n")
    sys.stdout.write("\nEndpoints:" + "\n")
    sys.stdout.write("  GET  /beta/litellm_prompt_management?prompt_id=<id>  (Waypoint spec)" + "\n")
    sys.stdout.write("  GET  /health                                          (health check)" + "\n")
    sys.stdout.write("  GET  /prompts                                         (list all prompts)" + "\n")
    sys.stdout.write("  GET  /prompts/{id}/variables                          (get prompt variables)" + "\n")
    sys.stdout.write("  POST /prompts                                         (create prompt)" + "\n")
    sys.stdout.write("\nExample usage:" + "\n")
    sys.stdout.write(
        '  curl "http://localhost:8080/beta/litellm_prompt_management?prompt_id=hello-world-prompt"' + "\n"
    )
    sys.stdout.write("\nPress CTRL+C to stop the server" + "\n")
    sys.stdout.write(str("=" * 70) + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
