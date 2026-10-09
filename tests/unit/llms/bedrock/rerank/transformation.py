import json

import pytest
from fastapi.testclient import TestClient

from unittest.mock import MagicMock, patch

from waypoint import rerank
from waypoint.llms.custom_httpx.http_handler import HTTPHandler
