# Technical Specification
## SuperFund Site & Insurance Policy Safety Checker ChatBot

**Version**: 1.0  
**Date**: December 14, 2025  
**Based on**: PRD v1.0  
**Status**: Ready for Implementation

---

## Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [Component Specifications](#2-component-specifications)
3. [API Specifications](#3-api-specifications)
4. [Data Models](#4-data-models)
5. [Implementation Details](#5-implementation-details)
6. [Testing Strategy](#6-testing-strategy)
7. [Deployment Guide](#7-deployment-guide)

---

## 1. Architecture Overview

### 1.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│                   Streamlit Frontend (app.py)                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Chat         │  │ Data Grid    │  │ Map Display     │  │
│  │ Interface    │  │ (AG Grid)    │  │ (Folium)        │  │
│  │              │  │              │  │                 │  │
│  │ - Messages   │  │ - Sortable   │  │ - Interactive   │  │
│  │ - Input      │  │ - Filterable │  │ - Markers       │  │
│  │ - Streaming  │  │ - Actions    │  │ - Popups        │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Section Manager (expand/collapse/maximize)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                          │
│                  Business Logic (src/)                       │
│                                                              │
│  ┌────────────────────┐        ┌────────────────────────┐  │
│  │ ChatBot            │        │ SafetyScorer           │  │
│  │ Orchestrator       │───────▶│ - Geocode              │  │
│  │                    │        │ - Find sites           │  │
│  │ - Route queries    │        │ - Calculate score      │  │
│  │ - Manage state     │        │ - Assign risk level    │  │
│  │ - Coordinate UI    │        └────────────────────────┘  │
│  └────────────────────┘                                     │
│           │                                                  │
│           ├──────────────────┬──────────────────┐          │
│           ↓                  ↓                  ↓           │
│  ┌────────────────┐ ┌────────────────┐ ┌─────────────┐   │
│  │ Query          │ │ RAG            │ │ Proximity   │   │
│  │ Classifier     │ │ Generator      │ │ Checker     │   │
│  │                │ │                │ │             │   │
│  │ - Intent       │ │ - Retrieval    │ │ - Geodesic  │   │
│  │ - Entities     │ │ - Augment      │ │ - Filter    │   │
│  │ - Route        │ │ - Generate     │ │ - Distance  │   │
│  └────────────────┘ └────────────────┘ └─────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Data Access Layer (Strategy Pattern)                 │  │
│  │                                                       │  │
│  │  DataStrategy ◄──┬── CSVDataStrategy (Phase 1)       │  │
│  │  (Interface)     └── VectorStoreStrategy (Phase 2)   │  │
│  │                                                       │  │
│  │  Specification ◄──┬── StateSpecification             │  │
│  │  (Interface)      ├── ProximitySpecification         │  │
│  │                   └── StatusSpecification            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│                                                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ CSV Files    │  │ Vector Store     │  │ LLM API      │ │
│  │              │  │ (Phase 2)        │  │              │ │
│  │ - SuperFund  │  │ - Chroma         │  │ - OpenAI     │ │
│  │ - Policies   │  │ - Embeddings     │  │ - GPT-3.5    │ │
│  └──────────────┘  └──────────────────┘  └──────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ External APIs                                         │  │
│  │ - GeoPy/Nominatim (Geocoding)                        │  │
│  │ - EPA CERCLIS (Future: Real-time data)               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack Details

**Frontend Framework**:
```yaml
streamlit: ^1.28.0
  Purpose: Web application framework
  Why: Rapid development, Python-native, built-in state management

streamlit-aggrid: ^0.3.0
  Purpose: Advanced data grid with sorting/filtering
  Why: Best-in-class grid for Streamlit, Excel-like UX

folium: ^0.14.0
  Purpose: Interactive maps
  Why: Python-friendly, Leaflet.js wrapper, good Streamlit integration

plotly: ^5.17.0
  Purpose: Charts and visualizations
  Why: Interactive, professional, wide chart variety
```

**Backend Framework**:
```yaml
langchain: ^0.1.0
  Purpose: LLM orchestration and RAG framework
  Why: Industry standard, excellent abstraction, active development

openai: ^1.6.0
  Purpose: LLM API client
  Why: Best-in-class models, reliable API, good documentation

chromadb: ^0.4.22
  Purpose: Vector database (Phase 2)
  Why: Easy setup, local-first, Python-native

pandas: ^2.1.0
  Purpose: Data manipulation
  Why: Industry standard, rich functionality

geopy: ^2.4.0
  Purpose: Geocoding
  Why: Multiple providers, free tier (Nominatim), simple API
```

---

## 2. Component Specifications

### 2.1 SafetyScorer Class

**Location**: `src/safety_scorer.py`

**Purpose**: Calculate address safety scores based on proximity to unremediated SuperFund sites.

**Class Definition**:
```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import pandas as pd
from geopy.distance import geodesic

@dataclass
class SafetyScore:
    """Result of safety assessment"""
    address: str
    coordinates: Optional[Tuple[float, float]]
    safety_score: float
    risk_level: str
    sites_found: int
    unremediated_sites: List[dict]
    error: Optional[str] = None

class SafetyScorer:
    """Calculate safety scores for addresses"""
    
    SCORE_PENALTY_PER_SITE = 25.0
    INITIAL_SCORE = 100.0
    MIN_SCORE = 0.0
    DEFAULT_RADIUS_MILES = 50
    
    UNREMEDIATED_STATUSES = [
        "Final NPL",
        "Proposed NPL", 
        "Active",
        "Ongoing Cleanup",
        "Long-term Monitoring"
    ]
    
    RISK_LEVELS = {
        100.0: "SAFE",
        75.0: "LOW RISK",
        50.0: "MEDIUM RISK",
        25.0: "HIGH RISK",
        0.0: "CRITICAL RISK"
    }
    
    def __init__(self, proximity_checker, superfund_data: pd.DataFrame):
        """
        Initialize scorer
        
        Args:
            proximity_checker: ProximityChecker instance
            superfund_data: DataFrame with SuperFund site data
        """
        self.proximity_checker = proximity_checker
        self.superfund_data = superfund_data
    
    def evaluate_address(
        self, 
        address: str,
        radius_miles: float = DEFAULT_RADIUS_MILES
    ) -> SafetyScore:
        """
        Evaluate safety of an address
        
        Args:
            address: Full street address
            radius_miles: Search radius (default: 50)
            
        Returns:
            SafetyScore object with results
        """
        # Step 1: Geocode address
        coords = self.proximity_checker.geocode_address(address)
        
        if coords is None:
            return SafetyScore(
                address=address,
                coordinates=None,
                safety_score=0.0,
                risk_level="UNKNOWN",
                sites_found=0,
                unremediated_sites=[],
                error="Geocoding failed - invalid address"
            )
        
        # Step 2: Find nearby sites
        nearby_sites = self.proximity_checker.find_sites_within_radius(
            coords[0], coords[1], radius_miles
        )
        
        # Step 3: Filter unremediated sites
        unremediated = [
            site for site in nearby_sites
            if site.get('Status') in self.UNREMEDIATED_STATUSES
        ]
        
        # Step 4: Calculate score
        score = self.INITIAL_SCORE
        for _ in unremediated:
            score -= self.SCORE_PENALTY_PER_SITE
        
        score = max(score, self.MIN_SCORE)
        
        # Step 5: Determine risk level
        risk_level = self.RISK_LEVELS.get(score, "UNKNOWN")
        
        return SafetyScore(
            address=address,
            coordinates=coords,
            safety_score=score,
            risk_level=risk_level,
            sites_found=len(nearby_sites),
            unremediated_sites=unremediated
        )
    
    def evaluate_batch(
        self,
        addresses: List[str],
        radius_miles: float = DEFAULT_RADIUS_MILES
    ) -> List[SafetyScore]:
        """
        Evaluate multiple addresses
        
        Args:
            addresses: List of addresses to evaluate
            radius_miles: Search radius
            
        Returns:
            List of SafetyScore objects
        """
        results = []
        for address in addresses:
            score = self.evaluate_address(address, radius_miles)
            results.append(score)
        
        return results
```

**Unit Tests**:
```python
# tests/test_safety_scorer.py

def test_score_no_sites():
    """Test scoring with 0 unremediated sites"""
    scorer = SafetyScorer(mock_proximity, mock_data)
    result = scorer.evaluate_address("123 Safe St, MT")
    
    assert result.safety_score == 100.0
    assert result.risk_level == "SAFE"

def test_score_one_site():
    """Test scoring with 1 unremediated site"""
    result = scorer.evaluate_address("456 Oak St, CA")
    
    assert result.safety_score == 75.0
    assert result.risk_level == "LOW RISK"

def test_score_four_sites():
    """Test scoring with 4+ sites (floor at 0%)"""
    result = scorer.evaluate_address("789 Industrial Rd, NJ")
    
    assert result.safety_score == 0.0
    assert result.risk_level == "CRITICAL RISK"
    assert len(result.unremediated_sites) >= 4

def test_geocoding_failure():
    """Test handling of invalid address"""
    result = scorer.evaluate_address("Invalid Address XYZ")
    
    assert result.error is not None
    assert result.risk_level == "UNKNOWN"
```

---

### 2.2 ProximityChecker Class

**Location**: `src/proximity_checker.py`

**Purpose**: Geocode addresses and find nearby SuperFund sites.

**Class Definition**:
```python
from typing import List, Optional, Tuple
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

class ProximityChecker:
    """Handle geocoding and proximity calculations"""
    
    def __init__(self, superfund_data: pd.DataFrame, user_agent: str = "superfund_chatbot"):
        """
        Initialize proximity checker
        
        Args:
            superfund_data: DataFrame with SuperFund sites (must have Latitude, Longitude)
            user_agent: User agent for Nominatim
        """
        self.superfund_data = superfund_data
        self.geocoder = Nominatim(user_agent=user_agent, timeout=10)
        self._geocode_cache = {}  # Cache to avoid repeated API calls
        
        # Validate SuperFund data has coordinates
        if 'Latitude' not in superfund_data.columns or 'Longitude' not in superfund_data.columns:
            raise ValueError("SuperFund data must include Latitude and Longitude columns")
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Convert address to (latitude, longitude)
        
        Args:
            address: Full street address
            
        Returns:
            (lat, lon) tuple or None if geocoding fails
        """
        # Check cache first
        if address in self._geocode_cache:
            return self._geocode_cache[address]
        
        try:
            # Rate limiting (Nominatim: 1 req/sec)
            time.sleep(1)
            
            location = self.geocoder.geocode(address)
            
            if location:
                coords = (location.latitude, location.longitude)
                self._geocode_cache[address] = coords
                return coords
            
            return None
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error for {address}: {e}")
            return None
    
    def calculate_distance(
        self,
        point1: Tuple[float, float],
        point2: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two points in miles
        
        Args:
            point1: (lat, lon)
            point2: (lat, lon)
            
        Returns:
            Distance in miles
        """
        return geodesic(point1, point2).miles
    
    def find_sites_within_radius(
        self,
        lat: float,
        lon: float,
        radius_miles: float
    ) -> List[dict]:
        """
        Find all SuperFund sites within radius
        
        Args:
            lat: Latitude of center point
            lon: Longitude of center point
            radius_miles: Search radius in miles
            
        Returns:
            List of site dictionaries with distance added
        """
        center = (lat, lon)
        nearby_sites = []
        
        for _, site in self.superfund_data.iterrows():
            site_coords = (site['Latitude'], site['Longitude'])
            distance = self.calculate_distance(center, site_coords)
            
            if distance <= radius_miles:
                site_dict = site.to_dict()
                site_dict['distance_miles'] = round(distance, 2)
                nearby_sites.append(site_dict)
        
        # Sort by distance (closest first)
        nearby_sites.sort(key=lambda x: x['distance_miles'])
        
        return nearby_sites
```

---

### 2.3 RAGGenerator Class

**Location**: `src/rag_generator.py`

**Purpose**: Generate comprehensive summary reports using RAG.

**Class Definition**:
```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import Document
from typing import List
from dataclasses import dataclass

@dataclass
class RAGSummary:
    """Generated RAG summary"""
    report: str
    sources: List[str]
    token_count: int

class RAGGenerator:
    """Generate RAG-based summaries"""
    
    SUMMARY_TEMPLATE = """You are an environmental risk assessment expert. 
    Generate a comprehensive report for the property at {address}.

Safety Score: {score}% ({risk_level})
Sites Found: {sites_count} unremediated SuperFund sites within {radius} miles

Site Details:
{site_details}

Generate a professional report with these sections:
1. Executive Summary (2-3 sentences)
2. Nearby SuperFund Sites (bullet list with key details)
3. Risk Analysis (paragraph explaining implications)
4. Recommendations (3-5 actionable items)

Use clear, professional language. Be factual and cite specific distances and contaminants.
"""
    
    def __init__(self, llm_model: str = "gpt-3.5-turbo", temperature: float = 0.3):
        """
        Initialize RAG generator
        
        Args:
            llm_model: OpenAI model name
            temperature: LLM temperature (lower = more factual)
        """
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_template(self.SUMMARY_TEMPLATE)
    
    def generate_summary(
        self,
        address: str,
        safety_score: float,
        risk_level: str,
        unremediated_sites: List[dict],
        radius_miles: float = 50
    ) -> RAGSummary:
        """
        Generate comprehensive summary report
        
        Args:
            address: Property address
            safety_score: Calculated safety score
            risk_level: Risk classification
            unremediated_sites: List of nearby sites
            radius_miles: Search radius used
            
        Returns:
            RAGSummary with report text
        """
        # Format site details
        site_details = self._format_site_details(unremediated_sites)
        
        # Generate prompt
        messages = self.prompt.format_messages(
            address=address,
            score=safety_score,
            risk_level=risk_level,
            sites_count=len(unremediated_sites),
            radius=radius_miles,
            site_details=site_details
        )
        
        # Generate response
        response = self.llm.invoke(messages)
        
        # Extract sources
        sources = [site.get('Site_Name', 'Unknown') for site in unremediated_sites]
        
        return RAGSummary(
            report=response.content,
            sources=sources,
            token_count=len(response.content.split())  # Rough estimate
        )
    
    def _format_site_details(self, sites: List[dict]) -> str:
        """Format site details for prompt"""
        if not sites:
            return "No unremediated sites found."
        
        formatted = []
        for i, site in enumerate(sites, 1):
            formatted.append(f"""
{i}. {site.get('Site_Name', 'Unknown')}
   - EPA ID: {site.get('EPA_ID', 'N/A')}
   - Distance: {site.get('distance_miles', 'N/A')} miles
   - Status: {site.get('Status', 'Unknown')}
   - Contaminants: {site.get('Contaminants', 'Not specified')}
""")
        
        return "\n".join(formatted)
```

---

### 2.4 Strategy Pattern Implementation

**Location**: `src/data/strategy.py`

**Purpose**: Abstract interface for data backends.

```python
from abc import ABC, abstractmethod
from typing import List, Dict
from .specification import Specification

class DataStrategy(ABC):
    """Abstract strategy for data access"""
    
    @abstractmethod
    def query(self, specification: Specification) -> List[Dict]:
        """
        Query data using specification
        
        Args:
            specification: Specification object defining criteria
            
        Returns:
            List of matching records as dictionaries
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Dict]:
        """Get all records"""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total records"""
        pass
```

**CSV Implementation**: `src/data/csv_strategy.py`

```python
import pandas as pd
from typing import List, Dict
from .strategy import DataStrategy
from .specification import Specification

class CSVDataStrategy(DataStrategy):
    """CSV file data strategy"""
    
    def __init__(self, file_path: str):
        """
        Initialize with CSV file
        
        Args:
            file_path: Path to CSV file
        """
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
    
    def query(self, specification: Specification) -> List[Dict]:
        """Query using specification"""
        # Apply specification to each row
        mask = self.df.apply(
            lambda row: specification.is_satisfied_by(row.to_dict()),
            axis=1
        )
        
        filtered_df = self.df[mask]
        return filtered_df.to_dict('records')
    
    def get_all(self) -> List[Dict]:
        """Get all records"""
        return self.df.to_dict('records')
    
    def count(self) -> int:
        """Count records"""
        return len(self.df)
    
    def reload(self):
        """Reload data from file"""
        self.df = pd.read_csv(self.file_path)
```

---

### 2.5 Specification Pattern Implementation

**Location**: `src/data/specification.py`

```python
from abc import ABC, abstractmethod
from typing import Dict
from geopy.distance import geodesic

class Specification(ABC):
    """Abstract specification for composable queries"""
    
    @abstractmethod
    def is_satisfied_by(self, item: Dict) -> bool:
        """Check if item satisfies specification"""
        pass
    
    def and_(self, other: 'Specification') -> 'Specification':
        """Logical AND"""
        return AndSpecification(self, other)
    
    def or_(self, other: 'Specification') -> 'Specification':
        """Logical OR"""
        return OrSpecification(self, other)
    
    def not_(self) -> 'Specification':
        """Logical NOT"""
        return NotSpecification(self)

class AndSpecification(Specification):
    """AND combination"""
    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2
    
    def is_satisfied_by(self, item: Dict) -> bool:
        return self.spec1.is_satisfied_by(item) and self.spec2.is_satisfied_by(item)

class OrSpecification(Specification):
    """OR combination"""
    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2
    
    def is_satisfied_by(self, item: Dict) -> bool:
        return self.spec1.is_satisfied_by(item) or self.spec2.is_satisfied_by(item)

class NotSpecification(Specification):
    """NOT negation"""
    def __init__(self, spec: Specification):
        self.spec = spec
    
    def is_satisfied_by(self, item: Dict) -> bool:
        return not self.spec.is_satisfied_by(item)

class StateSpecification(Specification):
    """Filter by state"""
    def __init__(self, state: str):
        self.state = state.upper()
    
    def is_satisfied_by(self, item: Dict) -> bool:
        return item.get('State', '').upper() == self.state

class ProximitySpecification(Specification):
    """Filter by proximity to coordinates"""
    def __init__(self, lat: float, lon: float, radius_miles: float):
        self.center = (lat, lon)
        self.radius = radius_miles
    
    def is_satisfied_by(self, item: Dict) -> bool:
        if 'Latitude' not in item or 'Longitude' not in item:
            return False
        
        try:
            site_coords = (float(item['Latitude']), float(item['Longitude']))
            distance = geodesic(self.center, site_coords).miles
            return distance <= self.radius
        except (ValueError, TypeError):
            return False

class StatusSpecification(Specification):
    """Filter by status"""
    def __init__(self, statuses: List[str]):
        self.statuses = [s.upper() for s in statuses]
    
    def is_satisfied_by(self, item: Dict) -> bool:
        return item.get('Status', '').upper() in self.statuses
```

**Usage Example**:
```python
# Find unremediated sites in CA within 50 miles of coordinates
spec = (
    StateSpecification("CA")
    .and_(StatusSpecification(["Final NPL", "Active", "Ongoing Cleanup"]))
    .and_(ProximitySpecification(34.0522, -118.2437, 50))
)

# Works with any strategy
results = data_strategy.query(spec)
```

---

## 3. API Specifications

### 3.1 SafetyScorer API

```python
class SafetyScorer:
    def evaluate_address(
        address: str,
        radius_miles: float = 50
    ) -> SafetyScore
    """
    Evaluate single address
    
    Args:
        address: Full street address (e.g., "123 Main St, San Diego CA 92101")
        radius_miles: Search radius (default: 50)
    
    Returns:
        SafetyScore dataclass with:
            - address: str
            - coordinates: Optional[Tuple[float, float]]
            - safety_score: float (0-100)
            - risk_level: str ("SAFE" | "LOW RISK" | "MEDIUM RISK" | "HIGH RISK" | "CRITICAL RISK")
            - sites_found: int
            - unremediated_sites: List[dict]
            - error: Optional[str]
    
    Raises:
        None (errors returned in SafetyScore.error field)
    
    Performance:
        - Typical: 2-4 seconds (includes geocoding)
        - Cached address: <1 second
    """
    
    def evaluate_batch(
        addresses: List[str],
        radius_miles: float = 50
    ) -> List[SafetyScore]
    """
    Evaluate multiple addresses
    
    Args:
        addresses: List of addresses
        radius_miles: Search radius
    
    Returns:
        List of SafetyScore objects (one per address)
    
    Performance:
        - Sequential processing
        - ~3 seconds per address (geocoding rate limit)
        - 10 addresses: ~30 seconds
    """
```

### 3.2 RAGGenerator API

```python
class RAGGenerator:
    def generate_summary(
        address: str,
        safety_score: float,
        risk_level: str,
        unremediated_sites: List[dict],
        radius_miles: float = 50
    ) -> RAGSummary
    """
    Generate comprehensive summary report
    
    Args:
        address: Property address
        safety_score: Score (0-100)
        risk_level: Risk classification
        unremediated_sites: List of nearby sites with details
        radius_miles: Radius used for search
    
    Returns:
        RAGSummary dataclass with:
            - report: str (formatted markdown)
            - sources: List[str] (site names)
            - token_count: int (approximate)
    
    Performance:
        - Typical: 2-3 seconds
        - Token usage: 500-1000 tokens
        - Cost: ~$0.002 per summary
    """
```

---

## 4. Data Models

### 4.1 SuperFund Sites Data Schema

```python
# DataFrame columns
SUPERFUND_SCHEMA = {
    'EPA_ID': str,              # Unique identifier (e.g., "CAD980498612")
    'Site_Name': str,           # Site name
    'Address': str,             # Street address
    'City': str,                # City
    'State': str,               # 2-letter state code
    'ZIP': str,                 # 5-digit ZIP
    'Latitude': float,          # Decimal degrees
    'Longitude': float,         # Decimal degrees
    'NPL_Status': str,          # "Final NPL", "Proposed NPL", etc.
    'Status': str,              # "Active", "Cleanup Complete", etc.
    'Contaminants': str,        # Comma-separated list
    'Cleanup_Status': str       # Description of cleanup progress
}

# Example row
{
    'EPA_ID': 'CAD980498612',
    'Site_Name': 'Operating Industries Inc',
    'Address': '5950 Azusa Canyon Rd',
    'City': 'Irwindale',
    'State': 'CA',
    'ZIP': '91706',
    'Latitude': 34.1395,
    'Longitude': -117.9539,
    'NPL_Status': 'Final NPL',
    'Status': 'Active',
    'Contaminants': 'VOCs, Heavy Metals, PCBs',
    'Cleanup_Status': 'Ongoing remediation, estimated completion 2028'
}
```

### 4.2 Policy Data Schema

```python
# Required fields
POLICY_SCHEMA_REQUIRED = {
    'Policy_ID': str,           # Unique identifier
    'Property_Address': str,    # Full street address
    'City': str,                # City
    'State': str,               # 2-letter code
    'ZIP': str                  # 5-digit ZIP
}

# Optional fields
POLICY_SCHEMA_OPTIONAL = {
    'Policy_Type': str,         # "Residential", "Commercial", "Industrial"
    'Coverage_Amount': float,   # Dollar amount
    'Effective_Date': str,      # ISO date
    'Latitude': float,          # Pre-geocoded (optional)
    'Longitude': float          # Pre-geocoded (optional)
}

# After evaluation, these fields are added:
POLICY_SCHEMA_EVALUATED = {
    'Safety_Score': float,      # 0-100
    'Risk_Level': str,          # "SAFE", "LOW RISK", etc.
    'Sites_Found': int,         # Count of nearby sites
    'Nearest_Site': str,        # Name of closest site
    'Nearest_Distance': float   # Distance in miles
}
```

---

## 5. Implementation Details

### 5.1 Streamlit Layout Implementation

**File**: `app.py`

```python
import streamlit as st
from src.section_manager import SectionManager, Section
from components.chat_interface import ChatInterface
from components.data_grid import DataGrid
from components.map_display import MapDisplay
from components.debug_panel import DebugPanel

# Page config
st.set_page_config(
    page_title="SuperFund Site Checker",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize section manager
section_manager = SectionManager()

# Check if any section is maximized
if section_manager.is_maximized():
    # Render only maximized section
    maximized = section_manager.get_maximized_section()
    render_maximized_section(maximized)
else:
    # Normal layout: 60/40 split
    col_chat, col_sidebar = st.columns([3, 2])
    
    with col_chat:
        # Chat section (full height)
        ChatInterface().render()
    
    with col_sidebar:
        # Data grid
        DataGrid().render()
        
        # Image/Map
        MapDisplay().render()
        
        # Debug (if enabled)
        if st.secrets.get("DEBUG_MODE", False):
            DebugPanel().render()
```

### 5.2 Section Manager Implementation

**File**: `src/section_manager.py`

```python
from enum import Enum
import streamlit as st

class Section(Enum):
    CHAT = "chat"
    DATA_GRID = "data_grid"
    IMAGE = "image"
    DEBUG = "debug"

class SectionState(Enum):
    COLLAPSED = "collapsed"
    NORMAL = "normal"
    MAXIMIZED = "maximized"

class SectionManager:
    """Manage section visibility and state"""
    
    def __init__(self):
        if "section_states" not in st.session_state:
            st.session_state.section_states = {
                Section.CHAT: SectionState.NORMAL,
                Section.DATA_GRID: SectionState.COLLAPSED,
                Section.IMAGE: SectionState.COLLAPSED,
                Section.DEBUG: SectionState.COLLAPSED
            }
        
        if "maximized_section" not in st.session_state:
            st.session_state.maximized_section = None
    
    def toggle_collapse(self, section: Section):
        """Toggle between collapsed and normal"""
        current = st.session_state.section_states[section]
        if current == SectionState.COLLAPSED:
            st.session_state.section_states[section] = SectionState.NORMAL
        else:
            st.session_state.section_states[section] = SectionState.COLLAPSED
        st.rerun()
    
    def toggle_maximize(self, section: Section):
        """Toggle maximize/restore"""
        if st.session_state.maximized_section == section:
            st.session_state.maximized_section = None
            st.session_state.section_states[section] = SectionState.NORMAL
        else:
            st.session_state.maximized_section = section
            st.session_state.section_states[section] = SectionState.MAXIMIZED
        st.rerun()
    
    def expand(self, section: Section):
        """Programmatically expand section"""
        if st.session_state.section_states[section] == SectionState.COLLAPSED:
            st.session_state.section_states[section] = SectionState.NORMAL
    
    def is_maximized(self) -> bool:
        """Check if any section is maximized"""
        return st.session_state.maximized_section is not None
    
    def get_maximized_section(self) -> Section:
        """Get currently maximized section"""
        return st.session_state.maximized_section
    
    def get_state(self, section: Section) -> SectionState:
        """Get current state of section"""
        return st.session_state.section_states[section]
```

---

## 6. Testing Strategy

### 6.1 Unit Tests

**Test Coverage Requirements**: >80%

**Key Test Files**:
```
tests/
├── test_safety_scorer.py       # Scoring algorithm
├── test_proximity_checker.py   # Geocoding and distance
├── test_specifications.py      # Specification pattern
├── test_strategies.py          # Strategy pattern
└── test_rag_generator.py       # RAG generation
```

**Example Tests**:

```python
# tests/test_safety_scorer.py
import pytest
from src.safety_scorer import SafetyScorer

def test_scoring_zero_sites():
    scorer = SafetyScorer(mock_proximity, mock_data)
    result = scorer.evaluate_address("123 Safe St")
    assert result.safety_score == 100.0
    assert result.risk_level == "SAFE"

def test_scoring_one_site():
    result = scorer.evaluate_address("456 Risk St")
    assert result.safety_score == 75.0
    assert result.risk_level == "LOW RISK"

def test_scoring_floor_at_zero():
    result = scorer.evaluate_address("789 Danger St")
    assert result.safety_score == 0.0
    assert result.risk_level == "CRITICAL RISK"

# tests/test_specifications.py
def test_state_specification():
    spec = StateSpecification("CA")
    assert spec.is_satisfied_by({"State": "CA"}) == True
    assert spec.is_satisfied_by({"State": "NY"}) == False

def test_proximity_specification():
    spec = ProximitySpecification(34.05, -118.24, 50)
    nearby = {"Latitude": 34.10, "Longitude": -118.20}
    far = {"Latitude": 40.71, "Longitude": -74.01}
    
    assert spec.is_satisfied_by(nearby) == True
    assert spec.is_satisfied_by(far) == False

def test_combined_specifications():
    spec = StateSpecification("CA").and_(
        StatusSpecification(["Active", "Final NPL"])
    )
    
    assert spec.is_satisfied_by({"State": "CA", "Status": "Active"}) == True
    assert spec.is_satisfied_by({"State": "NY", "Status": "Active"}) == False
```

### 6.2 Integration Tests

**End-to-End Workflows**:

```python
# tests/test_integration.py

def test_full_evaluation_workflow():
    """Test complete address evaluation"""
    # Setup
    scorer = SafetyScorer(ProximityChecker(superfund_df), superfund_df)
    
    # Execute
    result = scorer.evaluate_address("123 Main St, San Diego CA")
    
    # Verify
    assert result.coordinates is not None
    assert result.safety_score >= 0.0 and result.safety_score <= 100.0
    assert result.risk_level in ["SAFE", "LOW RISK", "MEDIUM RISK", "HIGH RISK", "CRITICAL RISK"]
    assert len(result.unremediated_sites) == (100 - result.safety_score) / 25

def test_rag_generation_workflow():
    """Test RAG summary generation"""
    # Setup
    rag = RAGGenerator()
    sites = [{"Site_Name": "Test Site", "distance_miles": 5.0}]
    
    # Execute
    summary = rag.generate_summary(
        address="123 Test St",
        safety_score=75.0,
        risk_level="LOW RISK",
        unremediated_sites=sites
    )
    
    # Verify
    assert len(summary.report) > 100
    assert "Executive Summary" in summary.report
    assert "75%" in summary.report or "LOW RISK" in summary.report
```

---

## 7. Deployment Guide

### 7.1 Local Development Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/SuperFundSiteChatBot.git
cd SuperFundSiteChatBot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Download SuperFund data
python scripts/download_superfund_data.py

# 6. Run application
streamlit run app.py
```

### 7.2 Streamlit Cloud Deployment

**File**: `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
maxUploadSize = 10
enableCORS = false
```

**Deployment Steps**:
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect repository
4. Add secrets:
   ```
   OPENAI_API_KEY = "sk-..."
   DEBUG_MODE = false
   ```
5. Deploy

### 7.3 Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...           # Required
DEBUG_MODE=false                # Optional (default: false)
LLM_MODEL=gpt-3.5-turbo        # Optional (default: gpt-3.5-turbo)
GEOCODING_USER_AGENT=superfund_chatbot  # Optional
```

---

## 8. Performance Optimization

### 8.1 Caching Strategy

```python
# Cache geocoding results
@st.cache_data(ttl=3600*24)  # 24 hours
def geocode_address(address: str):
    ...

# Cache data loading
@st.cache_resource
def load_superfund_data():
    return pd.read_csv("data/superfund_sites.csv")

# Cache LLM initialization
@st.cache_resource
def init_llm():
    return ChatOpenAI(model="gpt-3.5-turbo")
```

### 8.2 Batch Processing Optimization

```python
# Parallel geocoding (future enhancement)
from concurrent.futures import ThreadPoolExecutor

def evaluate_batch_parallel(addresses, max_workers=3):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(evaluate_address, addresses)
    return list(results)
```

---

**Document Status**: ✅ Complete

**Next Steps**:
1. Begin Phase 1: Core Infrastructure
2. Implement SafetyScorer class
3. Set up testing framework
4. Create initial Streamlit layout

---

*End of Technical Specification*
