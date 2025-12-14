# 🏗️ Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        app.py (Streamlit UI)                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Layout: 60% Chat │ 40% Sidebar (Data/Image/Debug)         │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌──────────────────┐
│ SectionManager│    │  SafetyScorer    │
│ - expand()    │    │ - score_policy() │
│ - collapse()  │    │ - geocode()      │
│ - maximize()  │    │ - risk_level()   │
└───────────────┘    └─────────┬────────┘
                               │
                               ▼
                     ┌─────────────────┐
                     │  IDataBackend   │ (Strategy Pattern)
                     └────────┬────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        ┌──────────────┐          ┌────────────────────┐
        │  CSVBackend  │          │ VectorStoreBackend │
        │  (Phase 1)   │          │   (Phase 2)        │
        └──────┬───────┘          └─────────┬──────────┘
               │                            │
               ▼                            ▼
    ┌──────────────────┐         ┌──────────────────┐
    │ superfund_       │         │  ChromaDB        │
    │ sites.csv        │         │  Embeddings      │
    └──────────────────┘         └──────────────────┘
               │
               └──────────┐
                          ▼
                  ┌────────────────┐
                  │ ISpecification │ (Specification Pattern)
                  └───────┬────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                  ▼
┌────────────────┐ ┌────────────┐ ┌──────────────┐
│ Geospatial     │ │  Status    │ │   State      │
│ Specification  │ │  Spec      │ │   Spec       │
│ (lat/lon/rad)  │ │            │ │              │
└────────────────┘ └────────────┘ └──────────────┘
```

## Data Flow

### User Query → Safety Score

```
1. User Input
   "Check 123 Main St, Brooklyn, NY"
          ↓
2. SafetyScorer.score_policy()
          ↓
3. Geocode address → (lat, lon)
          ↓
4. Create Specification
   GeospatialSpecification(lat, lon, 50mi)
   .and_spec(UnremediatedSpecification())
          ↓
5. Query Backend
   backend.query(specification)
          ↓
6. Filter CSV Data
   - Calculate distances
   - Filter by status
          ↓
7. Calculate Score
   100 - (site_count × 25)
          ↓
8. Return Result
   {score, risk_level, nearby_sites}
          ↓
9. Display in UI
   - Chat: Formatted report
   - Data Grid: Site details
   - Map: Visual representation
```

## Pattern Implementation

### Strategy Pattern: Backend Swapping

```python
# Interface
class IDataBackend:
    def load_data() → DataFrame
    def query(specification) → DataFrame
    def get_all_sites() → DataFrame

# Implementations
CSVBackend          # Phase 1: Simple file-based
VectorStoreBackend  # Phase 2: Semantic search

# Usage
backend = BackendFactory.create_backend("csv")
results = backend.query(spec)

# Later: Switch to vector store
backend = BackendFactory.create_backend("vector_store")
# Same interface, different implementation!
```

### Specification Pattern: Composable Queries

```python
# Simple specifications
geospatial = GeospatialSpecification(lat, lon, 50)
unremediated = UnremediatedSpecification()
ny_state = StateSpecification("NY")

# Compose with AND/OR
spec = geospatial.and_spec(unremediated)

# Complex query
spec = (
    GeospatialSpecification(lat, lon, 50)
    .and_spec(UnremediatedSpecification())
    .or_spec(StateSpecification("NY"))
)

# Apply to data
results = backend.query(spec)
```

## Component Responsibilities

### app.py (UI Layer)
- Streamlit page configuration
- 60/40 column layout
- Section rendering (chat, data grid, map, debug)
- User input handling
- Display formatting

### SectionManager (UI State)
- Session state management
- Expand/collapse/maximize logic
- Programmatic section activation
- Highlight control
- Button rendering

### SafetyScorer (Business Logic)
- Geocoding addresses
- Proximity calculations
- Score computation (100 - sites × 25)
- Risk level determination
- Batch processing

### IDataBackend (Data Access)
- Abstract data source
- CSV file reading (Phase 1)
- Vector store queries (Phase 2)
- Consistent interface for swapping

### ISpecification (Query Logic)
- Composable filters
- Geospatial queries (distance)
- Status filters (unremediated)
- State/contaminant filters
- Boolean composition (AND/OR/NOT)

### settings.py (Configuration)
- Environment variables
- Default values
- Path management
- Validation

## File Dependencies

```
app.py
├── config.settings
├── src.section_manager
├── src.safety_scorer
│   ├── src.specifications
│   │   └── config.settings
│   ├── src.strategy
│   │   └── config.settings
│   └── config.settings
└── src.strategy
    └── config.settings
```

## Session State Structure

```python
st.session_state = {
    'chat_history': [
        {'role': 'user', 'content': '...'},
        {'role': 'assistant', 'content': '...'}
    ],
    'current_score_result': {
        'score': 75,
        'risk_level': 'LOW',
        'nearby_sites': DataFrame(...),
        'site_count': 1,
        'location': (40.6753, -73.9985),
        'radius_miles': 50
    },
    'section_states': {
        'chat': 'expanded',
        'data_grid': 'expanded',
        'image': 'collapsed',
        'debug': 'collapsed'
    },
    'highlighted_section': 'data_grid'
}
```

## Development Phases

### Phase 1: MVP (Current) ✅
- CSV backend only
- Basic safety scoring
- Chat + data grid UI
- Manual section control

### Phase 2: Enhanced (Next)
- Vector store backend
- LangChain integration
- RAG report generation
- Interactive maps (Folium)
- Auto-section activation

### Phase 3: Advanced (Future)
- Multi-model LLM support
- Real-time EPA data sync
- Advanced analytics dashboard
- Batch policy processing
- Export/reporting features

## Testing Strategy

### Unit Tests
- `test_strategy.py`: Backend implementations
- `test_specifications.py`: Query composition
- `test_safety_scorer.py`: Score calculations

### Integration Tests
- End-to-end score calculation
- Backend switching
- Specification composition

### System Test
- `test_system.py`: Full system validation
- All components working together
- Data loading and querying

## Performance Considerations

### Current (CSV Backend)
- **Load time**: < 1 second (14 sites)
- **Query time**: < 100ms (in-memory filtering)
- **Geocoding**: 1-3 seconds per address
- **Scalability**: Works up to ~10,000 sites

### Future (Vector Store)
- **Load time**: < 1 second (embeddings)
- **Query time**: < 500ms (similarity search)
- **Semantic search**: Enabled
- **Scalability**: 100,000+ sites with indexing

## Security Notes

- ❌ **DO NOT** commit `.env` file to git
- ✅ Store API keys in environment variables
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Validate user inputs before geocoding
- ✅ Rate-limit API calls (Nominatim)

## Deployment Considerations

### Local Development
- Run with `streamlit run app.py`
- Use `.env` for configuration
- CSV backend for testing

### Production (Future)
- Deploy to Streamlit Cloud / Heroku / AWS
- Use environment variables for secrets
- Switch to vector store backend
- Add authentication/authorization
- Implement caching (st.cache_data)
- Monitor API usage and costs
