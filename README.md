# 📈 Stock Alert

A Python application that monitors stock price changes and sends SMS alerts when thresholds are exceeded. The application fetches stock data from Alpha Vantage and relevant news articles, then sends formatted alerts via Twilio.

### 🔄 Recent Updates

- **Improved Error Handling**: Added specific exceptions and better error messages
- **Code Organization**: Moved utility functions to `utils.py` for better separation of concerns
- **SMS Formatting**: Enhanced message formatting with better handling of character limits
- **Trial Mode Support**: Special handling for Twilio trial account limitations
- **Clean Code**: Improved code structure and documentation

### ⚠️ Twilio Trial Mode Notice

In trial mode, the application will:
- Send only the first news article
- Format messages to fit within 160 characters
- Include basic stock movement information
- Automatically shorten URLs

For production use with a paid Twilio account, the application supports:
- Multiple news articles per alert
- Full message formatting with emojis
- Detailed stock information


## 📜 Development History

- **Initial Development**: The core functionality was developed independently as part of a coding exercise.
- **Refactoring**: The code was later refactored with assistance from GitHub Copilot and Cascade to improve code quality, error handling, and maintainability.
- **Current State**: The application is now more robust, with better separation of concerns and error handling.

## 🚀 Features

- **Stock Monitoring**: Fetches real-time stock data from Alpha Vantage API
- **Smart Alerts**: Evaluates percentage change against a configurable threshold
- **News Integration**: Retrieves relevant news articles for context
- **SMS Notifications**: Sends formatted alerts via Twilio
- **Trial Mode Support**: Special handling for Twilio trial account limitations
- **Error Handling**: Comprehensive error handling and logging
- **Configuration**: Simple setup using `.env` file
- **Modular Design**: Clean, maintainable code structure

## 🧱 Project Structure

```
.
├── config.py          # Loads and validates environment variables
├── data_fetch.py      # Fetches stock data and news articles
├── sms.py             # Handles SMS preparation and sending
├── utils.py           # Utility functions and calculations
├── main.py            # Main application entry point
├── .env               # Configuration (not committed)
├── requirements.txt   # Project dependencies
└── HOW_IT_WORKS.md    # Detailed explanation of the application flow
```

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SLS-BLN/stock_alert.git
   cd stock_alert
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**
   ```env
   # Twilio Configuration
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   MY_PHONE_NUMBER=+1234567890
   
   # Alpha Vantage API
   ALPHAVANTAGE_API_KEY=your_api_key
   ALPHAVANTAGE_API_ENDPOINT=https://www.alphavantage.co/query
   
   # News API
   NEWS_API_KEY=your_news_api_key
   NEWS_API_ENDPOINT=https://newsapi.org/v2/everything
   
   # Application Settings
   STOCK=TSLA
   COMPANY_NAME=Tesla
   THRESHOLD=5.0
   TWILIO_TRIAL_MODE=true
   ```

5. **Run the app**
   ```bash
   python main.py
   ```

---

## 🧠 TODOs

- [ ] Add CLI interface for better user interaction
- [ ] Add more comprehensive error handling
- [ ] Implement unit tests
- [ ] Add support for multiple stocks
- [ ] Add configuration options via command line arguments

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

- [ ] Replace `print()` with structured logging
- [ ] Add CLI support with `argparse`
- [ ] Add unit tests for core modules
- [ ] Abstract SMS provider for flexibility
- [ ] Implement retry logic for API calls
- [ ] Add caching for stock data
- [ ] Improve error handling and config validation

---

## 👨‍💻 Author

**Stefan** — Berlin-based developer refining Python skills and building real-world tools.  
Bootcamp attendee, focused on clean architecture, automation, and practical problem-solving.

---

## 📄 License

This project is licensed under the MIT License.
