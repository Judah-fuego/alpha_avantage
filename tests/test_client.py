# tests/test_intraday.py

import os
import pytest
from dotenv import load_dotenv
from alpha_vantage_client import AlphaVantageClient
# Load .env variables for local dev
load_dotenv()

@pytest.fixture
def client():
    api_key = os.getenv("ALPHA_ADVANTAGE_API_KEY")
    assert api_key, "ALPHA_ADVANTAGE_API_KEY not found in environment"
    return AlphaVantageClient(api_key=api_key)

def test_intraday_compact(client):
    result = client.get_time_series_intraday(symbol="AAPL", interval="5min")
    assert isinstance(result, dict), "Expected result to be a dictionary"
    assert any("Time Series" in k for k in result.keys()), "Response missing expected time series data"


