from streamlit.connections import BaseConnection
import streamlit as st
import requests
import os
import time

class CoinMarketCapConnection(BaseConnection):
    # Class attribute for the base URL of the CoinMarketCap API
    BASE_URL = "https://pro-api.coinmarketcap.com/v1/"

    def __init__(self, connection_name):
        # Initialize the parent class (BaseConnection)
        super().__init__(connection_name)
        # Call the _connect method to set up the connection
        self._connect()

    def _connect(self, **kwargs):
        # Fetch the API key from Streamlit's secrets or environment
        self.api_key = st.secrets["coinmarketcap"]["api_key"]
        # If API key is not found, raise an exception
        if not self.api_key:
            raise ValueError("CoinMarketCap API Key not found in environment!")

        # Initialize rate limit variables
        # These are used to handle API rate limiting
        self._rate_limit_reset = time.time() + 60  # Reset in 60 seconds by default
        self._rate_limit_remaining = 30  # Default to a reasonable number of requests

    def _get_headers(self):
        # Return the headers required for the API request
        # Includes the API key
        return {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }

    def _handle_rate_limit(self, response):
        # Handle the rate limit based on the API response
        self._rate_limit_remaining = int(response.headers.get("X-CMC_PRO_API_REQUESTS_REMAINING", 30))
        self._rate_limit_reset = time.time() + int(response.headers.get("X-CMC_PRO_API_REQUESTS_RESET_IN", 60))

        # If rate limit is reached, pause execution until reset
        if self._rate_limit_remaining <= 0:
            sleep_time = self._rate_limit_reset - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _request(self, endpoint, params=None):
        # Perform the API request
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params)

        # Handle rate limiting based on the response
        if "X-CMC_PRO_API_REQUESTS_REMAINING" in response.headers:
            self._handle_rate_limit(response)

        # Raise an exception if the response status is not 200 (OK)
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.text}")

        # Return the JSON response
        return response.json()

    def fetch_latest_data(self, limit=100):
        # Public method to fetch the latest cryptocurrency data
        # 'limit' parameter to limit the number of results
        return self._request("cryptocurrency/listings/latest", params={"limit": limit})

    def fetch_historical_data(self, cryptocurrency_id, start_date, end_date):
        # Public method to fetch historical data for a cryptocurrency
        params = {
            "id": cryptocurrency_id,
            "time_start": start_date,
            "time_end": end_date
        }
        return self._request("cryptocurrency/quotes/historical", params=params)