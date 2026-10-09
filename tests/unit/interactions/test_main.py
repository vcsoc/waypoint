import pytest

import waypoint
import waypoint.interactions as interactions


@pytest.fixture
def api_key():
    return "test-api-key"


class TestGoogleInteractionsCreate:
    @pytest.mark.usefixtures("fake_provider_credentials")
    def test_missing_model_and_agent(self, api_key):
        """Test error when neither model nor agent is provided."""
        with pytest.raises((ValueError, waypoint.APIConnectionError)):
            interactions.create(
                input="Hello",
                api_key=api_key,
            )
