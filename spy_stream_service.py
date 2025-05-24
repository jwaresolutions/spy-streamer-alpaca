import logging
from datetime import datetime, date, time, timedelta
import pytz
from alpaca_trade_api.stream import Stream
import pandas as pd
import os
import json
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spy_stream.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SPYDataCollector:
    def __init__(self, api_key: str, api_secret: str, paper_url: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_url = paper_url
        self.current_data: List[Dict] = []
        self.current_date = None
        self.last_bar_time = None
        self.data_gaps = []
        self.session_stats = SessionStats()
        self.initialize_new_day()

    def initialize_new_day(self):
        if self.current_date != date.today():
            if self.current_data:
                self.save_current_data()
            self.current_date = date.today()
            self.current_data = []
            self.session_stats = SessionStats()
            logger.info(f"Initialized new day: {self.current_date}")

            if self.data_gaps:
                self.save_session_stats()

    def save_session_stats(self):
        stats = {
            'date': self.current_date.isoformat(),
            'session_high': self.session_stats.session_high,
            'session_low': self.session_stats.session_low,
            'total_volume': self.session_stats.volume_total,
            'total_trades': self.session_stats.trade_count_total,
            'bars_processed': self.session_stats.bars_processed,
            'data_gaps': self.data_gaps
        }

        stats_file = f'data/SPY_{self.current_date}_stats.json'
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Saved session statistics to {stats_file}")

    async def handle_bar(self, bar):
        bar_date = bar.timestamp.date()
        if self.current_date is None or bar_date != self.current_date:
            self.initialize_new_day()

        if self.last_bar_time:
            expected_time = self.last_bar_time + timedelta(minutes=1)
            if bar.timestamp > expected_time:
                gap = {
                    'start': expected_time.isoformat(),
                    'end': bar.timestamp.isoformat(),
                    'missing_minutes': (bar.timestamp - expected_time).seconds // 60
                }
                self.data_gaps.append(gap)
                logger.warning(f"Data gap detected: {gap}")

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
            'trade_count': bar.trade_count,
            'spread': bar.high - bar.low,
            'price_change': bar.close - bar.open,
            'price_change_pct': ((bar.close - bar.open) / bar.open) * 100,
            'session_type': 'regular' if is_market_hours(bar.timestamp) else 'extended',
        }

        self.current_data.append(bar_dict)
        self.last_bar_time = bar.timestamp

        self.session_stats.update(bar)

        if len(self.current_data) >= 100:
            self.save_current_data()

    def save_current_data(self):
        if not self.current_data:
            return

        os.makedirs('data', exist_ok=True)

        df = pd.DataFrame(self.current_data)
        filename = f'data/SPY_{self.current_date}.csv'

        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)

        logger.info(f"Saved {len(self.current_data)} records to {filename}")
        self.current_data = []

    def run(self):
        logger.info("Starting SPY data streaming service...")

        stream = Stream(
            self.api_key,
            self.api_secret,
            base_url=self.paper_url,
            data_feed='iex'
        )
        stream.subscribe_bars(self.handle_bar, 'SPY')
        try:
        stream.run()
    except KeyboardInterrupt:
            self.save_current_data()
            self.save_session_stats()
            logger.info("Service stopped by user")
        except Exception as e:
        logger.error(f"Error in main loop: {e}")
            self.save_current_data()
            self.save_session_stats()

def main():
    API_KEY = 'PKKBHUDCGX3EYBURG6B6'
    API_SECRET = 'bn81IJO3rKU4POymKaC3iCt2k8mCanUtkmyXg0Gj'
    PAPER_URL = 'https://paper-api.alpaca.markets'

    collector = SPYDataCollector(API_KEY, API_SECRET, PAPER_URL)
    collector.run()

if __name__ == "__main__":
    main()
class SPYDataCollector:
    def __init__(self, api_key: str, api_secret: str, paper_url: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_url = paper_url
        self.current_data: List[Dict] = []
        self.current_date = None
        self.last_bar_time = None
        self.data_gaps = []
        self.session_stats = SessionStats()
        self.initialize_new_day()

    def initialize_new_day(self):
        if self.current_date != date.today():
            if self.current_data:
                self.save_current_data()
            self.current_date = date.today()
            self.current_data = []
            self.session_stats = SessionStats()
            logger.info(f"Initialized new day: {self.current_date}")

            if self.data_gaps:
                self.save_session_stats()

    def save_session_stats(self):
        stats = {
            'date': self.current_date.isoformat(),
            'session_high': self.session_stats.session_high,
            'session_low': self.session_stats.session_low,
            'total_volume': self.session_stats.volume_total,
            'total_trades': self.session_stats.trade_count_total,
            'bars_processed': self.session_stats.bars_processed,
            'data_gaps': self.data_gaps
        }

        stats_file = f'data/SPY_{self.current_date}_stats.json'
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Saved session statistics to {stats_file}")

    async def handle_bar(self, bar):
        bar_date = bar.timestamp.date()
        if self.current_date is None or bar_date != self.current_date:
            self.initialize_new_day()

        if self.last_bar_time:
            expected_time = self.last_bar_time + timedelta(minutes=1)
            if bar.timestamp > expected_time:
                gap = {
                    'start': expected_time.isoformat(),
                    'end': bar.timestamp.isoformat(),
                    'missing_minutes': (bar.timestamp - expected_time).seconds // 60
                }
                self.data_gaps.append(gap)
                logger.warning(f"Data gap detected: {gap}")

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
            'trade_count': bar.trade_count,
            'spread': bar.high - bar.low,
            'price_change': bar.close - bar.open,
            'price_change_pct': ((bar.close - bar.open) / bar.open) * 100,
            'session_type': 'regular' if is_market_hours(bar.timestamp) else 'extended',
        }

        self.current_data.append(bar_dict)
        self.last_bar_time = bar.timestamp

        self.session_stats.update(bar)

        if len(self.current_data) >= 100:
            self.save_current_data()

    def save_current_data(self):
        if not self.current_data:
            return

        os.makedirs('data', exist_ok=True)

        df = pd.DataFrame(self.current_data)
        filename = f'data/SPY_{self.current_date}.csv'

        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)

        logger.info(f"Saved {len(self.current_data)} records to {filename}")
        self.current_data = []

    def run(self):
        logger.info("Starting SPY data streaming service...")

        stream = Stream(
            self.api_key,
            self.api_secret,
            base_url=self.paper_url,
            data_feed='iex'
        )
        stream.subscribe_bars(self.handle_bar, 'SPY')
        try:
        stream.run()
    except KeyboardInterrupt:



            self.save_current_data()
            self.save_session_stats()
            logger.info("Service stopped by user")
        except Exception as e:
        logger.error(f"Error in main loop: {e}")

            self.save_current_data()
            self.save_session_stats()



def main():
    API_KEY = 'PKKBHUDCGX3EYBURG6B6'
    API_SECRET = 'bn81IJO3rKU4POymKaC3iCt2k8mCanUtkmyXg0Gj'
    PAPER_URL = 'https://paper-api.alpaca.markets'

    collector = SPYDataCollector(API_KEY, API_SECRET, PAPER_URL)
    collector.run()

if __name__ == "__main__":
    main()
