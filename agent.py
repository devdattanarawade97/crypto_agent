# Import necessary libraries
from pycoingecko import CoinGeckoAPI
from typing import Optional, List
from google.adk.agents import Agent  # Ensure this is a valid import in your environment
import datetime  # Required for time injection

# --- Crypto Price Tool Definition ---

# Instantiate the CoinGecko API Client
cg = CoinGeckoAPI()

def get_crypto_prices(crypto_ids: List[str], currency: Optional[str] = 'usd') -> dict:
    """
    Fetches the current price(s) for the given cryptocurrency IDs from CoinGecko.

    Args:
        crypto_ids (List[str]): A list of CoinGecko API IDs for the cryptocurrencies
                                (e.g., ['bitcoin', 'ethereum', 'dogecoin']).
        currency (Optional[str], optional): The currency to display the price in
                                            (e.g., 'usd', 'eur', 'gbp', 'inr').
                                            Defaults to 'usd'.

    Returns:
        dict: status ("success" or "error") and a report with the prices or an error message.
    """
    print(f"Tool: Fetching prices for IDs={crypto_ids} in currency={currency}")

    # Ensure currency is lowercase as required by CoinGecko API
    target_currency = currency.lower() if currency else 'usd'

    if not crypto_ids:
        return {"status": "error", "error_message": "Please provide at least one cryptocurrency ID (e.g., 'bitcoin')."}

    try:
        # --- Call CoinGecko API ---
        price_data = cg.get_price(ids=crypto_ids, vs_currencies=target_currency)

        # --- Format the Report ---
        if not price_data:
            return {"status": "error", "error_message": f"Could not retrieve price data for the specified IDs: {', '.join(crypto_ids)}. Please ensure the IDs are correct CoinGecko IDs."}

        report_lines = []
        for crypto_id in crypto_ids:
            if crypto_id in price_data and target_currency in price_data[crypto_id]:
                price = price_data[crypto_id][target_currency]
                report_lines.append(f"- {crypto_id.capitalize()}: {price:,} {target_currency.upper()}")
            else:
                report_lines.append(f"- {crypto_id.capitalize()}: Price data not found (check ID or currency '{target_currency}').")

        return {
            "status": "success",
            "report": "Current Prices:\n" + "\n".join(report_lines)
        }

    except Exception as e:
        print(f"Error calling CoinGecko API: {e}")
        if "invalid vs_currency" in str(e).lower():
            return {"status": "error", "error_message": f"Invalid target currency specified: '{target_currency}'. Please use standard currency codes like 'usd', 'eur', 'inr'."}
        if "Could not find coin with the given id" in str(e):
            return {"status": "error", "error_message": f"One or more cryptocurrency IDs were not found by CoinGecko: {', '.join(crypto_ids)}. Please use valid CoinGecko IDs (e.g., 'bitcoin', 'ethereum')."}

        return {"status": "error", "error_message": f"An error occurred while fetching prices: {e}"}


# --- Agent Definition ---
# Make sure to use a model capable of function calling
root_agent = Agent(
    name="crypto_price_checker",
    model="gemini-1.5-flash-001",  # Ensure model supports function calling
    description=(
        "An agent that fetches current cryptocurrency prices using the CoinGecko API."
    ),
    instruction=(
        "You are a helpful cryptocurrency price assistant. Your goal is to provide the current market price for cryptocurrencies requested by the user. "
        "Use the 'get_crypto_prices' tool to fetch the data. "
        "You need the official CoinGecko ID for each cryptocurrency (e.g., 'bitcoin', 'ethereum', 'solana', 'dogecoin'). If the user gives you a name or symbol you're unsure about, ask them to clarify or provide the CoinGecko ID. "
        "You can also specify the currency for the price (default is USD, but you can use others like 'INR', 'EUR', 'GBP'). "
        "Present the prices clearly based on the tool's report. If the tool reports an error (like an invalid ID), relay that information to the user. "
        f"Assume the current time is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')} unless specified otherwise by the user."
    ),
    tools=[get_crypto_prices],
)
