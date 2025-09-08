# 📈 Stock Alert

A Python application that monitors stock price changes and sends SMS alerts when thresholds are exceeded. This project was initially developed as part of a learning exercise and later refactored for better code quality and maintainability.

### ⚠️ Twilio SMS Delivery Limitation (Development Mode)

**Note:** SMS messages may fail to send when using a Twilio **Trial account** due to strict character limits.

- Trial accounts allow only **1 SMS segment** per message.
- Messages with **Unicode symbols** (e.g., 📈, 🟢, ▲) are encoded differently, reducing the limit to **70 characters**.
- Even without emojis, longer headlines or verbose content can exceed the **160-character GSM limit**.

This behavior is **intentional during development** to preserve formatting and test full message structure. In production, with a paid Twilio account, these limits are relaxed and multi-segment messages are supported.

To debug delivery issues, check the Twilio **Error Logs**:
> **Twilio Console → Account Dashboard → Monitor → Errors → Error Logs**  
> Look for error code: **30044 – Trial Message Length Exceeded**

You can also shorten messages or remove emojis to stay within trial limits if needed.


## 📜 Development History

- **Initial Development**: The core functionality was developed independently as part of a coding exercise.
- **Refactoring**: The code was later refactored with assistance from GitHub Copilot and Cascade to improve code quality, error handling, and maintainability.
- **Current State**: The application is now more robust, with better separation of concerns and error handling.

## 🚀 Features

- Fetches real-time stock data from Alpha Vantage API
- Evaluates percentage change against a configurable threshold
- Sends SMS alerts via Twilio
- Retrieves relevant news articles
- Simple configuration using `.env` file
- Clean, modular code structure

## 🧱 Project Structure

```
.
├── config.py          # Loads and validates environment variables
├── data_fetch.py      # Fetches stock data and news articles
├── sms.py             # Handles SMS preparation and sending
├── utils.py           # Utility functions and calculations
├── main.py            # Main application entry point
├── .env               # Configuration (not committed)
└── requirements.txt   # Project dependencies
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
