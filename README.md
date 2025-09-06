# 📈 Stock Alert

A modular Python application that monitors stock price changes and sends SMS alerts when thresholds are exceeded. Designed for clarity, extensibility, and real-world use cases.

---

## 🚀 Features

- Fetches real-time stock data
- Evaluates percentage change against a configurable threshold
- Sends SMS alerts via Twilio
- Retrieves contextual news headlines
- Uses `.env` for secure configuration
- Modular structure with clear separation of concerns
- Logging integrated across all modules

---

## 🧱 Project Structure

```
.
├── config.py          # Loads and validates environment variables
├── data_fetch.py      # Fetches stock data and news articles
├── sms.py             # Prepares and sends SMS alerts
├── utils.py           # Evaluates stock change logic
├── main.py            # Entry point for the alert pipeline
├── pipeline.py        # Orchestrates the alert workflow
├── logger.py          # Centralized logging setup
├── .env               # Stores secrets (not committed)
├── .gitignore         # Ignores sensitive and build files
```

---

## ⚙️ Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/SLS-BLN/stock_alert.git
   cd stock_alert
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**
   ```env
   API_KEY=your_stock_api_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=+1234567890
   TARGET_PHONE_NUMBER=+0987654321
   STOCK_SYMBOL=AAPL
   THRESHOLD=5.0
   ```

5. **Run the app**
   ```bash
   python main.py
   ```

---

## 🧠 TODOs

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
