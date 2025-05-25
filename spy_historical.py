from typing import List, Dict, Any
import pandas as pd
from datetime import datetime, timedelta
from alpaca_trade_api.rest import REST
import pytz
import time
from secrets import API_KEY, API_SECRET, PAPER_URL


def fetch_historical_data() -> None:
    try:
        # Set up time parameters
        end_date: datetime = datetime.now(pytz.UTC)
        start_date: datetime = end_date - timedelta(days=730)  # 2 years

        print(f"Fetching SPY minute data from {start_date} to {end_date}")

        # Fetch data in smaller chunks to avoid timeouts (3-month chunks)
        chunk_size: timedelta = timedelta(days=90)
        current_start: datetime = start_date
        all_bars: List[Any] = []

        while current_start < end_date:
            current_end: datetime = min(current_start + chunk_size, end_date)
            print(f"Fetching chunk: {current_start} to {current_end}")

            # Get bars for current chunk
            bars = api.get_bars(
                symbol="SPY",
                timeframe="1Min",
                start=current_start.isoformat(),
                end=current_end.isoformat(),
                adjustment="raw",
            )

            all_bars.extend(bars)
            print(f"Retrieved {len(bars)} bars for current chunk")

            # Move to next chunk
            current_start = current_end
            time.sleep(1)  # Rate limiting pause

        # Convert all bars to DataFrame
        df: pd.DataFrame = pd.DataFrame(
            [
                {
                    "timestamp": bar.t,
                    "open": bar.o,
                    "high": bar.h,
                    "low": bar.l,
                    "close": bar.c,
                    "volume": bar.v,
                    "vwap": bar.vw,
                    "trades": bar.n,
                }
                for bar in all_bars
            ]
        )

        # Save to CSV
        filename: str = (
            f'data/SPY_minute_data_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv'
        )
        df.to_csv(filename, index=False)
        print(f"\nData successfully saved to {filename}")
        print(f"Total bars retrieved: {len(df)}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Initialize Alpaca API
    api: REST = REST(API_KEY, API_SECRET, PAPER_URL)
    fetch_historical_data()
