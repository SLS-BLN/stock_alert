# 📖 How the Stock Alert System Works

This document provides a detailed explanation of the Stock Alert system's architecture and functionality. The application follows functional programming principles and has been refactored for better code organization and error handling.

## 🏗️ System Architecture

The application follows a functional design with clear separation of concerns:

```
main.py            # Entry point and orchestration
├── config.py      # Configuration management and validation
├── data_fetch.py  # Data retrieval from external APIs
├── sms.py         # SMS notification handling with trial mode support
└── utils.py       # Core business logic and calculations
```

## 🔄 Workflow Overview

1. **Configuration Loading**
   - Loads and validates environment variables from `.env`
   - Handles missing or invalid configuration
   - Sets up application parameters with type safety

2. **Stock Data Processing**
   - Fetches stock data from Alpha Vantage API
   - Extracts latest and previous day's closing prices
   - Calculates percentage change with proper error handling

3. **Threshold Evaluation**
   - Compares price change against configurable threshold
   - Proceeds only if threshold is exceeded
   - Handles both positive and negative price movements

4. **News Integration**
   - Fetches relevant news articles based on company name
   - Extracts title, description, and URL
   - Limits results based on configuration

5. **Smart Notification**
   - Adapts message format based on trial/production mode
   - Handles SMS character limits automatically
   - Provides clear, actionable alerts with relevant context

## 🧩 Core Components

### 1. `main.py`
- **Purpose**: Application entry point and workflow orchestration
- **Key Functions**:
  - `main()`: Loads configuration and runs the alert pipeline
  - `run_alert_pipeline()`: Coordinates the entire workflow
  - Handles error states and provides user feedback

### 2. `config.py`
- **Purpose**: Manages application configuration and environment
- **Key Features**:
  - Validates required environment variables
  - Provides type-safe configuration access
  - Handles missing or invalid configuration gracefully
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
