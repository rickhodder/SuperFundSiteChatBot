# 🚀 Quick Start Guide

## Prerequisites
- Python 3.9 or higher
- pip (Python package installer)
- OpenAI API key (get one at https://platform.openai.com/api-keys)

## Setup Instructions

### Option 1: Automated Setup (Recommended)

1. **Run setup script:**
   ```cmd
   setup.bat
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Display next steps

2. **Configure API key:**
   ```cmd
   copy .env.example .env
   notepad .env
   ```
   Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **Test the system:**
   ```cmd
   venv\Scripts\activate
   python test_system.py
   ```

4. **Run the app:**
   ```cmd
   run.bat
   ```
   Or manually:
   ```cmd
   venv\Scripts\activate
   streamlit run app.py
   ```

### Option 2: Manual Setup

1. **Create virtual environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```cmd
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```cmd
   copy .env.example .env
   ```
   Edit `.env` and add your OpenAI API key.

4. **Test and run:**
   ```cmd
   python test_system.py
   streamlit run app.py
   ```

## Testing the App

### Test Addresses

The sample data includes 14 SuperFund sites. Try these addresses:

**High-risk area (multiple nearby sites):**
- `123 5th Street, Brooklyn, NY 11215` (near Gowanus Canal)

**Medium-risk area:**
- `456 Park Ave, Los Angeles, CA 90001` (near San Fernando Valley)

**Low-risk area (completed sites only):**
- `789 Main St, Niagara Falls, NY 14304` (near Love Canal - remediated)

**Safe area (no nearby sites):**
- `100 Pike St, Seattle, WA 98101` (far from any sites)

### Expected Results

**Brooklyn address:**
- Should find 1-2 unremediated sites within 50 miles
- Safety score: 50-75 (MEDIUM or LOW risk)
- Data grid shows Gowanus Canal and/or Newtown Creek

**Los Angeles address:**
- Should find 1-2 sites
- Safety score: 50-75
- Shows San Fernando Valley contamination

**Niagara Falls address:**
- May find Love Canal (completed)
- Safety score: 75-100 (LOW or SAFE risk)

## Verifying Everything Works

Run the system test:
```cmd
python test_system.py
```

You should see:
```
✅ All required packages installed
✅ Config loaded
✅ CSV loaded: 14 SuperFund sites
✅ Backend initialized: CSVBackend
✅ Geospatial query works
✅ SafetyScorer works
✅ All tests passed! Ready to run: streamlit run app.py
```

## Using the App

1. **Open browser** at http://localhost:8501

2. **Enter an address** in the chat:
   ```
   What's the safety score for 123 5th Street, Brooklyn, NY?
   ```

3. **View results:**
   - Chat shows safety score and risk level
   - Data Grid section auto-expands with nearby sites
   - Use expand/collapse/maximize buttons on each section

4. **Explore sections:**
   - **Chat (60% left):** Enter queries, view conversational results
   - **Data Grid (40% right):** Sortable table of nearby sites
   - **Map View:** Placeholder for Phase 2 visualization
   - **Debug:** Enable in .env with `DEBUG_MODE=True`

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "OPENAI_API_KEY not set"
- Copy `.env.example` to `.env`
- Add your API key to `.env`
- Restart the app

### "CSV file not found"
- Ensure `data/raw/superfund_sites.csv` exists
- Sample data is included in the repository

### "Could not geocode address"
- Nominatim API has rate limits
- Try a more specific address (include city, state, zip)
- Wait a few seconds between requests

### Port 8501 already in use
- Stop existing Streamlit app
- Or run on different port: `streamlit run app.py --server.port 8502`

## Next Steps

### Phase 2 Enhancements (TODO)
- Switch to Vector Store backend
- Add interactive Folium maps
- Implement RAG report generation
- Add LangChain query classification

### Development
- Read [TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) for architecture details
- Read [PRD.md](docs/PRD.md) for product requirements
- Run tests: `python test_system.py`
- Format code: `black src/ app.py`

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Review [docs/PRD.md](docs/PRD.md) for features and requirements
- Review [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) for implementation details

## 🎉 You're Ready!

If all tests pass, run:
```cmd
streamlit run app.py
```

Enjoy checking SuperFund site safety! 🏭✅
