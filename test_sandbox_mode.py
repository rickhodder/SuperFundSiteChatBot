"""
Quick test for sandbox mode address lookup.
Tests that addresses can be found in local CSV files without web API.
"""
from src.safety_scorer import SafetyScorer
from src.strategy import get_backend

def test_address_lookup():
    """Test local address lookup from CSVs."""
    
    print("=" * 60)
    print("SANDBOX MODE ADDRESS LOOKUP TEST")
    print("=" * 60)
    
    # Initialize
    backend = get_backend()
    scorer = SafetyScorer()
    
    # Test addresses from policies.csv
    test_addresses_policies = [
        "3048 Pine Road, Anchorage, AK 99501",
        "8766 Park Avenue, Seattle, WA 98101",
        "3268 Maple Drive, Burlington, VT 05401",
    ]
    
    # Test addresses from superfund_sites.csv
    test_addresses_sites = [
        "1361 Industrial Blvd, Burlington, VT 05401",
    ]
    
    print("\n📋 Testing Policy Addresses:")
    print("-" * 60)
    for address in test_addresses_policies:
        try:
            lat, lon = backend.get_coordinates_by_address(address)
            print(f"✅ {address}")
            print(f"   → ({lat}, {lon})")
        except ValueError as e:
            print(f"❌ {address}")
            print(f"   → Error: {e}")
    
    print("\n🏭 Testing SuperFund Site Addresses:")
    print("-" * 60)
    for address in test_addresses_sites:
        try:
            lat, lon = backend.get_coordinates_by_address(address)
            print(f"✅ {address}")
            print(f"   → ({lat}, {lon})")
        except ValueError as e:
            print(f"❌ {address}")
            print(f"   → Error: {e}")
    
    print("\n🎯 Testing Full Scoring Flow:")
    print("-" * 60)
    test_address = "8766 Park Avenue, Seattle, WA 98101"
    print(f"Scoring: {test_address}")
    try:
        result = scorer.score_policy(address=test_address)
        print(f"✅ Score: {result['score']}/100")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Nearby Sites: {result['site_count']}")
        print(f"   Location: {result['location']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n❌ Testing Invalid Address (Should Fail):")
    print("-" * 60)
    try:
        lat, lon = backend.get_coordinates_by_address("123 Fake Street, Nowhere, XX 00000")
        print(f"⚠️  Unexpected success: ({lat}, {lon})")
    except ValueError as e:
        print(f"✅ Expected error received:")
        print(f"   {str(e)[:100]}...")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_address_lookup()
