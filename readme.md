# crypto_agent
# Crypto Price Checker Agent

## Description

This agent leverages the CoinGecko API to provide current market prices for various cryptocurrencies. It can fetch prices for one or multiple cryptocurrencies simultaneously and display them in a specified fiat currency (defaulting to USD).

This agent is designed to be used within a compatible agent framework (like one using `google.adk.agents`) and utilizes a large language model (LLM) capable of function calling (e.g., Gemini 1.5 Flash) to understand user requests and invoke the appropriate tool.

**Current Time Context:** Information requests will be processed assuming the current time is around **Monday, April 14, 2025 at 4:02 PM IST**, unless otherwise specified by the user.

## Features

* Fetches real-time cryptocurrency prices from CoinGecko.
* Supports fetching prices for multiple cryptocurrencies in a single request.
* Allows specifying the target fiat currency (e.g., USD, EUR, GBP, INR).
* Handles potential errors like invalid cryptocurrency IDs or unsupported currencies gracefully.

## Requirements

* **Python 3.x**
* **Required Python Libraries:**
    ```
    pycoingecko
    google-adk-agents  # Or the specific agent framework library you are using
    typing             # (Standard library)
    ```
    You can typically install dependencies using pip:
    ```bash
    pip install pycoingecko google-adk-agents
    ```
    *(Note: Replace `google-adk-agents` with the actual package name if it differs in your environment).*
* **LLM Backend:** Access to a Google AI model capable of function calling, specified in the agent definition (e.g., `gemini-1.5-flash-001`).
* **Internet Connection:** Required to call the CoinGecko API.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install pycoingecko google-adk-agents
    ```
2.  **Ensure Agent Framework:** Make sure the environment where you run this code has the necessary setup for the `google.adk.agents` framework or your chosen alternative.

## Code Overview

1.  **`get_crypto_prices(crypto_ids: List[str], currency: Optional[str] = 'usd') -> dict` Function (Tool):**
    * This function acts as the tool that the agent uses.
    * It takes a list of cryptocurrency IDs (strings, e.g., `['bitcoin', 'ethereum']`) and an optional target fiat currency code (string, e.g., `'inr'`).
    * It initializes the `CoinGeckoAPI` client.
    * It calls the `cg.get_price()` method from the `pycoingecko` library.
    * It formats the results into a dictionary containing a `status` ("success" or "error") and either a `report` (formatted string with prices) or an `error_message`.
    * It includes error handling for invalid inputs or API issues.

2.  **`Agent` Definition (`root_agent`):**
    * Defines the agent's configuration using the `Agent` class.
    * `name`: `crypto_price_checker`
    * `model`: `gemini-1.5-flash-001` (or another function-calling model).
    * `description`: Explains the agent's purpose.
    * `instruction`: Provides detailed guidelines to the LLM on how to behave, interact with the user, use the tool, handle CoinGecko IDs, manage currencies, and report results or errors. Includes the current time context.
    * `tools`: Lists the available functions the agent can call (`[get_crypto_prices]`).

## How to Use (Conceptual)

This agent is intended to be run within its specific framework. You would interact with it via natural language prompts.

**Example User Prompts:**

* "What's the current price of Bitcoin?"
* "Get me the prices for Ethereum and Solana in INR."
* "How much is Dogecoin in GBP?"
* "Price check: cardano, polkadot" (Agent should assume USD if currency not specified)

**Example Agent Interaction Flow:**

1.  **User:** "Price for bitcoin and ethereum in eur"
2.  **Agent (LLM):** Understands the request, identifies the cryptocurrencies ('bitcoin', 'ethereum') and the currency ('eur'). Determines it needs to use the `get_crypto_prices` tool.
3.  **Agent (Framework):** Calls the `get_crypto_prices(crypto_ids=['bitcoin', 'ethereum'], currency='eur')` function.
4.  **`get_crypto_prices` Tool:** Executes, calls CoinGecko API, gets prices.
5.  **`get_crypto_prices` Tool:** Returns a dictionary like:
    ```python
    {
        "status": "success",
        "report": "Current Prices:\n- Bitcoin: 65,432.10 EUR\n- Ethereum: 3,123.45 EUR"
    }
    ```
6.  **Agent (LLM):** Receives the tool's result and formats a user-friendly response based on the report.
7.  **Agent (Response to User):** "Okay, here are the current prices in EUR:\n- Bitcoin: 65,432.10 EUR\n- Ethereum: 3,123.45 EUR"

**Error Handling Example:**

1.  **User:** "What's the price of FakeCoin?"
2.  **Agent (LLM):** Calls `get_crypto_prices(crypto_ids=['fakecoin'], currency='usd')`.
3.  **`get_crypto_prices` Tool:** CoinGecko API fails to find 'fakecoin'. Returns:
    ```python
    {
        "status": "error",
        "error_message": "One or more cryptocurrency IDs were not found by CoinGecko: fakecoin. Please use valid CoinGecko IDs (e.g., 'bitcoin', 'ethereum')."
    }
    ```
4.  **Agent (LLM):** Receives the error.
5.  **Agent (Response to User):** "Sorry, I couldn't find price data for 'fakecoin'. Please ensure you're using a valid CoinGecko ID (like 'bitcoin', 'ethereum')."

## CoinGecko IDs

* This tool requires official **CoinGecko API IDs** (e.g., `bitcoin`, `ethereum`, `solana`, `dogecoin`), not just symbols (like BTC, ETH, SOL, DOGE).
* If unsure about an ID, you can often find it on the CoinGecko website ([https://www.coingecko.com/](https://www.coingecko.com/)). The ID is usually part of the URL for a specific coin (e.g., `https://www.coingecko.com/en/coins/bitcoin` means the ID is `bitcoin`).

## Disclaimer


Cryptocurrency prices are highly volatile. The data provided by this agent comes directly from the CoinGecko API and is for informational purposes only. No financial advice is given or implied. Verify information independently before making any financial decisions.