# 📖 How the Stock Alert System Works

This document provides a detailed explanation of the Stock Alert system's architecture and functionality. The application was initially developed independently and later refactored with assistance from GitHub Copilot and Cascade to improve code quality and maintainability.

## 🏗️ System Architecture

The application follows a modular design with clear separation of concerns:

```
main.py            # Entry point and orchestration
├── config.py      # Configuration management
├── data_fetch.py  # Data retrieval from external APIs
├── sms.py         # SMS notification handling
└── utils.py       # Helper functions and calculations
```

## 🔄 Workflow Overview

1. **Configuration Loading**
   - Loads environment variables from `.env`
   - Validates required configuration
   - Sets up application parameters

2. **Stock Data Fetching**
   - Retrieves stock data from Alpha Vantage API
   - Processes the latest stock prices
   - Calculates percentage change

3. **Threshold Check**
   - Compares price change against threshold
   - Proceeds only if threshold is exceeded

4. **News Retrieval**
   - Fetches relevant news articles
   - Formats article titles and URLs

5. **Notification**
   - Prepares SMS message with stock data and news
   - Sends notification via Twilio

## 🧩 Core Components

### 1. `main.py`
- **Purpose**: Application entry point and workflow orchestration
- **Key Functions**:
  - `main()`: Initializes and runs the alert pipeline
  - `run_alert_pipeline()`: Executes the main workflow

### 2. `config.py`
- **Purpose**: Manages application configuration
- **Key Features**:
  - Loads environment variables
  - Validates required settings
  - Handles type conversion

### 3. `data_fetch.py`
- **Purpose**: Handles external API communication
- **Key Functions**:
  - `fetch_stock_data()`: Gets stock data from Alpha Vantage
  - `fetch_news_articles()`: Retrieves relevant news
  - `extract_latest_prices()`: Processes price data

### 4. `sms.py`
- **Purpose**: Manages SMS notifications
- **Key Functions**:
  - `prepare_sms()`: Formats message content
  - `send_sms()`: Handles Twilio communication

### 5. `utils.py`
- **Purpose**: Provides utility functions
- **Key Functions**:
  - `calculate_percentage_change()`: Computes price changes
  - `is_threshold_reached()`: Checks threshold condition
  - `shorten_url()`: Shortens URLs for SMS

## 🔄 Data Flow

1. Configuration is loaded and validated
2. Stock data is fetched and processed
3. If significant change is detected:
   - News articles are retrieved
   - SMS message is prepared and sent
4. Results are reported to the console

## 🛠️ Development Notes

- The code follows Python best practices
- Type hints are used for better code clarity
- Error handling is implemented throughout
- Configuration is managed through environment variables

## 🔄 Future Improvements

- Add command-line interface
- Implement logging
- Add unit tests
- Support multiple stocks
- Add caching for API responses
- Improve error handling and retries
