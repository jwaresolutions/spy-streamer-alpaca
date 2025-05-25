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