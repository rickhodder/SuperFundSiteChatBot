# 🏭 SuperFund Site Safety Checker

A Streamlit chatbot that checks insurance policy safety based on proximity to EPA SuperFund sites. Uses geospatial analysis and a safety scoring algorithm to assess environmental risks.

## ✨ Features

- **Safety Scoring Algorithm**: Start at 100%, deduct 25% per unremediated site within 50 miles
- **Smart Data Display**: Grid view with sorting, filtering, and action buttons
- **Dynamic Sections**: Expand/collapse/maximize UI sections programmatically
- **Geospatial Analysis**: Distance calculations using Specification pattern
- **Swappable Backends**: Strategy pattern enables CSV → Vector store migration
- **Interactive Chat**: Natural language queries for policy safety checks

## 🏗️ Architecture

- **Strategy Pattern**: `IDataBackend` interface with CSV and Vector Store implementations
- **Specification Pattern**: Composable geospatial and filter queries
- **Modular Design**: Separation of UI components and business logic
- **Session Management**: Streamlit session state for section control

## 📋 Requirements

- Python 3.9+
- Streamlit 1.28+
- See `requirements.txt` for full dependencies

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/SuperFundSiteChatBot.git
cd SuperFundSiteChatBot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 5. Run Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📊 Sample Data

A sample CSV with 14 SuperFund sites is included in `data/raw/superfund_sites.csv`. Test addresses:

- **Brooklyn, NY** (near Gowanus Canal & Newtown Creek)
- **Los Angeles, CA** (near San Fernando Valley contamination)
- **Niagara Falls, NY** (near Love Canal - completed site)

## 🎯 Usage

1. Enter an address in the chat: `"123 Main St, Brooklyn, NY"`
2. View safety score and risk level
3. Inspect nearby sites in the data grid
4. Expand map section for visualization (Phase 2)

### Example Queries
- `"What's the safety score for 456 Park Ave, New York, NY?"`
- `"Check this address: 789 Oak St, Los Angeles, CA"`

## 📁 Project Structure

```
SuperFundSiteChatBot/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── config/
│   └── settings.py        # Configuration management
├── src/
│   ├── strategy.py        # Backend Strategy pattern
│   ├── specifications.py  # Query Specification pattern
│   ├── safety_scorer.py   # Safety scoring algorithm
│   └── section_manager.py # UI section control
├── data/
│   ├── raw/              # Source CSV files
│   ├── processed/        # Processed data
│   └── embeddings/       # Vector embeddings (Phase 2)
└── docs/
    ├── PRD.md            # Product Requirements
    └── TECHNICAL_SPEC.md # Technical Specification
```

## 🔧 Configuration

Key settings in `config/settings.py`:

- `PROXIMITY_RADIUS_MILES`: Search radius (default: 50)
- `SCORE_PENALTY_PER_SITE`: Deduction per site (default: 25)
- `INITIAL_SCORE`: Starting score (default: 100)

## 🧪 Development Phases

### Phase 1: MVP (Completed) ✅
- CSV backend with geospatial queries
- Safety scoring algorithm
- Chat interface with section management
- Data grid display

### Phase 2: Enhanced (In Progress)
- Vector store backend (ChromaDB)
- Interactive map with Folium
- RAG report generation
- LangChain integration

### Phase 3: Advanced (Planned)
- Multi-model LLM support
- Advanced analytics dashboard
- Batch policy processing
- Export capabilities

## 🤝 Contributing

Contributions welcome! Please see development setup in `docs/TECHNICAL_SPEC.md`.

## 📄 License

MIT License - see LICENSE file

## 🐛 Troubleshooting

**Error: "OPENAI_API_KEY not set"**
- Copy `.env.example` to `.env` and add your API key

**Error: "CSV file not found"**
- Ensure `data/raw/superfund_sites.csv` exists
- Check `DATA_PATH` setting in `.env`

**Geocoding errors**
- GeoPy uses Nominatim (rate-limited)
- Add delays between batch requests
- Consider upgrading to paid geocoding service

## 📚 Documentation

- [Product Requirements Document](docs/PRD.md)
- [Technical Specification](docs/TECHNICAL_SPEC.md)

## 🙏 Acknowledgments

- EPA SuperFund data
- Streamlit framework
- LangChain library
Streamlit/Python based chatbot
