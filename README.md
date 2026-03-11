# 📊 Market Intelligence AI Agent

> **Automated company and competitor analysis powered by AI** — Save hours of manual research with intelligent news aggregation, vector storage, LLM analysis, and instant WhatsApp notifications.

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/at264939-ctrl/market-agent
cd Market-agent

# 2. Configure API keys
cp .env.example .env  # Or edit .env directly

# 3. Run with one click
./run.sh
```

Or analyze specific companies:
```bash
./run.sh -c "Apple,Microsoft,Google"
```

---

## ⏱️ Time Savings: Why This Matters

### Traditional Manual Research Process

| Task | Time Required |
|------|---------------|
| Search company news on Google | 30 min |
| Filter relevant articles | 45 min |
| Read and summarize articles | 60 min |
| Compare competitors | 45 min |
| Write executive summary | 30 min |
| Format and distribute report | 15 min |
| **Total** | **~3.75 hours** |

### With Market Intelligence Agent

| Task | Time Required |
|------|---------------|
| Configure companies | 1 min |
| Run automated analysis | 2 min (unattended) |
| Review WhatsApp summary | 3 min |
| **Total** | **~6 minutes** |

### 🎯 **Time Saved: 97% (3.5+ hours per analysis)**

---

## 🔧 Features

### 1. **Tavily News Search** 🔍
- Advanced web search for company news
- Real-time competitor monitoring
- Automatic relevance filtering

### 2. **ChromaDB Vector Storage** 💾
- Local vector database for article storage
- Semantic similarity search
- Persistent knowledge base

### 3. **Llama 3 Analysis via Groq** 🤖
- Ultra-fast LLM processing (70B parameters)
- Market trend analysis
- Competitive intelligence reports
- Strategic recommendations

### 4. **Twilio WhatsApp Notifications** 📱
- Instant executive summaries
- Mobile-first delivery
- Automated report distribution

---

## 📁 Project Structure

```
Market-agent/
├── market_agent.py      # Core agent classes
├── main.py              # CLI entry point
├── requirements.txt     # Python dependencies
├── .env                 # API credentials (create from .env.example)
├── .env.example         # Template for .env
├── run.sh               # One-click runner (colored output)
├── README.md            # This file
└── chroma_db/           # Vector database (auto-created)
```

---

## 🔑 Setup Instructions

### 1. Get API Keys

| Service | Purpose | Get Key |
|---------|---------|---------|
| **Groq** | Llama 3 LLM access | [console.groq.com](https://console.groq.com/keys) |
| **Tavily** | News search API | [app.tavily.com](https://app.tavily.com/api-keys) |
| **Twilio** | WhatsApp messaging | [console.twilio.com](https://console.twilio.com/) |

### 2. Configure Environment

Edit `.env` with your credentials:

```bash
# Groq API Key (for Llama 3 LLM)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# Tavily API Key (for news search)
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx

# Twilio Credentials (for WhatsApp)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Your WhatsApp number (recipient)
RECIPIENT_WHATSAPP_NUMBER=whatsapp:+1234567890
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the setup command:
```bash
./run.sh --setup
```

---

## 📖 Usage

### Basic Usage

```bash
# Run with default companies (Apple, Microsoft, Google)
./run.sh

# Analyze specific companies
./run.sh -c "Tesla,NVIDIA,AMD"

# Disable WhatsApp notifications
./run.sh -c "Amazon" -n
```

### Python CLI

```bash
# Basic analysis
python main.py --companies "Apple,Microsoft"

# Without notifications
python main.py -c "Tesla" --no-notification

# Verbose output
python main.py -c "Google" -v
```

### Programmatic Usage

```python
from market_agent import MarketIntelligenceAgent

# Initialize agent
agent = MarketIntelligenceAgent()

# Run analysis
results = agent.run_analysis(
    companies=["Apple", "Microsoft", "Google"],
    send_notification=True
)

# Access results
print(results["competitive_report"])
```

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐
│   Tavily API    │────▶│  TavilySearch    │
│  (News Search)  │     │    (Class)       │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
┌─────────────────┐     ┌──────────────────┐
│   ChromaDB      │◀────│  ChromaDBStore   │
│ (Vector Store)  │     │    (Class)       │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
┌─────────────────┐     ┌──────────────────┐
│   Groq API      │◀────│  GroqAnalyzer    │
│  (Llama 3 LLM)  │     │    (Class)       │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
┌─────────────────┐     ┌──────────────────┐
│   Twilio API    │◀────│  TwilioNotifier  │
│  (WhatsApp)     │     │    (Class)       │
└─────────────────┘     └──────────────────┘
```

---

## 📊 Sample Output

```
╔═══════════════════════════════════════════════════════════╗
║     📊  Market Intelligence AI Agent                     ║
║         Automated Company Analysis System                ║
╚═══════════════════════════════════════════════════════════╝

▶ Checking Python installation...
✓ Found Python 3.10.12

▶ Checking environment configuration...
✓ Environment configured

▶ Installing Python dependencies...
✓ Dependencies installed

▶ Starting Market Intelligence Agent...

📌 Analyzing: Apple, Microsoft, Google
📱 Notifications: Enabled

============================================================
🎯 Starting Market Intelligence Analysis
============================================================

📰 STEP 1: Searching & Storing News
----------------------------------------
🔍 Searching Tavily for: Apple company news 2024 2025
✅ Found 10 articles
💾 Storing 10 articles for Apple
...

🧠 STEP 2: Analyzing Market Trends
----------------------------------------
🤖 Analyzing trends for Apple using Llama 3
✅ Analysis complete for Apple
...

📊 STEP 3: Generating Competitive Report
----------------------------------------
🤖 Generating competitive analysis report
✅ Competitive report generated

📱 STEP 4: Sending WhatsApp Notification
----------------------------------------
📱 Sending WhatsApp message...
✅ Message sent! SID: SMxxxxxxxxxxxx

============================================================
✅ Analysis Complete!
============================================================
💾 Report saved to: market_report_20250305_143022.txt
```

---

## 🔒 Security Notes

- Never commit `.env` to version control
- Rotate API keys regularly
- Use environment variables in production
- Restrict Twilio WhatsApp numbers to authorized recipients

---

## 🛠️ Troubleshooting

### "API Key not found"
Ensure `.env` file exists and contains valid keys:
```bash
cat .env | grep GROQ_API_KEY
```

### "Module not found"
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### "Twilio message failed"
- Verify WhatsApp sandbox is activated
- Check phone number format (must include `whatsapp:+`)
- Ensure account has sufficient credits

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

**Built with ❤️ using Python, Tavily, ChromaDB, Groq (Llama 3), and Twilio**
