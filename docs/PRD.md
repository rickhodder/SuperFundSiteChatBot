# Product Requirements Document (PRD)
## SuperFund Site & Insurance Policy Safety Checker ChatBot

**Version**: 1.0  
**Date**: December 14, 2025  
**Status**: Draft - Ready for Development  
**Author**: Development Team  

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Product Vision & Goals](#2-product-vision--goals)
3. [Core Features & Requirements](#3-core-features--requirements)
4. [GUI Layout & Design](#4-gui-layout--design)
5. [Safety Scoring Algorithm](#5-safety-scoring-algorithm)
6. [Data Architecture](#6-data-architecture)
7. [Technical Requirements](#7-technical-requirements)
8. [User Workflows](#8-user-workflows)
9. [Development Phases](#9-development-phases)
10. [Success Criteria](#10-success-criteria)

---

## 1. Executive Summary

### 1.1 Problem Statement

Insurance underwriters and risk analysts need to evaluate the environmental safety of property addresses based on proximity to EPA SuperFund contaminated sites. Current challenges include:

- **Manual research**: Looking up SuperFund sites is time-consuming
- **No risk quantification**: Difficult to assign numeric risk scores
- **Poor data presentation**: Chatbots display tabular data poorly
- **Lack of visualization**: Hard to understand spatial relationships
- **No batch processing**: Can't evaluate multiple policies at once

### 1.2 Solution

A Streamlit-based intelligent chatbot that:

✅ **Evaluates address safety** based on proximity to unremediated SuperFund sites  
✅ **Assigns risk scores** using a standardized algorithm (starts at 100%, -25% per site, minimum 0%)  
✅ **Generates RAG summaries** combining scoring results with site details  
✅ **Displays data intelligently** in dedicated grid vs. chat window  
✅ **Visualizes locations** on interactive maps  
✅ **Processes batches** of policies efficiently  

### 1.3 Target Users

- **Insurance Underwriters**: Evaluate policy risk
- **Risk Analysts**: Portfolio analysis
- **Real Estate Professionals**: Due diligence
- **Environmental Consultants**: Site assessments
- **Compliance Officers**: Regulatory requirements

### 1.4 Key Differentiators

| Traditional Approach | SuperFund ChatBot |
|---------------------|-------------------|
| Manual SuperFund lookup | Automated proximity detection |
| Subjective risk assessment | Standardized scoring algorithm (0-100%) |
| Text-only results | Interactive grid + map visualization |
| Single address at a time | Batch processing support |
| No documentation | RAG-generated summary reports |

---

## 2. Product Vision & Goals

### 2.1 Vision Statement

> **"Transform environmental risk assessment from hours of research into seconds of intelligent analysis"**

### 2.2 Product Goals

**Primary Goals**:
1. **Automate** SuperFund proximity detection within 50 miles
2. **Standardize** risk scoring across all addresses
3. **Visualize** spatial relationships between properties and contamination sites
4. **Generate** comprehensive summary reports using RAG

**Secondary Goals**:
5. Support both insurance policies and standalone address evaluation
6. Enable batch processing for portfolio analysis
7. Provide extensible architecture (CSV → Vector DB migration path)
8. Maintain development transparency with debug logging

### 2.3 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Processing Speed** | <5 sec per address | Time from query to result |
| **Accuracy** | >95% geocoding success | Valid coordinates found |
| **User Satisfaction** | >4.5/5 rating | Post-session survey |
| **Batch Efficiency** | 10 addresses in <30 sec | Total processing time |
| **RAG Quality** | >4/5 coherence rating | Manual review |
| **Cost per Query** | <$0.10 | API costs |

---

## 3. Core Features & Requirements

### 3.1 Address Safety Scoring

#### **Feature: Proximity-Based Risk Assessment**

**Description**: Calculate a safety score for any address based on unremediated SuperFund sites within 50 miles.

**Scoring Algorithm**:
```
Initial Score: 100%

For each unremediated SuperFund site within 50 miles:
    Score = Score - 25%

Minimum Score: 0% (cannot go below zero)

Examples:
- 0 sites within 50 miles → 100% (SAFE)
- 1 site within 50 miles → 75% (LOW RISK)
- 2 sites within 50 miles → 50% (MEDIUM RISK)
- 3 sites within 50 miles → 25% (HIGH RISK)
- 4+ sites within 50 miles → 0% (CRITICAL RISK)
```

**Risk Level Classification**:
| Score Range | Risk Level | Color | Icon |
|-------------|------------|-------|------|
| 100% | SAFE | 🟢 Green | ✓ |
| 75% | LOW RISK | 🟡 Yellow | ⚠ |
| 50% | MEDIUM RISK | 🟠 Orange | ⚠⚠ |
| 25% | HIGH RISK | 🔴 Red | ⚠⚠⚠ |
| 0% | CRITICAL RISK | 🔴 Dark Red | ❌ |

**Requirements**:
- FR-1.1: Calculate score based on UNREMEDIATED sites only
- FR-1.2: Consider all sites within 50-mile radius
- FR-1.3: Score cannot drop below 0%
- FR-1.4: Return list of all sites found within radius
- FR-1.5: Include distance to each site in results
- FR-1.6: Support custom radius (future: allow user to override 50 miles)

**Acceptance Criteria**:
- ✅ Given address with 0 unremediated sites → Score = 100%
- ✅ Given address with 1 unremediated site at 10 miles → Score = 75%
- ✅ Given address with 4 unremediated sites → Score = 0%
- ✅ Remediated sites are excluded from scoring
- ✅ All sites within radius are listed regardless of score

---

### 3.2 RAG-Generated Summary Reports

#### **Feature: Intelligent Document Summarization**

**Description**: Generate comprehensive summary documents combining:
- Address safety score
- List of nearby SuperFund sites
- Site details (contaminants, status, cleanup progress)
- Risk assessment narrative
- Recommendations

**RAG Components**:
1. **Retrieval**: Pull relevant SuperFund site data from vector store
2. **Augmentation**: Combine with scoring results
3. **Generation**: LLM creates human-readable summary

**Report Structure**:
```markdown
# Environmental Risk Assessment Report
**Address**: 123 Main Street, San Diego, CA 92101
**Assessment Date**: December 14, 2025
**Safety Score**: 50% (MEDIUM RISK)

## Executive Summary
This property is located within 50 miles of 2 unremediated EPA SuperFund sites, 
resulting in a medium risk classification...

## Nearby SuperFund Sites

### 1. Operating Industries Inc Landfill
- **Distance**: 2.3 miles
- **EPA ID**: CAD980498612
- **Status**: Final NPL, Cleanup Ongoing
- **Primary Contaminants**: VOCs, Heavy Metals, PCBs
- **Health Concerns**: Groundwater contamination, soil pollution

### 2. San Gabriel Valley Site
- **Distance**: 12.7 miles  
- **EPA ID**: CAD090631123
- **Status**: Final NPL, Long-term Monitoring
- **Primary Contaminants**: Dioxins, Pesticides

## Risk Analysis
The proximity of Operating Industries Inc (2.3 miles) poses a potential concern 
due to ongoing cleanup operations and documented groundwater contamination...

## Recommendations
- Conduct Phase I Environmental Site Assessment
- Review soil and water quality reports
- Consider environmental liability insurance
- Monitor EPA cleanup progress updates
```

**Requirements**:
- FR-2.1: Generate summary for each address evaluation
- FR-2.2: Include all scoring inputs and outputs
- FR-2.3: Provide detailed site information from vector store
- FR-2.4: Format as readable markdown document
- FR-2.5: Export as text, PDF, or display in chat
- FR-2.6: Cite sources (EPA database, vector store docs)

**Acceptance Criteria**:
- ✅ Summary includes safety score and risk level
- ✅ All nearby sites listed with key details
- ✅ Narrative explains scoring rationale
- ✅ Recommendations are actionable
- ✅ Generated in <3 seconds after scoring

---

### 3.3 Insurance Policy Integration

#### **Feature: Policy-Level Risk Assessment**

**Description**: Evaluate insurance policies by assessing the environmental risk of the insured property address.

**Policy Data Fields**:
- Policy ID (unique identifier)
- Property Address (full street address)
- City, State, ZIP
- Policy Type (Residential, Commercial, Industrial)
- Coverage Amount
- Effective Date
- (Optional) Latitude, Longitude

**Workflows**:
1. **Single Policy Evaluation**:
   - User queries: "Check policy P-12345"
   - System retrieves policy address
   - Performs safety scoring
   - Displays result in grid + map

2. **Batch Policy Evaluation**:
   - User uploads CSV with multiple policies
   - System processes all addresses in parallel
   - Generates risk report for entire portfolio
   - Highlights high-risk policies

3. **Grid-Based Actions**:
   - Display policies in data grid
   - "Evaluate" button per row
   - Batch select and evaluate multiple rows
   - Sort by risk level after evaluation

**Requirements**:
- FR-3.1: Load policy data from CSV upload
- FR-3.2: Validate required fields (Policy ID, Address)
- FR-3.3: Support batch evaluation (up to 100 policies)
- FR-3.4: Add risk score column to policy data
- FR-3.5: Flag high-risk policies (score ≤25%)
- FR-3.6: Export evaluated policies with scores

---

### 3.4 Data Query Patterns (Strategy & Specification)

#### **Feature: Flexible Data Backend**

**Description**: Support multiple data backends (CSV, Vector DB) without changing query interface.

**Strategy Pattern Implementation**:

```python
# Abstract interface
class DataStrategy(ABC):
    @abstractmethod
    def query(self, specification: Specification) -> List[Dict]:
        pass

# CSV Implementation
class CSVDataStrategy(DataStrategy):
    def query(self, specification: Specification) -> List[Dict]:
        # Load CSV, apply filters
        df = pd.read_csv(self.file_path)
        return specification.apply(df)

# Vector Store Implementation  
class VectorStoreStrategy(DataStrategy):
    def query(self, specification: Specification) -> List[Dict]:
        # Query vector DB
        results = self.vector_store.similarity_search(specification.to_query())
        return specification.filter(results)
```

**Specification Pattern Implementation**:

```python
class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, item: Dict) -> bool:
        pass
    
    def and_(self, other: 'Specification') -> 'Specification':
        return AndSpecification(self, other)
    
    def or_(self, other: 'Specification') -> 'Specification':
        return OrSpecification(self, other)

# Example specifications
class StateSpecification(Specification):
    def __init__(self, state: str):
        self.state = state
    
    def is_satisfied_by(self, item: Dict) -> bool:
        return item.get('State') == self.state

class ProximitySpecification(Specification):
    def __init__(self, lat: float, lon: float, radius_miles: float):
        self.center = (lat, lon)
        self.radius = radius_miles
    
    def is_satisfied_by(self, item: Dict) -> bool:
        site_coords = (item['latitude'], item['longitude'])
        distance = geodesic(self.center, site_coords).miles
        return distance <= self.radius
```

**Vector Store Geospatial Query**:

**Question**: Can vector stores query by lat/long within radius?

**Answer**: Yes, with appropriate setup:

**Option A: Metadata Filtering (Chroma, Pinecone)**
```python
# Store lat/long in metadata
vector_store.add_documents(
    documents=docs,
    metadatas=[
        {"latitude": 34.05, "longitude": -118.24, ...}
    ]
)

# Query with distance filter (calculated in application layer)
results = vector_store.similarity_search(
    query_text,
    k=100,  # Over-fetch
    filter={"state": "CA"}  # Pre-filter
)

# Post-filter by distance
filtered = [
    r for r in results 
    if geodesic((user_lat, user_lon), (r.metadata['latitude'], r.metadata['longitude'])).miles <= 50
]
```

**Option B: Dedicated Geospatial Index (Elasticsearch, PostgreSQL+PostGIS)**
```python
# Native geospatial query
results = geo_index.query_within_radius(
    center=(user_lat, user_lon),
    radius_miles=50,
    filters={"status": "unremediated"}
)
```

**Requirements**:
- FR-4.1: Implement Strategy pattern for data access
- FR-4.2: Implement Specification pattern for queries
- FR-4.3: Support CSV backend (Phase 1)
- FR-4.4: Support Vector DB backend (Phase 2)
- FR-4.5: Same query interface regardless of backend
- FR-4.6: Geospatial queries supported in both backends

**Acceptance Criteria**:
- ✅ Can swap CSV ↔ Vector DB without changing query code
- ✅ Specification objects work with both backends
- ✅ Proximity queries return identical results
- ✅ Performance acceptable for both backends

---

## 4. GUI Layout & Design

### 4.1 Layout Structure (60/40 Split)

**Overall Layout**:
```
┌──────────────────────┬──────────┐
│                      │  Data    │
│  Chat (60%)          │  [Grid]  │
│  [Messages]          ├──────────┤
│  [Input]             │  Image   │
│                      │  [Map]   │
│                      ├──────────┤
│                      │  Debug   │
└──────────────────────┴──────────┘
```

**Rationale**:
- ✅ **Chat-first UX**: Natural language is primary interface
- ✅ **Context always visible**: No tab switching required
- ✅ **Data not buried**: Grid/map visible alongside chat
- ✅ **Flexible space allocation**: Sections expand/collapse as needed
- ✅ **Solve chatbot data problem**: Tabular data in dedicated grid, not chat scroll

### 4.2 Section Specifications

#### **Section 1: Chat (💬) - Left Column, 60% width**

**Purpose**: Primary interaction via natural language

**Components**:
- **Message History**: Scrollable conversation thread
  - User messages (right-aligned, blue)
  - Assistant messages (left-aligned, gray)
  - Timestamps
  - Source citations (expandable)
  
- **Chat Input**: Fixed at bottom
  - Text box (multi-line support)
  - Send button
  - Suggested queries

- **Features**:
  - Streaming responses (word-by-word)
  - Copy message
  - Regenerate response
  - Export conversation

**Default State**: Expanded, full height

**Header Controls**:
- Title: "💬 Conversation"
- Collapse button: ▼ / ▶
- Maximize button: ⛶ / ⊡

---

#### **Section 2: Data Grid (📊) - Right Column, Top**

**Purpose**: Display structured data (policies, SuperFund sites)

**Components**:
- **AG Grid / Streamlit-AgGrid**:
  - Sortable columns (click header)
  - Filterable columns (dropdown per column)
  - Row selection (checkboxes)
  - Pagination (25/50/100 rows per page)
  
- **Action Buttons**:
  - Per-row: "Evaluate Address" button
  - Batch: "Evaluate Selected" button
  - Export: "Download CSV" button

- **Display Modes**:
  - Policy view: Policy ID, Address, City, State, Score, Risk Level
  - SuperFund view: Site Name, EPA ID, Distance, Status, Contaminants

**Default State**: Collapsed until data query

**Default Height**: 300px (33% of right column)

**Header Controls**:
- Title: "📊 Data Grid"
- Badge: Row count (e.g., "47 rows")
- Collapse button: ▼ / ▶
- Maximize button: ⛶ / ⊡

**Interaction Pattern**:
```
User: "Show me all policies in California"

→ Chat Response: "Found 47 policies. See Data Grid →"
→ Data Grid: Auto-expands, pulse animation
→ Grid Content: Displays 47 policies with columns
```

---

#### **Section 3: Image/Map (🗺️) - Right Column, Middle**

**Purpose**: Visual display (maps, charts, images)

**Content Types**:
1. **Interactive Maps** (Folium/Plotly):
   - Policy address marker (📍 blue)
   - SuperFund site markers (⚠️ color-coded by distance)
   - Radius circle (50 miles)
   - Popups with site details
   - Zoom/pan controls

2. **Charts**:
   - Risk distribution histogram
   - Distance scatter plots
   - Contamination type bar charts

3. **Static Images**:
   - Property photos
   - Site diagrams
   - Aerial imagery

**Default State**: Collapsed until visual query

**Default Height**: 300px (33% of right column)

**Header Controls**:
- Title: "🗺️ Visual Display"
- Badge: "Map loaded" or "Chart: Risk Distribution"
- Collapse button: ▼ / ▶
- Maximize button: ⛶ / ⊡

**Map Legend**:
```
📍 Policy Address
⚠️ SuperFund Site (0-5 mi) - Red
⚠️ SuperFund Site (5-20 mi) - Orange  
⚠️ SuperFund Site (20-50 mi) - Gray
⭕ 50-mile radius
```

---

#### **Section 4: Debug (🐛) - Right Column, Bottom**

**Purpose**: Development logging and troubleshooting

**Content**:
- Real-time log stream
- Log levels: INFO, DEBUG, WARNING, ERROR
- Timestamps
- Color-coded by severity

**Sample Log Output**:
```
[2025-12-14 10:23:15] INFO: User query received: "Check policy P-12345"
[2025-12-14 10:23:16] DEBUG: Query classified as POLICY_EVALUATION
[2025-12-14 10:23:16] DEBUG: Retrieved policy address: 123 Main St, SD
[2025-12-14 10:23:17] INFO: Geocoding successful: (32.7157, -117.1611)
[2025-12-14 10:23:18] DEBUG: Found 2 unremediated sites within 50 miles
[2025-12-14 10:23:18] INFO: Safety score calculated: 50%
[2025-12-14 10:23:19] DEBUG: Generating RAG summary (450 tokens)
[2025-12-14 10:23:21] INFO: Response complete (4.2s)
```

**Features**:
- Log filtering (by level)
- Search logs
- Clear logs
- Export logs
- Performance metrics

**Visibility**: 
- Development: Visible but collapsed by default
- Production: Hidden (unless `DEBUG_MODE=true` in .env)

**Default State**: Collapsed

**Default Height**: 200px (33% of right column)

**Header Controls**:
- Title: "🐛 Debug Logs"
- Badge: Entry count (e.g., "128 entries")
- Collapse button: ▼ / ▶
- Maximize button: ⛶ / ⊡

---

### 4.3 Section Control Behaviors

#### **Expand/Collapse**

**Collapsed State**:
- Shows header only (50px height)
- Content hidden
- Icon: ▶ (right arrow)

**Expanded State**:
- Shows header + content
- Content scrollable within default height
- Icon: ▼ (down arrow)

**Keyboard Shortcut**: Alt + [1-4]

---

#### **Maximize/Restore**

**Maximized State**:
- Section fills entire screen
- All other sections hidden
- Close button (⊡) in header
- ESC key to restore

**Normal State**:
- Section at default size within column
- All sections visible (if expanded)
- Icon: ⛶ (maximize)

**Keyboard Shortcut**: Ctrl + [1-4]

---

#### **Programmatic Activation**

The chatbot automatically expands/highlights sections based on query type:

| Query Type | Action | Example |
|------------|--------|---------|
| Policy list | Expand Data Grid | "Show policies in CA" |
| Address safety | Expand Data + Image | "Check 123 Main St" |
| Location visual | Expand Image | "Show map of site" |
| General Q&A | Keep Chat focused | "What is a SuperFund site?" |
| Error | Expand Debug (dev) | API failure |

**Visual Feedback**:
- Pulse animation (2 seconds)
- Chat reference link: "See Data Grid →"
- Badge sparkle icon: ✨

---

## 5. Safety Scoring Algorithm

### 5.1 Detailed Specification

**Inputs**:
- `address`: Full street address (string)
- `radius_miles`: Search radius (default: 50)
- `superfund_data`: DataFrame of all SuperFund sites

**Processing Steps**:

1. **Geocode Address**:
   ```python
   coords = geocode_address(address)
   # Returns: (latitude, longitude) or None if failed
   ```

2. **Find Sites Within Radius**:
   ```python
   nearby_sites = []
   for site in superfund_data:
       distance = calculate_distance(coords, site.coords)
       if distance <= radius_miles:
           nearby_sites.append({
               'site': site,
               'distance': distance
           })
   ```

3. **Filter by Remediation Status**:
   ```python
   unremediated_sites = [
       s for s in nearby_sites 
       if s['site']['status'] in ['Active', 'Ongoing Cleanup', 'Final NPL']
       # Exclude: 'Cleanup Complete', 'Deleted from NPL'
   ]
   ```

4. **Calculate Score**:
   ```python
   score = 100.0  # Start at 100%
   
   for site in unremediated_sites:
       score -= 25.0
   
   score = max(score, 0.0)  # Cannot go below 0%
   ```

5. **Determine Risk Level**:
   ```python
   if score == 100:
       risk_level = "SAFE"
   elif score == 75:
       risk_level = "LOW RISK"
   elif score == 50:
       risk_level = "MEDIUM RISK"
   elif score == 25:
       risk_level = "HIGH RISK"
   else:  # score == 0
       risk_level = "CRITICAL RISK"
   ```

**Outputs**:
```python
{
    "address": "123 Main Street, San Diego CA 92101",
    "coordinates": (32.7157, -117.1611),
    "safety_score": 50.0,
    "risk_level": "MEDIUM RISK",
    "sites_found": 2,
    "unremediated_sites": [
        {
            "name": "Operating Industries Inc",
            "epa_id": "CAD980498612",
            "distance_miles": 2.3,
            "status": "Final NPL",
            "contaminants": ["VOCs", "Heavy Metals", "PCBs"]
        },
        {
            "name": "San Gabriel Valley",
            "epa_id": "CAD090631123",
            "distance_miles": 12.7,
            "status": "Ongoing Cleanup",
            "contaminants": ["Dioxins", "Pesticides"]
        }
    ]
}
```

### 5.2 Edge Cases

**Case 1: Geocoding Failure**
```
Address: "123 Fake Street, Nowhere CA"
Result: Error message, score = N/A
Action: Display in chat, don't populate grid/map
```

**Case 2: No Sites Found**
```
Address: "123 Rural Road, Montana"
Sites within 50 miles: 0
Score: 100% (SAFE)
Action: Display success message, green indicator
```

**Case 3: All Sites Remediated**
```
Address: "456 Clean Street, CA"
Sites within 50 miles: 3 (all remediated)
Unremediated: 0
Score: 100% (SAFE)
Note: Show message "3 remediated sites nearby"
```

**Case 4: Maximum Risk**
```
Address: "789 Industrial Zone, NJ"
Sites within 50 miles: 8 (6 unremediated)
Score: 0% (CRITICAL RISK)
Note: Score stops at 0%, but list all 6 sites
```

---

## 6. Data Architecture

### 6.1 Data Sources

#### **SuperFund Sites Database**

**Source**: EPA CERCLIS Public Database
- URL: https://cumulis.epa.gov/supercpad/cursites/srchsites.cfm
- Format: CSV export
- Size: ~1,741 sites (as of 2024)
- Update Frequency: Quarterly

**Required Fields**:
```csv
EPA_ID,Site_Name,Address,City,State,ZIP,Latitude,Longitude,NPL_Status,Status,Contaminants,Cleanup_Status
CAD980498612,Operating Industries Inc,5950 Azusa Canyon Rd,Irwindale,CA,91706,34.1395,-117.9539,Final NPL,Active,"VOCs, Heavy Metals, PCBs",Ongoing
```

**Status Values for Filtering**:
- **Unremediated** (count toward score):
  - "Final NPL"
  - "Proposed NPL"
  - "Active"
  - "Ongoing Cleanup"
  - "Long-term Monitoring"
  
- **Remediated** (exclude from score):
  - "Cleanup Complete"
  - "Deleted from NPL"
  - "No Further Action"

---

#### **Insurance Policy Data**

**Source**: User upload (CSV)

**Required Fields**:
```csv
Policy_ID,Property_Address,City,State,ZIP
P-12345,123 Main Street,San Diego,CA,92101
P-12346,456 Oak Avenue,Los Angeles,CA,90015
```

**Optional Fields**:
```csv
Policy_Type,Coverage_Amount,Effective_Date,Latitude,Longitude
Commercial,1000000,2024-01-15,32.7157,-117.1611
Residential,500000,2024-02-20,34.0522,-118.2437
```

**Validation Rules**:
- Policy_ID must be unique
- Property_Address cannot be blank
- State must be valid 2-letter code
- ZIP must be 5 digits
- Coverage_Amount must be numeric (if present)

---

### 6.2 Backend Strategy Architecture

#### **Phase 1: CSV Backend**

**Implementation**:
```python
class CSVDataStrategy(DataStrategy):
    def __init__(self, file_path: str):
        self.df = pd.read_csv(file_path)
    
    def query(self, spec: Specification) -> List[Dict]:
        # Apply specification filters
        filtered_df = self.df[self.df.apply(spec.is_satisfied_by, axis=1)]
        return filtered_df.to_dict('records')
    
    def query_by_proximity(
        self, 
        lat: float, 
        lon: float, 
        radius_miles: float
    ) -> List[Dict]:
        # Calculate distances for all rows
        self.df['distance'] = self.df.apply(
            lambda row: geodesic(
                (lat, lon), 
                (row['Latitude'], row['Longitude'])
            ).miles,
            axis=1
        )
        
        # Filter by radius
        nearby = self.df[self.df['distance'] <= radius_miles]
        return nearby.to_dict('records')
```

**Pros**:
- Simple to implement
- No external dependencies
- Easy to debug
- Works offline

**Cons**:
- Slower for large datasets
- No semantic search
- Manual distance calculations

---

#### **Phase 2: Vector Store Backend**

**Implementation**:
```python
class VectorStoreStrategy(DataStrategy):
    def __init__(self, collection_name: str):
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=OpenAIEmbeddings()
        )
    
    def query(self, spec: Specification) -> List[Dict]:
        # Semantic search
        query_text = spec.to_natural_language()
        results = self.vector_store.similarity_search(
            query_text,
            k=100,
            filter=spec.to_metadata_filter()
        )
        
        # Post-filter with specification
        return [
            r.metadata for r in results 
            if spec.is_satisfied_by(r.metadata)
        ]
    
    def query_by_proximity(
        self, 
        lat: float, 
        lon: float, 
        radius_miles: float
    ) -> List[Dict]:
        # Option 1: Retrieve all, filter in memory
        all_sites = self.vector_store.get()
        nearby = []
        
        for site in all_sites:
            metadata = site['metadata']
            distance = geodesic(
                (lat, lon),
                (metadata['latitude'], metadata['longitude'])
            ).miles
            
            if distance <= radius_miles:
                metadata['distance'] = distance
                nearby.append(metadata)
        
        return nearby
        
        # Option 2 (future): Use dedicated geospatial index
        # results = self.geo_index.within_radius(lat, lon, radius_miles)
```

**Pros**:
- Semantic search capabilities
- Better for unstructured text (RAG)
- Scalable to millions of records
- Embedding-based similarity

**Cons**:
- More complex setup
- External service dependency
- Geospatial queries require workaround

---

#### **Specification Pattern Examples**

```python
# Query by state
spec = StateSpecification("CA")

# Query by proximity
spec = ProximitySpecification(
    lat=34.0522,
    lon=-118.2437,
    radius_miles=50
)

# Query by status
spec = StatusSpecification(["Final NPL", "Active"])

# Combined query: CA AND unremediated AND within 50 miles
spec = (
    StateSpecification("CA")
    .and_(StatusSpecification(["Final NPL", "Active"]))
    .and_(ProximitySpecification(lat, lon, 50))
)

# Execute with either backend
data_strategy = get_current_strategy()  # Returns CSV or Vector
results = data_strategy.query(spec)
```

---

### 6.3 Data Migration Path

**Step 1**: Start with CSV (Phase 1)
```python
data_strategy = CSVDataStrategy("data/superfund_sites.csv")
```

**Step 2**: Prepare for migration
```python
# Create embeddings from CSV
embeddings = create_embeddings_from_csv("data/superfund_sites.csv")

# Populate vector store
vector_store.add_documents(embeddings)
```

**Step 3**: Switch strategy (Phase 2)
```python
data_strategy = VectorStoreStrategy("superfund_collection")
```

**Key**: Application code using `data_strategy.query(spec)` doesn't change!

---

## 7. Technical Requirements

### 7.1 Technology Stack

**Frontend**:
- **Streamlit** 1.28+ (UI framework)
- **streamlit-aggrid** 0.3+ (data grid)
- **Folium** 0.14+ (maps)
- **Plotly** 5.17+ (charts)

**Backend**:
- **Python** 3.9+
- **LangChain** 0.1+ (RAG orchestration)
- **OpenAI API** (LLM: GPT-3.5-turbo or GPT-4)
- **Chroma** 0.4+ or **FAISS** 1.7+ (vector store, Phase 2)

**Data Processing**:
- **Pandas** 2.1+ (data manipulation)
- **GeoPy** 2.4+ (geocoding via Nominatim)
- **Shapely** 2.0+ (geospatial calculations)

**Development**:
- **pytest** (testing)
- **black** (formatting)
- **flake8** (linting)
- **python-dotenv** (environment management)

### 7.2 System Architecture

```
┌────────────────────────────────────────────────┐
│         Streamlit Frontend (app.py)            │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Chat    │ │DataGrid  │ │ Map Display  │  │
│  └──────────┘ └──────────┘ └──────────────┘  │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│        Application Logic Layer (src/)          │
│                                                 │
│  ┌────────────────┐  ┌────────────────────┐   │
│  │ ChatBot        │  │ SafetyScorer       │   │
│  │ (orchestrator) │  │ (scoring logic)    │   │
│  └────────────────┘  └────────────────────┘   │
│                                                 │
│  ┌────────────────┐  ┌────────────────────┐   │
│  │ DataStrategy   │  │ Specification      │   │
│  │ (CSV/Vector)   │  │ (query patterns)   │   │
│  └────────────────┘  └────────────────────┘   │
│                                                 │
│  ┌────────────────┐  ┌────────────────────┐   │
│  │ ProximityCheck │  │ RAGGenerator       │   │
│  │ (geospatial)   │  │ (summaries)        │   │
│  └────────────────┘  └────────────────────┘   │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│           Data & API Layer                     │
│                                                 │
│  ┌──────────────┐  ┌──────────────────────┐   │
│  │ CSV Files    │  │ Vector Store (Phase2)│   │
│  │ - policies   │  │ - Chroma/FAISS       │   │
│  │ - superfund  │  │ - embeddings         │   │
│  └──────────────┘  └──────────────────────┘   │
│                                                 │
│  ┌──────────────┐  ┌──────────────────────┐   │
│  │ LLM API      │  │ Geocoding API        │   │
│  │ (OpenAI)     │  │ (GeoPy/Nominatim)    │   │
│  └──────────────┘  └──────────────────────┘   │
└────────────────────────────────────────────────┘
```

### 7.3 File Structure

```
SuperFundSiteChatBot/
├── app.py                          # Main Streamlit application
├── .env                            # Environment variables (API keys)
├── .gitignore
├── requirements.txt
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── chatbot.py                  # Main orchestrator
│   ├── llm_handler.py              # LLM API wrapper
│   ├── safety_scorer.py            # Scoring algorithm
│   ├── proximity_checker.py        # Geospatial calculations
│   ├── rag_generator.py            # RAG summary generation
│   ├── query_classifier.py         # Intent detection
│   ├── section_manager.py          # GUI section control
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── strategy.py             # Strategy pattern interface
│   │   ├── csv_strategy.py         # CSV backend
│   │   ├── vector_strategy.py      # Vector DB backend (Phase 2)
│   │   └── specification.py        # Specification pattern
│   │
│   └── utils.py
│
├── components/
│   ├── __init__.py
│   ├── chat_interface.py
│   ├── data_grid.py
│   ├── map_display.py
│   ├── debug_panel.py
│   └── section_header.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── raw/
│   │   ├── superfund_sites.csv
│   │   └── policies.csv (user upload)
│   ├── processed/
│   └── embeddings/ (Phase 2)
│
├── tests/
│   ├── __init__.py
│   ├── test_safety_scorer.py
│   ├── test_proximity_checker.py
│   ├── test_specifications.py
│   └── test_strategies.py
│
├── docs/
│   ├── PRD.md (this document)
│   ├── TECHNICAL_SPEC.md
│   ├── API_DOCUMENTATION.md
│   └── USER_GUIDE.md
│
└── notebooks/
    └── data_exploration.ipynb
```

### 7.4 Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| **Single Address Scoring** | <5 seconds | Geocoding + proximity + RAG |
| **Batch (10 addresses)** | <30 seconds | Parallel processing |
| **Batch (100 addresses)** | <5 minutes | Progress bar shown |
| **Data Grid Render (100 rows)** | <1 second | AG Grid optimized |
| **Map Generation** | <3 seconds | Cached per address |
| **RAG Summary** | <3 seconds | 500-1000 tokens |
| **Section Toggle** | <0.1 seconds | Pure UI |
| **CSV Upload** | <2 seconds | 10MB max |

### 7.5 API Cost Estimates

**OpenAI API** (GPT-3.5-turbo):
- Query classification: ~100 tokens → $0.0002
- RAG generation: ~1000 tokens → $0.002
- **Total per evaluation**: ~$0.0025

**Monthly Cost** (1000 evaluations):
- LLM costs: ~$2.50
- Geocoding: Free (Nominatim)
- **Total**: ~$3/month

---

## 8. User Workflows

### 8.1 Workflow: Single Address Evaluation

**User Story**: "As an underwriter, I want to evaluate the environmental risk of a specific address"

**Steps**:

1. **User enters query**:
   ```
   "Check the safety of 123 Main Street, San Diego CA 92101"
   ```

2. **System processes**:
   - Classifies as ADDRESS_SAFETY_CHECK
   - Extracts address: "123 Main Street, San Diego CA 92101"
   - Geocodes → (32.7157, -117.1611)
   - Queries SuperFund sites within 50 miles
   - Finds 2 unremediated sites
   - Calculates score: 100% - 25% - 25% = 50%
   - Generates RAG summary

3. **Chat displays**:
   ```
   🏠 Address Safety Assessment
   
   Address: 123 Main Street, San Diego CA 92101
   Safety Score: 50% (MEDIUM RISK) 🟠
   
   Found 2 unremediated SuperFund sites within 50 miles:
   
   1. Operating Industries Inc (2.3 miles)
      - Status: Final NPL, Ongoing Cleanup
      - Contaminants: VOCs, Heavy Metals, PCBs
   
   2. San Gabriel Valley Site (12.7 miles)
      - Status: Final NPL, Long-term Monitoring
      - Contaminants: Dioxins, Pesticides
   
   See map for visual details →
   📄 View full report
   ```

4. **Image section activates**:
   - Auto-expands with pulse animation
   - Displays map with:
     - 📍 Blue marker at 123 Main St
     - ⚠️ Red marker at Operating Industries (2.3 mi)
     - ⚠️ Orange marker at San Gabriel (12.7 mi)
     - ⭕ 50-mile radius circle

5. **User clicks "View full report"**:
   - Chat displays formatted RAG-generated summary
   - Includes all details, risk analysis, recommendations
   - Export button available (TXT, PDF)

---

### 8.2 Workflow: Policy Batch Evaluation

**User Story**: "As a risk analyst, I want to evaluate 50 policies in my portfolio"

**Steps**:

1. **User uploads CSV**:
   - Clicks "Upload Policies" button
   - Selects `portfolio_california.csv` (50 policies)
   - System validates columns

2. **Chat confirms**:
   ```
   ✅ Loaded 50 policies from California
   
   Summary:
   - Cities: 15
   - Policy Types: 30 Commercial, 20 Residential
   
   💡 Suggested actions:
    • "Evaluate all policies"
    • "Show high-value policies only"
    • "Filter by Los Angeles"
   ```

3. **Data Grid activates**:
   - Auto-expands
   - Displays all 50 policies
   - Columns: Policy_ID, Address, City, Coverage, [Not Evaluated]

4. **User clicks "Select All" → "Evaluate Selected"**:
   - System shows progress: "Evaluating 10/50 policies..."
   - Updates grid in real-time as each completes
   - Adds columns: Safety_Score, Risk_Level, Sites_Found

5. **Chat summarizes**:
   ```
   ✅ Evaluated 50 policies in 2 minutes 14 seconds
   
   Risk Distribution:
   🟢 SAFE (100%): 12 policies
   🟡 LOW RISK (75%): 18 policies
   🟠 MEDIUM RISK (50%): 14 policies
   🔴 HIGH RISK (25%): 4 policies
   ❌ CRITICAL RISK (0%): 2 policies
   
   ⚠️ Attention Required:
   - Policy P-12346: CRITICAL RISK (5 unremediated sites nearby)
   - Policy P-12350: CRITICAL RISK (4 unremediated sites nearby)
   
   See Data Grid for full details →
   ```

6. **Data Grid updates**:
   - Rows color-coded by risk level
   - Sortable by Safety_Score (lowest first)
   - Filterable by Risk_Level

7. **Image section displays**:
   - Heat map of California
   - All 50 policy locations
   - Color intensity = risk level
   - Cluster markers by region

8. **User exports results**:
   - Selects high-risk rows (6 policies)
   - Clicks "Export Selected"
   - Downloads `high_risk_policies_2025-12-14.csv`
   - Includes all columns + evaluation results

---

### 8.3 Workflow: Policy Grid Selection & Action

**User Story**: "I want to evaluate specific policies from the grid"

**Steps**:

1. **User queries**:
   ```
   "Show me all policies in Los Angeles with coverage over $500,000"
   ```

2. **Data Grid displays**:
   - 12 matching policies
   - Columns: Policy_ID, Address, City, Coverage, [Action]

3. **User selects 3 policies** (checkboxes)

4. **User clicks "Evaluate" button** (appears when rows selected)

5. **System processes**:
   - Shows inline progress in grid
   - Each row updates with score as it completes

6. **Results display**:
   ```
   Row 1: P-12345 → 75% (LOW RISK) ✅
   Row 2: P-12348 → 25% (HIGH RISK) ⚠️
   Row 3: P-12352 → 100% (SAFE) ✅
   ```

7. **User clicks map icon** next to P-12348:
   - Image section activates
   - Shows map for that specific policy
   - 3 SuperFund sites visible

---

### 8.4 Workflow: RAG Summary Generation

**User Story**: "I need a formal report for client presentation"

**Steps**:

1. **After evaluation completes**:
   ```
   Chat: "Evaluation complete. Generate formal report?"
   
   User: "Yes, create a detailed report"
   ```

2. **System generates RAG summary**:
   - Retrieves relevant SuperFund site details from vector store
   - Combines with scoring results
   - LLM generates structured narrative

3. **Chat displays formatted report**:
   ```markdown
   # Environmental Risk Assessment Report
   **Property**: 123 Main Street, San Diego CA 92101
   **Assessment Date**: December 14, 2025
   **Safety Score**: 50% (MEDIUM RISK)
   
   ## Executive Summary
   This property is located within 50 miles of 2 unremediated 
   EPA SuperFund sites, resulting in a medium risk classification.
   The closest site (Operating Industries Inc) is 2.3 miles away
   and is currently undergoing active cleanup operations...
   
   ## Detailed Site Analysis
   
   ### 1. Operating Industries Inc Landfill
   **EPA ID**: CAD980498612
   **Distance**: 2.3 miles NW of property
   **Status**: Final NPL, Active Cleanup (Est. completion: 2028)
   **Primary Contaminants**: 
   - Volatile Organic Compounds (VOCs)
   - Heavy Metals (Lead, Arsenic, Chromium)
   - Polychlorinated Biphenyls (PCBs)
   
   **Environmental Concerns**:
   - Soil contamination to depth of 30 feet
   - Groundwater plume extending 1 mile
   - Air quality monitoring ongoing
   
   **Health Risks**:
   - Potential vapor intrusion to buildings
   - Groundwater contamination affects drinking water
   - Long-term exposure risks from heavy metals
   
   ...
   
   ## Risk Mitigation Recommendations
   1. Commission Phase I Environmental Site Assessment
   2. Review EPA cleanup progress quarterly
   3. Consider environmental liability insurance ($250K coverage)
   4. Implement air quality monitoring if industrial use
   5. Restrict groundwater extraction within 2-mile radius
   
   ## Conclusion
   The property presents moderate environmental risk due to 
   proximity to active SuperFund sites. Recommended mitigation 
   measures can reduce exposure. Ongoing monitoring is essential.
   
   ---
   *This report is generated using EPA CERCLIS data as of 
   December 14, 2025. Consult with environmental professionals 
   for site-specific guidance.*
   ```

4. **User actions**:
   - Clicks "Export as PDF"
   - Clicks "Copy to clipboard"
   - Clicks "Email report" (future feature)

---

## 9. Development Phases

### Phase 1: Core Infrastructure (Weeks 1-2)

**Goal**: Basic GUI + CSV data access

**Tasks**:
- [x] Project setup (repo, venv, requirements.txt)
- [ ] Implement 60/40 Streamlit layout
- [ ] Create Section component with expand/collapse/maximize
- [ ] Implement SectionManager class
- [ ] Build Chat interface shell
- [ ] Build Data Grid with AG Grid
- [ ] Build Map Display placeholder
- [ ] Build Debug panel
- [ ] Load SuperFund CSV data
- [ ] Implement CSVDataStrategy
- [ ] Test all section controls

**Deliverables**:
✅ GUI with all 4 sections functional  
✅ CSV data loads and displays in grid  
✅ All controls work (expand/collapse/maximize)

---

### Phase 2: Safety Scoring Logic (Week 3)

**Goal**: Address evaluation works

**Tasks**:
- [ ] Implement SafetyScorer class
- [ ] Integrate GeoPy for geocoding
- [ ] Implement ProximityChecker
- [ ] Calculate distance using geodesic
- [ ] Filter unremediated sites
- [ ] Implement scoring algorithm (100%, -25% per site, min 0%)
- [ ] Add risk level classification
- [ ] Handle edge cases (geocoding failures, no sites found)
- [ ] Write unit tests for scoring logic
- [ ] Test with known addresses

**Deliverables**:
✅ Scoring algorithm works correctly  
✅ Risk levels assigned properly  
✅ All edge cases handled

---

### Phase 3: LLM & RAG Integration (Week 4)

**Goal**: Chat responds with intelligence

**Tasks**:
- [ ] Set up OpenAI API integration
- [ ] Create LLMHandler class
- [ ] Implement query classification
- [ ] Build basic chatbot responses
- [ ] Implement RAG framework with LangChain
- [ ] Create document loaders for SuperFund data
- [ ] Implement summary generation
- [ ] Format RAG output as structured report
- [ ] Add source citations
- [ ] Test RAG quality

**Deliverables**:
✅ Chatbot responds to queries  
✅ RAG summaries generate correctly  
✅ Summaries are coherent and useful

---

### Phase 4: Map Visualization (Week 5)

**Goal**: Visual display of locations

**Tasks**:
- [ ] Integrate Folium for maps
- [ ] Create MapGenerator class
- [ ] Add policy address markers (blue)
- [ ] Add SuperFund site markers (color-coded)
- [ ] Add 50-mile radius circles
- [ ] Implement marker popups
- [ ] Add map legend
- [ ] Connect map to scoring results
- [ ] Implement map export (PNG)
- [ ] Test map performance with many markers

**Deliverables**:
✅ Maps display correctly  
✅ Markers show proper information  
✅ Colors match risk levels

---

### Phase 5: Intelligent Section Control (Week 6)

**Goal**: Sections activate automatically

**Tasks**:
- [ ] Implement QueryClassifier with patterns + LLM
- [ ] Detect query types (POLICY_LIST, ADDRESS_SAFETY, etc.)
- [ ] Implement auto-expand logic in SectionManager
- [ ] Add pulse animations for section activation
- [ ] Add clickable references in chat ("See Data Grid →")
- [ ] Implement badge updates with sparkle
- [ ] Connect classifier to chatbot orchestrator
- [ ] Test all query types
- [ ] Ensure user can override automation

**Deliverables**:
✅ Sections activate based on query type  
✅ Visual cues work properly  
✅ Classification accuracy >85%

---

### Phase 6: Policy Integration & Batch (Week 7)

**Goal**: Policy evaluation works

**Tasks**:
- [ ] Implement policy CSV upload
- [ ] Validate policy data
- [ ] Add "Evaluate" button to grid rows
- [ ] Implement single policy evaluation
- [ ] Implement batch evaluation with progress bar
- [ ] Parallel processing for batch operations
- [ ] Update grid with results in real-time
- [ ] Add risk level filtering/sorting
- [ ] Implement export with evaluation results
- [ ] Test with large policy sets (100+)

**Deliverables**:
✅ Policy evaluation works end-to-end  
✅ Batch processing efficient  
✅ Results display properly in grid

---

### Phase 7: Specification Pattern & Vector DB Prep (Week 8)

**Goal**: Flexible query architecture

**Tasks**:
- [ ] Implement Specification base class
- [ ] Create concrete specifications (State, Proximity, Status)
- [ ] Implement AND/OR composition
- [ ] Refactor CSVDataStrategy to use specifications
- [ ] Write tests for all specifications
- [ ] Prepare for vector DB migration:
  - [ ] Generate embeddings from CSV
  - [ ] Set up Chroma collection
  - [ ] Test embedding quality
- [ ] Implement VectorStoreStrategy (basic)
- [ ] Test strategy swapping

**Deliverables**:
✅ Specification pattern working  
✅ Can swap between CSV and Vector backends  
✅ Vector store ready for Phase 2 full migration

---

### Phase 8: Polish & Deployment (Week 9-10)

**Goal**: Production-ready application

**Tasks**:
- [ ] Comprehensive error handling
- [ ] Loading states for all operations
- [ ] Retry logic for API failures
- [ ] Write user documentation
- [ ] Create README with setup instructions
- [ ] Add unit tests (target >80% coverage)
- [ ] Performance optimization
- [ ] Debug mode environment toggle
- [ ] Security audit (API keys, input validation)
- [ ] Deploy to Streamlit Cloud
- [ ] Set up monitoring

**Deliverables**:
✅ All features working  
✅ No critical bugs  
✅ Documentation complete  
✅ Deployed to production

---

## 10. Success Criteria

### 10.1 Must Have (MVP)

**Core Functionality**:
- ✅ Evaluate address safety with scoring algorithm
- ✅ Calculate score based on unremediated sites (100%, -25% each, min 0%)
- ✅ Display results in chat, grid, and map
- ✅ Generate RAG summary reports
- ✅ All 4 sections (Chat, Data, Image, Debug) functional
- ✅ Expand/collapse/maximize controls work
- ✅ Load policy CSV and evaluate in batch
- ✅ Strategy pattern allows backend switching
- ✅ Specification pattern for flexible queries

**Quality Metrics**:
- Response time <5 seconds for single evaluation
- Batch processing 10 addresses in <30 seconds
- Geocoding success rate >95%
- RAG summary coherence >4/5 rating
- Zero critical bugs

### 10.2 Should Have (Phase 2)

**Enhanced Features**:
- Vector store backend fully operational
- Semantic search for SuperFund sites
- Custom radius configuration (not just 50 miles)
- Multi-criteria sorting in grid
- Advanced filters (by contaminant type, date range)
- PDF export for RAG summaries
- Email report functionality
- Historical trend analysis

**Quality Metrics**:
- User satisfaction >4.5/5
- 70%+ users leverage batch processing
- Average 20+ queries per session

### 10.3 Nice to Have (Future)

**Advanced Features**:
- Real-time EPA data sync via API
- Machine learning risk prediction
- Integration with GIS systems
- Mobile app version
- Multi-user collaboration
- Custom risk weighting (allow users to adjust -25% penalty)
- Contaminant-specific risk scores
- Property value impact estimation
- Insurance premium calculator

---

## 11. Open Questions & Decisions

### Q1: Remediation Status Definitions
**Question**: How do we determine if a site is "unremediated"?

**Decision**: Use EPA status codes:
- **Unremediated** = "Final NPL", "Proposed NPL", "Active", "Ongoing Cleanup"
- **Remediated** = "Cleanup Complete", "Deleted from NPL", "No Further Action"

**Rationale**: Aligns with EPA terminology, clear distinction

---

### Q2: Custom Scoring Algorithm
**Question**: Should users be able to adjust the -25% penalty per site?

**Decision**: Not in MVP, add in Phase 2

**Rationale**: Keep MVP simple; most users will accept standardized scoring

---

### Q3: Distance Weighting
**Question**: Should closer sites count more toward the score? (e.g., site at 2 miles worse than site at 40 miles)

**Current Algorithm**: All sites within 50 miles count equally (-25%)

**Options**:
- A) Keep flat penalty (current)
- B) Distance-weighted: closer = higher penalty
- C) Zone-based: 0-5mi = -50%, 5-20mi = -30%, 20-50mi = -20%

**Decision**: Start with Option A (flat), add distance weighting in Phase 2

**Rationale**: Simpler to explain and implement; can enhance later based on feedback

---

### Q4: Maximum Score Penalty
**Question**: Should score be allowed to go negative, or stop at 0%?

**Decision**: Stop at 0% (as specified)

**Rationale**: Negative scores are confusing; 0% already indicates critical risk

---

### Q5: Batch Size Limit
**Question**: What's the maximum number of policies we can evaluate at once?

**Options**:
- A) 50 policies (safe, ~2-3 minutes)
- B) 100 policies (balanced, ~5 minutes)
- C) 500+ policies (requires background job queue)

**Decision**: 100 policies max in MVP (Option B)

**Rationale**: Handles typical portfolio sizes; larger batches can use background processing in Phase 2

---

### Q6: Vector Store Provider
**Question**: Which vector store should we use?

**Options**:
- A) Chroma (open-source, local, easy setup)
- B) Pinecone (cloud, managed, scalable)
- C) Weaviate (open-source, production-ready)
- D) FAISS (Meta, fast, local)

**Decision**: Chroma for MVP (Option A), migrate to Pinecone for production scale if needed

**Rationale**: Chroma is easiest to set up, works locally, sufficient for Phase 1-2

---

## 12. Appendix

### 12.1 Glossary

- **NPL**: National Priorities List (most serious SuperFund sites)
- **CERCLIS**: Comprehensive Environmental Response, Compensation, and Liability Information System
- **RAG**: Retrieval Augmented Generation (LLM + knowledge base)
- **Unremediated**: Site still contaminated, cleanup not complete
- **Remediated**: Cleanup complete, site safe or removed from NPL
- **VOCs**: Volatile Organic Compounds (common contaminants)
- **PCBs**: Polychlorinated Biphenyls (toxic industrial chemicals)
- **Strategy Pattern**: Design pattern for swappable algorithms
- **Specification Pattern**: Design pattern for composable query criteria

### 12.2 Example Queries

**Address Evaluation**:
1. "Check 123 Main Street, San Diego CA 92101"
2. "Is 456 Oak Avenue safe?"
3. "Evaluate the environmental risk of 789 Elm Road, Fresno CA"

**Policy Queries**:
4. "Show all policies in California"
5. "List high-risk policies"
6. "Which policies need environmental assessment?"

**Batch Operations**:
7. "Evaluate all policies in the grid"
8. "Check all Los Angeles properties"
9. "Generate reports for selected policies"

**Site Queries**:
10. "Show SuperFund sites in Texas"
11. "What contaminants are in site CAD980498612?"
12. "How many unremediated sites are in California?"

**General Knowledge**:
13. "What is a SuperFund site?"
14. "How does EPA cleanup work?"
15. "What are the health risks of PCBs?"

### 12.3 References

- **EPA SuperFund Database**: https://cumulis.epa.gov/supercpad/cursites/srchsites.cfm
- **EPA CERCLIS**: https://www.epa.gov/superfund/superfund-information-systems
- **LangChain Docs**: https://python.langchain.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Chroma Docs**: https://docs.trychroma.com
- **GeoPy Docs**: https://geopy.readthedocs.io

---

**Document Status**: ✅ Ready for Review & Approval

**Next Steps**:
1. Review and approve PRD
2. Create detailed technical specification
3. Set up development environment
4. Begin Phase 1: Core Infrastructure

---

*End of Product Requirements Document*
