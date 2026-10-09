"""
New Relic AI Monitoring Integration for Waypoint

This module provides integration with New Relic's AI Monitoring feature to track
LLM requests, responses, and usage metrics.
"""

from waypoint.integrations.newrelic.newrelic import NewRelicLogger

__all__ = ["NewRelicLogger"]
