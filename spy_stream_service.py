import logging
from datetime import datetime
import pytz
from alpaca_trade_api.stream import Stream
import pandas as pd
import os
from secrets import API_KEY, API_SECRET, PAPER_URL


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spy_stream.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)



current_data = []

async def handle_bar(bar):
    global current_data
    try:
        est_timestamp = bar.timestamp.astimezone(pytz.timezone('America/New_York'))

        bar_dict = {
            'timestamp': bar.timestamp.isoformat(),
            'timestamp_est': est_timestamp.isoformat(),
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume,
            'vwap': bar.vwap,
            'trade_count': bar.trade_count
        }

        current_data.append(bar_dict)

        if len(current_data) >= 100:
            save_data()

    except Exception as e:
        logger.error(f"Error processing bar: {e}")

def save_data():
    global current_data
    try:
        if not current_data:
            return

        df = pd.DataFrame(current_data)
        date_str = datetime.now().strftime('%Y-%m-%d')

        os.makedirs('data', exist_ok=True)

        filename = f'data/SPY_{date_str}.csv'

        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)

        logger.info(f"Saved {len(current_data)} records to {filename}")
        current_data = []

    except Exception as e:
        logger.error(f"Error saving data: {e}")

def main():
    try:
        logger.info("Starting SPY data streaming service...")

        stream = Stream(
            API_KEY,
            API_SECRET,
            base_url=PAPER_URL,
            data_feed='iex'
        )

        stream.subscribe_bars(handle_bar, 'SPY')

        stream.run()

    except KeyboardInterrupt:
        save_data()
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        save_data()
if __name__ == "__main__":
    main()
