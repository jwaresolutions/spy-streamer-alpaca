SPY Stock Data Streaming Service
A Python service that streams real-time SPY (S&P 500 ETF) market data using Alpaca's API and saves it to daily CSV files. The service captures minute-by-minute data during market hours and maintains daily statistics.

Features
Real-time minute-by-minute SPY data collection
Automatic daily file management
Market session awareness (regular vs extended hours)
Data quality monitoring and gap detection
Daily statistics tracking
Systemd service integration for reliable operation
Prerequisites
Python 3.8 or higher
Alpaca Markets account (Paper trading is fine)
Linux system with systemd (for service deployment)
Installation
Clone the repository: git clone [your-repo-url] cd [repo-directory]

Create and activate a virtual environment (recommended): python3 -m venv venv source venv/bin/activate

Install dependencies: pip install -r requirements.txt

Configure your Alpaca API credentials in the script or use environment variables.

Configuration
Update the following variables in spy_stream_service.py with your Alpaca credentials:

API_KEY = 'your_api_key' API_SECRET = 'your_secret_key'

Running the Service
Manual Execution
Run the script directly: python spy_stream_service.py

As a Systemd Service
Create the service file: sudo vim /etc/systemd/system/spy-stream.service

Add the following configuration (adjust paths as needed): [Unit] Description=SPY Streaming Data Service After=network.target

[Service] Type=simple User=root WorkingDirectory=/root/src ExecStart=/usr/bin/python3 /root/src/spy_stream_service.py Restart=always RestartSec=10

[Install] WantedBy=multi-user.target

Enable and start the service: sudo systemctl enable spy-stream sudo systemctl start spy-stream
Data Output
The service creates two types of files in the data directory:

Daily Data Files: SPY_YYYY-MM-DD.csv

Timestamp (UTC and EST)
OHLC prices
Volume
VWAP
Trade count
Spread
Price changes
Session type
Daily Statistics: SPY_YYYY-MM-DD_stats.json

Session high/low
Total volume
Total trades
Data quality metrics
Gap detection
Monitoring
Check service status: sudo systemctl status spy-stream

View live logs: journalctl -u spy-stream -f

Service Management
Start the service
sudo systemctl start spy-stream

Stop the service
sudo systemctl stop spy-stream

Restart the service
sudo systemctl restart spy-stream

View service logs
journalctl -u spy-stream -f

Data Structure
CSV Columns
timestamp: UTC timestamp
timestamp_est: Eastern Time timestamp
open: Opening price
high: Highest price
low: Lowest price
close: Closing price
volume: Trading volume
vwap: Volume Weighted Average Price
trade_count: Number of trades
spread: High-Low spread
price_change: Absolute price change
price_change_pct: Percentage price change
session_type: Market session identifier
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
[Your chosen license]

Disclaimer
This software is for educational purposes only. Use at your own risk. Market data provided by Alpaca Markets.
