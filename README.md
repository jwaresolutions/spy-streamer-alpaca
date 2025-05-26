# Bitcoin/USD Data Streaming Service

A Python service that streams real-time Bitcoin/USD market data using Polygon.io's API and saves it to daily CSV files. The service captures minute-by-minute data 24/7 and maintains daily statistics.

## Features

- Real-time minute-by-minute BTC/USD data collection
- 24/7 data collection (including weekends)
- Automatic daily file management
- Data quality monitoring and gap detection
- Daily statistics tracking
- Systemd service integration for reliable operation

## Prerequisites

- Python 3.8 or higher
- Polygon.io account (Starter tier or higher)
- Linux system with systemd (for service deployment)

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-directory]
```
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy configuration template and edit with your API key:
```bash
cp config.template.py config.py
vim config.py  # Replace 'your_polygon_api_key_here' with your actual API key
```

## Service Setup
1. update 2 instances of `{location to source}` with the correct location to source i.e. `ExecStart=/home/user/project/venv/bin/python /home/user/project/src/crypto_stream_service.py`
2. Copy updated service file to service directory:
```bash
sudo cp crypto-stream.service /etc/systemd/system/crypto-stream.service
```
3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable crypto-stream
sudo systemctl start crypto-stream
```

## other commands
1. Check service status:
```bash
sudo systemctl status crypto-stream
```

2. View logs
```bash
journalctl -u crypto-stream -f
```

3. Restart service
```bash
./restart-crypto-service.sh
```

4. Test Polygon connection
```bash
python test_polygon.py
```
