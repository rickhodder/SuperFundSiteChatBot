"""
Quick test script to verify core functionality.
Run this before starting the Streamlit app.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import streamlit
        import pandas
        import geopy
        import langchain
        print("✅ All required packages installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        import config.settings as settings
        print(f"✅ Config loaded")
        print(f"  - App Title: {settings.APP_TITLE}")
        print(f"  - Proximity Radius: {settings.PROXIMITY_RADIUS_MILES} miles")
        print(f"  - Score Penalty: {settings.SCORE_PENALTY_PER_SITE} per site")
        
        if not settings.OPENAI_API_KEY:
            print("⚠️  WARNING: OPENAI_API_KEY not set in .env")
        else:
            print(f"✅ OpenAI API Key configured")
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_data_file():
    """Test that CSV data file exists."""
    print("\nTesting data file...")
    try:
        from config.settings import SUPERFUND_DATA_FILE
        import pandas as pd
        
        df = pd.read_csv(SUPERFUND_DATA_FILE)
        print(f"✅ CSV loaded: {len(df)} SuperFund sites")
        print(f"  - Columns: {', '.join(df.columns.tolist())}")
        
        # Show sample
        print("\n  Sample sites:")
        for idx, row in df.head(3).iterrows():
            print(f"    - {row['site_name']} ({row['city']}, {row['state']})")
        
        return True
    except Exception as e:
        print(f"❌ Data file error: {e}")
        return False

def test_strategy_pattern():
    """Test Strategy pattern backend."""
    print("\nTesting Strategy pattern...")
    try:
        from src.strategy import BackendFactory, CSVBackend
        
        backend = BackendFactory.create_backend("csv")
        data = backend.load_data()
        
        print(f"✅ Backend initialized: {backend.__class__.__name__}")
        print(f"  - Sites loaded: {len(data)}")
        
        return True
    except Exception as e:
        print(f"❌ Strategy pattern error: {e}")
        return False

def test_specifications():
    """Test Specification pattern."""
    print("\nTesting Specification pattern...")
    try:
        from src.specifications import GeospatialSpecification, StateSpecification
        from src.strategy import BackendFactory
        
        backend = BackendFactory.create_backend("csv")
        data = backend.load_data()
        
        # Test geospatial query (Brooklyn)
        spec = GeospatialSpecification(40.6782, -73.9442, 10)
        results = spec.is_satisfied_by(data)
        
        print(f"✅ Geospatial query works")
        print(f"  - Sites within 10mi of Brooklyn: {len(results)}")
        
        # Test state query
        ny_spec = StateSpecification("NY")
        ny_results = ny_spec.is_satisfied_by(data)
        
        print(f"  - Sites in NY state: {len(ny_results)}")
        
        return True
    except Exception as e:
        print(f"❌ Specification pattern error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_safety_scorer():
    """Test SafetyScorer."""
    print("\nTesting SafetyScorer...")
    try:
        from src.safety_scorer import SafetyScorer
        
        scorer = SafetyScorer()
        
        # Test with Brooklyn coordinates (near Gowanus Canal)
        result = scorer.score_policy(
            latitude=40.6753,
            longitude=-73.9985
        )
        
        print(f"✅ SafetyScorer works")
        print(f"  - Score: {result['score']}/100")
        print(f"  - Risk Level: {result['risk_level']}")
        print(f"  - Nearby Sites: {result['site_count']}")
        
        return True
    except Exception as e:
        print(f"❌ SafetyScorer error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("SuperFund Site Safety Checker - System Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_data_file,
        test_strategy_pattern,
        test_specifications,
        test_safety_scorer
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✅ All tests passed! Ready to run: streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Fix issues before running app.")
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
