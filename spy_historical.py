import pandas as pd
from datetime import datetime, timedelta
from alpaca_trade_api.rest import REST
import pytz
import time

# Alpaca API credentials
API_KEY = 'PKKBHUDCGX3EYBURG6B6'
API_SECRET = 'bn81IJO3rKU4POymKaC3iCt2k8mCanUtkmyXg0Gj'
ALPACA_ENDPOINT = 'https://paper-api.alpaca.markets'

# Initialize Alpaca API
api = REST(API_KEY, API_SECRET, ALPACA_ENDPOINT)

def fetch_historical_data():
    try:
        # Set up time parameters - fetch from 2 years ago until yesterday
        end_date = datetime.now(pytz.UTC) - timedelta(days=1)  # Yesterday
        start_date = end_date - timedelta(days=730)  # 2 years before end date
        
        print(f"Fetching SPY minute data from {start_date} to {end_date}")
        
        # Fetch data in smaller chunks to avoid timeouts (3-month chunks)
        chunk_size = timedelta(days=90)
        current_start = start_date
        all_bars = []
        
        while current_start < end_date:
            current_end = min(current_start + chunk_size, end_date)
            print(f"Fetching chunk: {current_start} to {current_end}")
            
            try:
                # Get bars for current chunk
                bars = api.get_bars(
                    symbol='SPY',
                    timeframe='1Min',
                    start=current_start.isoformat(),
                    end=current_end.isoformat(),
                    adjustment='raw'
                )
                
                all_bars.extend(bars)
                print(f"Retrieved {len(bars)} bars for current chunk")
                
                # Move to next chunk
                current_start = current_end
                time.sleep(2)  # Increased pause between chunks
                
            except Exception as chunk_error:
                print(f"Error fetching chunk: {str(chunk_error)}")
                time.sleep(5)  # Longer pause on error
                continue
        
        if not all_bars:
            print("No data was retrieved!")
            return
            
        # Convert all bars to DataFrame
        df = pd.DataFrame([
            {
                'timestamp': bar.t,
                'open': bar.o,
                'high': bar.h,
                'low': bar.l,
                'close': bar.c,
                'volume': bar.v,
                'vwap': bar.vw,
                'trades': bar.n
            } for bar in all_bars
        ])
        
        # Save to CSV
        filename = f'SPY_minute_data_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv'
        df.to_csv(filename, index=False)
        print(f"\nData successfully saved to {filename}")
        print(f"Total bars retrieved: {len(df)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    fetch_historical_data()