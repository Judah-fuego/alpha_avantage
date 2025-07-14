import requests
import os
from typing import Optional, Dict, Union


class AlphaVantageClient:
    BASE_URL="https://www.alphavantage.co/query"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided")
        

    def get_time_series_intraday(
        self,
        symbol: str,
        interval: str,
        adjusted: Optional[bool] = None,
        extended_hours: Optional[bool] = None,
        month: Optional[str] = None,  # format: YYYY-MM
        outputsize: Optional[str] = "compact",  # compact | full
        datatype: Optional[str] = "json",  # json | csv
    ) -> Dict:
        """Query intraday OHLCV time series for a stock with optional parameters."""

        # Required parameters
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key,
        }

        # Optional parameters
        if adjusted is not None:
            params["adjusted"] = "true" if adjusted else "false"

        if extended_hours is not None:
            params["extended_hours"] = "true" if extended_hours else "false"

        if month:
            params["month"] = month

        if outputsize == "compact" or outputsize == "full":

            params["outputsize"] = outputsize

        if datatype:
            params["datatype"] = datatype

        # Make the request
        response = requests.get(self.BASE_URL, params=params)
        if not response.ok:
            raise RuntimeError(f"Alpha Vantage API error: {response.status_code} {response.text}")

        # Return JSON or CSV text based on datatype
        return response.json() if datatype == "json" else response.text
    
    def get_time_series(
        self,
        symbol: str,
        period: str,  # "daily" | "weekly" | "monthly"
        adjusted: bool = False,
        outputsize: Optional[str] = "compact",  # compact | full (only for daily)
        datatype: Optional[str] = "json",  # json | csv
    ) -> Dict:
        """
        Query time series OHLCV data for a stock.
        
        Args:
            symbol: Stock symbol (e.g., "IBM", "TSCO.LON")
            period: Time period - "daily", "weekly", or "monthly"
            adjusted: Whether to get adjusted data (includes dividends/splits)
            outputsize: "compact" (100 data points) or "full" (20+ years). Only applies to daily data.
            datatype: "json" or "csv"
        
        Returns:
            Dict if datatype="json", str if datatype="csv"
        """
        
        # Validate period
        if period not in ["daily", "weekly", "monthly"]:
            raise ValueError("period must be 'daily', 'weekly', or 'monthly'")
        
        # Build function name based on period and adjusted flag
        function_name = f"TIME_SERIES_{period.upper()}"
        if adjusted:
            function_name += "_ADJUSTED"
        
        # Required parameters
        params = {
            "function": function_name,
            "symbol": symbol,
            "apikey": self.api_key,
        }
        
        # Optional parameters
        if datatype:
            params["datatype"] = datatype
        
        # outputsize only applies to daily data
        if period == "daily" and outputsize in ["compact", "full"]:
            params["outputsize"] = outputsize
        
        # Make the request
        response = requests.get(self.BASE_URL, params=params)
        if not response.ok:
            raise RuntimeError(f"Alpha Vantage API error: {response.status_code} {response.text}")
        
        # Return JSON or CSV text based on datatype
        return response.json() if datatype == "json" else response.text
    
    def get_quote(
            self,
            symbol: Union[str, list[str]],
            datatype: str = "json", # json | csv
            function: str = 'GLOBAL_QUOTE',
            bulk: bool = False,
    ) -> Union[Dict, str]:
        """
        Returns the latest price and volume information for a ticker of your choice.

        Args:
            symbol: Stock symbol (e.g., "IBM", "TSCO.LON")
            datatype: "json" or "csv"
            bulk: Whether to get single or bulk (MAX=100 tickers) per request
        
        Returns:
            Dict if datatype="json", str if datatype="csv"
        """

        if bulk:
            function = "REALTIME_BULK_QUOTES"

        if bulk and isinstance(symbol, list):
            symbol = ",".join(symbol)

        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key,
        }

        response = requests.get(self.BASE_URL, params=params)
        if not response.ok:
            raise RuntimeError(f"Alpha Vantage API error: {response.status_code} {response.text}")
        
        # Return JSON or CSV text based on datatype
        return response.json() if datatype == "json" else response.text
    
    def get_global_market_status(
       self     
    ) -> Dict: 
       
        params = {
            "function": "MARKET_STATUS",
            "apikey": self.api_key,
        }

        response = requests.get(self.BASE_URL, params=params)
        if not response.ok:
            raise RuntimeError(f"Alpha Vantage API error: {response.status_code} {response.text}")
        
        # Return JSON or CSV text based on datatype
        return response.json()