from typing import Any
import sys
import os
from mcp.server.fastmcp import FastMCP

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import getStockPriceEGX, getStockDataEGX
from egx import validate_symbol, format_indicators
from precious_metals import get_gold_price, get_silver_price

# Initialize FastMCP server
mcp = FastMCP(
    from fastapi import FastAPI
from contextlib import asynccontextmanager
    "egx_stock_tools",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
)

@mcp.tool()
def stock_price_egx(symbol: str) -> str:
    """Get the current price of a stock in EGX."""
    if not validate_symbol(symbol):
        return f"Error: Invalid symbol format. Symbol should be 4 letters (received: {symbol})"
    try:
        return str(getStockPriceEGX(symbol))
    except Exception as e:
        return f"Error getting stock price: {str(e)}"

@mcp.tool()
def stock_data_egx(symbol: str) -> str:
    """Get stock technicals and statistics from EGX."""
    if not validate_symbol(symbol):
        return f"Error: Invalid symbol format. Symbol should be 4 letters (received: {symbol})"
    try:
        indicators = getStockDataEGX(symbol)
        if isinstance(indicators, dict):
            formatted_indicators = format_indicators(indicators)
            return "\n".join([f"{k}: {v}" for k, v in formatted_indicators.items()])
        return str(indicators)
    except Exception as e:
        return f"Error getting stock data: {str(e)}"

@mcp.tool()
def gold_price() -> str:
    """Get the current price of gold in EGP."""
    try:
        return get_gold_price()
    except Exception as e:
        return f"Error getting gold price: {str(e)}"

@mcp.tool()
def silver_price() -> str:
    """Get the current price of silver in EGP."""
    try:
        return get_silver_price()
    except Exception as e:
        return f"Error getting silver price: {str(e)}"
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/", mcp.streamable_http_app())
def main() -> None:
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
