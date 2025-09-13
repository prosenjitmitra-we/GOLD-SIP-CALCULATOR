# 🏆 Gold SIP Calculator Chatbot

A comprehensive Gold SIP (Systematic Investment Plan) calculator with multiple interfaces - web app, Streamlit dashboard, and Telegram bot. Calculate your gold investment returns, get live gold prices, and receive investment insights.

## ✨ Features

- **💰 SIP Return Calculation**: Calculate profit/loss, CAGR, and total returns for your gold SIP investments
- **📊 Interactive Dashboard**: Beautiful Streamlit dashboard with charts and visualizations
- **🤖 Web Chatbot**: Flask-based conversational interface for easy calculations
- **📱 Telegram Bot**: Chat with the bot on Telegram for on-the-go calculations
- **💎 Live Gold Prices**: Real-time gold price integration with multiple API sources
- **📈 Investment Insights**: Monthly breakdown, price sensitivity analysis, and investment tips
- **📄 Reports**: Download detailed investment reports

## 🏗️ Architecture

```
gold-sip-chatbot/
├── src/                     # Core calculation logic
│   ├── gold_sip_calculator.py    # Main calculator class
│   └── gold_price_api.py         # Live price API integration
├── web/                     # Flask web application
│   ├── app.py                    # Flask server
│   └── templates/
│       └── index.html            # Chatbot interface
├── telegram/                # Telegram bot
│   └── telegram_bot.py           # Bot implementation
├── streamlit_app.py         # Streamlit dashboard
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the project
git clone <repository-url>
cd gold-sip-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test the Core Calculator

```bash
# Run the core calculator test
python src/gold_sip_calculator.py
```

### 3. Launch Web Applications

#### Flask Web Chatbot
```bash
# Start the Flask web server
python web/app.py
```
Visit: `http://localhost:5000`

#### Streamlit Dashboard
```bash
# Start the Streamlit dashboard
streamlit run streamlit_app.py
```
Visit: `http://localhost:8501`

### 4. Setup Telegram Bot (Optional)

1. **Create Telegram Bot**:
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Get your bot token

2. **Configure Token**:
   ```python
   # In telegram/telegram_bot.py, replace:
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   # With your actual token
   ```

3. **Run the Bot**:
   ```bash
   python telegram/telegram_bot.py
   ```

## 💡 Usage Examples

### Basic SIP Calculation

```python
from src.gold_sip_calculator import GoldSIPCalculator

calculator = GoldSIPCalculator()

results = calculator.calculate_sip_returns(
    monthly_amount=10000,      # ₹10,000 per month
    duration_months=24,        # 2 years
    average_gold_price=8000,   # ₹8,000/gram average (historical)
    current_gold_price=10500   # ₹10,500/gram current
)

print(f"Total Investment: ₹{results['total_investment']:,.0f}")
print(f"Current Value: ₹{results['current_value']:,.0f}")
print(f"Profit/Loss: ₹{results['profit_loss']:,.0f} ({results['profit_loss_percentage']:.2f}%)")
print(f"CAGR: {results['cagr']:.2f}% per annum") # Shows realistic ~12.5% with historical prices
```

### Live Gold Price

```python
from src.gold_price_api import get_live_gold_price

current_price = get_live_gold_price()
print(f"Current Gold Price: ₹{current_price}/gram")
```

## 🔧 Configuration

### Gold Price API Setup (Optional)

For live gold prices, you can configure API keys:

1. **MetalPriceAPI** (Free: 100 requests/month):
   - Sign up at https://metalpriceapi.com
   - Get your API key
   - Set in `src/gold_price_api.py`

2. **GoldAPI** (Free: 1000 requests/month):
   - Sign up at https://goldapi.io
   - Get your API key
   - Set in `src/gold_price_api.py`

3. **FCS API** (Free: 500 requests/month):
   - Sign up at https://fcsapi.com
   - Get your API key
   - Set in `src/gold_price_api.py`

**Note**: The app works with mock prices if no API keys are configured.

### Environment Variables (Optional)

Create a `.env` file for production:

```env
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# Gold Price APIs
METALPRICEAPI_KEY=your-metalpriceapi-key
GOLDAPI_KEY=your-goldapi-key
FCS_API_KEY=your-fcs-api-key
```

## 📊 Features Overview

### Web Chatbot (Flask)
- **Conversational Interface**: Step-by-step input collection
- **Live Gold Prices**: Real-time price display
- **Session Management**: Maintains conversation state
- **Responsive Design**: Works on mobile and desktop
- **Interactive Results**: Options for breakdown and tips

### Streamlit Dashboard
- **Interactive Charts**: Plotly-powered visualizations
- **Price Sensitivity**: Analyze returns vs price changes
- **Monthly Breakdown**: Detailed month-wise investment data
- **Scenario Analysis**: Compare different investment amounts
- **Download Reports**: Export calculation results

### Telegram Bot
- **Inline Keyboards**: Easy button-based navigation
- **Command Support**: `/start`, `/price`, `/tips`, `/help`
- **Multi-user Support**: Handles multiple conversations
- **Rich Formatting**: Markdown-formatted responses
- **Error Handling**: Graceful error messages

## 🧮 Calculation Logic

### Core Formula

```
Total Units Bought = (Monthly Amount × Duration) ÷ Average Gold Price
Current Value = Total Units × Current Gold Price
Profit/Loss = Current Value - Total Investment
CAGR = ((Current Value ÷ Total Investment) ^ (1/Years)) - 1
```

### Key Metrics
- **Total Investment**: Sum of all monthly investments
- **Gold Purchased**: Total grams of gold accumulated
- **Current Value**: Market value of gold at current prices
- **Profit/Loss**: Absolute and percentage returns
- **CAGR**: Compound Annual Growth Rate

### 📈 Historical Performance Context

**Gold has delivered excellent returns over the last decade:**
- **10-Year CAGR (2015-2025)**: ~12.5% per annum
- **2015 Price**: ~₹2,600/gram
- **2025 Price**: ~₹10,500/gram

**For realistic calculations, use historical average prices:**
- **Recent SIP (1-2 years)**: Average ₹9,000-9,500/gram
- **Medium-term SIP (2-3 years)**: Average ₹7,500-8,500/gram  
- **Long-term SIP (5+ years)**: Average ₹5,000-7,000/gram

💡 **Pro Tip**: The calculator computes CAGR based on your inputs. Use lower average prices to reflect historical SIP scenarios and see the true potential of gold investments!

## 🛠️ Development

### Project Structure
- `src/`: Core business logic and calculations
- `web/`: Flask web application
- `telegram/`: Telegram bot implementation
- `tests/`: Unit tests (to be added)
- `data/`: Data files and cache (auto-generated)

### Adding New Features

1. **Core Logic**: Add new calculation methods to `GoldSIPCalculator`
2. **Web Interface**: Extend Flask routes and templates
3. **Dashboard**: Add new Streamlit components
4. **Bot**: Extend Telegram bot handlers

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests (when implemented)
python -m pytest tests/
```

## 🚀 Deployment

### Flask Web App

#### Local Development
```bash
python web/app.py
```

#### Production (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 web.app:app
```

### Streamlit Dashboard

#### Local
```bash
streamlit run streamlit_app.py
```

#### Production
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Telegram Bot

#### Local/Server
```bash
python telegram/telegram_bot.py
```

#### As Service (Linux)
Create a systemd service file for production deployment.

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# For Flask
EXPOSE 5000
CMD ["python", "web/app.py"]

# For Streamlit
# EXPOSE 8501
# CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## 💡 Gold Investment Tips

### Best Practices
- **Consistency**: Invest the same amount monthly regardless of gold prices
- **Long-term Focus**: Gold SIP works best for 3+ years investment horizon
- **Portfolio Allocation**: Keep gold allocation to 5-15% of your portfolio
- **Digital Gold**: Consider digital gold for lower costs and easy liquidity

### When to Invest in Gold
- **Market Uncertainty**: Gold acts as a hedge during volatile times
- **Inflation**: Historically performs well during high inflation periods
- **Portfolio Diversification**: As part of a balanced investment strategy
- **Goal-based Planning**: For long-term goals like weddings, retirement

## ⚠️ Important Notes

### Limitations
- **No Income Generation**: Gold doesn't provide dividends or interest
- **Price Volatility**: Short-term price fluctuations are normal
- **Tax Implications**: Consider capital gains tax on gold investments
- **Storage Costs**: Physical gold has making charges and storage costs

### Disclaimer
This tool is for educational and planning purposes only. Past performance doesn't guarantee future returns. Please consult a financial advisor for investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 📞 Support

For questions, suggestions, or issues:
- Open a GitHub issue
- Contact: https://shorturl.at/ublTG

---

**Built with ❤️ for smart gold investors** 🏆💛

## 🎯 Roadmap

- [ ] Database integration for historical data
- [ ] User accounts and portfolio tracking
- [ ] Mobile app development
- [ ] Advanced charting and technical analysis
- [ ] Integration with investment platforms
- [ ] Multi-language support
- [ ] Real-time notifications

- [ ] Automated SIP recommendations
