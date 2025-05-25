from typing import List, Dict, Any
import logging
from datetime import datetime
import pytz
from alpaca_trade_api.stream import Stream
import pandas as pd
import os
from secrets import API_KEY, API_SECRET, PAPER_URL

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("spy_stream.log"), logging.StreamHandler()],
)
logger: logging.Logger = logging.getLogger(__name__)

current_data: List[Dict[str, Any]] = []


async def handle_bar(bar: Any) -> None:
    """Handle incoming bar data"""
    global current_data
    try:
        # Convert to EST
        est_timestamp: datetime = bar.timestamp.astimezone(
            pytz.timezone("America/New_York")
        )

        # Store the bar data
        bar_dict: Dict[str, Any] = {
            "timestamp": bar.timestamp.isoformat(),
            "timestamp_est": est_timestamp.isoformat(),
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
            "vwap": bar.vwap,
            "trade_count": bar.trade_count,
        }

        current_data.append(bar_dict)

        # Save every 100 bars
        if len(current_data) >= 100:
            save_data()

    except Exception as e:
        logger.error(f"Error processing bar: {e}")


def save_data() -> None:
    """Save data to CSV file"""
    global current_data
    try:
        if not current_data:
            return

        df: pd.DataFrame = pd.DataFrame(current_data)
        date_str: str = datetime.now().strftime("%Y-%m-%d")

        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        filename: str = f"data/SPY_{date_str}.csv"

        if os.path.exists(filename):
            df.to_csv(filename, mode="a", header=False, index=False)
        else:
            df.to_csv(filename, index=False)

        logger.info(f"Saved {len(current_data)} records to {filename}")
        current_data = []

    except Exception as e:
        logger.error(f"Error saving data: {e}")


def main() -> None:
    """Main function to run the streaming service"""
    try:
        logger.info("Starting SPY data streaming service...")

        # Initialize the streaming client
        stream: Stream = Stream(
            API_KEY, API_SECRET, base_url=PAPER_URL, data_feed="iex"
        )

        # Subscribe to SPY bars
        stream.subscribe_bars(handle_bar, "SPY")

        # Start streaming
        stream.run()

    except KeyboardInterrupt:
        save_data()
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        save_data()


if __name__ == "__main__":
    main()
