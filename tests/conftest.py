"""
Pytest configuration.
"""

import pytest
import os
from dotenv import load_dotenv


# Load environment variables from .env.example for testing
env_file = os.path.join(os.path.dirname(__file__), "../.env.example")
if os.path.exists(env_file):
    load_dotenv(env_file)

# Override test settings
os.environ["DEBUG"] = "True"
os.environ["ENVIRONMENT"] = "testing"
os.environ["ENABLE_AUTH"] = "False"  # Disable auth for tests
os.environ["RATE_LIMIT_ENABLED"] = "False"  # Disable rate limiting for tests


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
