"""
Safety Scorer: Calculate insurance policy safety scores.
Algorithm: Start at 100%, deduct 25% per unremediated site within 50 miles, minimum 0%.
"""
from typing import Tuple, Dict, List
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import config.settings as settings
from src.specifications import unremediated_within_radius
from src.strategy import get_backend


class SafetyScorer:
    """
    Calculate safety scores for insurance policies based on proximity to SuperFund sites.
    """
    
    def __init__(self):
        self.initial_score = settings.INITIAL_SCORE
        self.penalty_per_site = settings.SCORE_PENALTY_PER_SITE
        self.radius_miles = settings.PROXIMITY_RADIUS_MILES
        self.minimum_score = settings.MINIMUM_SCORE
        self.risk_levels = settings.RISK_LEVELS
        
        # Initialize geocoder
        self.geocoder = Nominatim(user_agent="superfund_safety_checker")
    
    def geocode_address(self, address: str) -> Tuple[float, float]:
        """
        Convert address to latitude/longitude coordinates.
        
        Args:
            address: Full address string
        
        Returns:
            Tuple of (latitude, longitude)
        
        Raises:
            ValueError: If address cannot be geocoded
        """
        try:
            location = self.geocoder.geocode(address, timeout=10)
            
            if location:
                return (location.latitude, location.longitude)
            else:
                raise ValueError(f"Could not geocode address: {address}")
        
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            raise ValueError(f"Geocoding service error: {str(e)}")
    
    def score_policy(
        self,
        address: str = None,
        latitude: float = None,
        longitude: float = None
    ) -> Dict:
        """
        Calculate safety score for an insurance policy location.
        
        Args:
            address: Full address (will be geocoded if lat/lon not provided)
            latitude: Latitude coordinate (optional if address provided)
            longitude: Longitude coordinate (optional if address provided)
        
        Returns:
            Dict with keys:
                - score: Safety score (0-100)
                - risk_level: Risk category (SAFE/LOW/MEDIUM/HIGH/CRITICAL)
                - nearby_sites: DataFrame of nearby unremediated sites
                - site_count: Number of nearby unremediated sites
                - location: Tuple of (lat, lon)
        """
        # Get coordinates
        if latitude is None or longitude is None:
            if address is None:
                raise ValueError("Must provide either address or (latitude, longitude)")
            latitude, longitude = self.geocode_address(address)
        
        location = (latitude, longitude)
        
        # Query unremediated sites within radius using Specification pattern
        spec = unremediated_within_radius(latitude, longitude, self.radius_miles)
        backend = get_backend()
        nearby_sites = backend.query_superfund(spec)
        
        site_count = len(nearby_sites)
        
        # Calculate score
        score = self.initial_score - (site_count * self.penalty_per_site)
        score = max(score, self.minimum_score)  # Floor at 0
        
        # Determine risk level
        risk_level = self._get_risk_level(score)
        
        return {
            'score': score,
            'risk_level': risk_level,
            'nearby_sites': nearby_sites,
            'site_count': site_count,
            'location': location,
            'radius_miles': self.radius_miles
        }
    
    def _get_risk_level(self, score: int) -> str:
        """
        Map score to risk level category.
        
        Args:
            score: Safety score (0-100)
        
        Returns:
            Risk level string
        """
        # Sort thresholds in descending order
        for threshold in sorted(self.risk_levels.keys(), reverse=True):
            if score >= threshold:
                return self.risk_levels[threshold]
        
        return "CRITICAL"  # Fallback
    
    def batch_score_policies(self, addresses: List[str]) -> pd.DataFrame:
        """
        Score multiple policy locations at once.
        
        Args:
            addresses: List of address strings
        
        Returns:
            DataFrame with columns: address, score, risk_level, site_count
        """
        results = []
        
        for address in addresses:
            try:
                result = self.score_policy(address=address)
                results.append({
                    'address': address,
                    'latitude': result['location'][0],
                    'longitude': result['location'][1],
                    'score': result['score'],
                    'risk_level': result['risk_level'],
                    'site_count': result['site_count']
                })
            except Exception as e:
                results.append({
                    'address': address,
                    'latitude': None,
                    'longitude': None,
                    'score': None,
                    'risk_level': 'ERROR',
                    'site_count': None,
                    'error': str(e)
                })
        
        return pd.DataFrame(results)
    
    def batch_score_from_csv(self) -> pd.DataFrame:
        """
        Score all policies loaded from CSV file.
        
        Returns:
            DataFrame with columns: policy_id, address, score, risk_level, site_count
        """
        backend = get_backend()
        policies = backend.get_all_policies()
        
        if policies.empty:
            print("⚠ No policies found in CSV")
            return pd.DataFrame()
        
        results = []
        
        for idx, policy in policies.iterrows():
            try:
                # Use lat/lon from policy if available, otherwise geocode
                if 'Latitude' in policy and 'Longitude' in policy and \
                   pd.notna(policy['Latitude']) and pd.notna(policy['Longitude']):
                    result = self.score_policy(
                        latitude=policy['Latitude'],
                        longitude=policy['Longitude']
                    )
                else:
                    # Geocode the address
                    address = f"{policy.get('Address', '')}, {policy.get('City', '')}, {policy.get('State', '')}"
                    result = self.score_policy(address=address)
                
                results.append({
                    'policy_id': policy.get('Id', f'P-{idx}'),
                    'address': policy.get('Address', 'Unknown'),
                    'city': policy.get('City', 'Unknown'),
                    'state': policy.get('State', 'N/A'),
                    'latitude': result['location'][0],
                    'longitude': result['location'][1],
                    'score': result['score'],
                    'risk_level': result['risk_level'],
                    'site_count': result['site_count'],
                    'property_value': policy.get('property_value', None),
                    'coverage_type': policy.get('coverage_type', 'Unknown')
                })
            except Exception as e:
                print(f"⚠ Error scoring policy {policy.get('policy_id', idx)}: {str(e)}")
                results.append({
                    'policy_id': policy.get('Id', f'P-{idx}'),
                    'address': policy.get('Address', 'Unknown'),
                    'city': policy.get('City', 'Unknown'),
                    'state': policy.get('State', 'N/A'),
                    'latitude': None,
                    'longitude': None,
                    'score': None,
                    'risk_level': 'ERROR',
                    'site_count': None,
                    'property_value': policy.get('property_value', None),
                    'coverage_type': policy.get('PolicyType', 'Unknown'),
                    'error': str(e)
                })
        
        return pd.DataFrame(results)


def format_score_report(score_result: Dict) -> str:
    """
    Format score result as readable text report.
    
    Args:
        score_result: Result dictionary from SafetyScorer.score_policy()
    
    Returns:
        Formatted string report
    """
    report = f"""
🎯 **Safety Score: {score_result['score']}/100**
⚠️ **Risk Level: {score_result['risk_level']}**

📍 **Location**: {score_result['location'][0]:.4f}, {score_result['location'][1]:.4f}
📏 **Search Radius**: {score_result['radius_miles']} miles
🏭 **Nearby Unremediated Sites**: {score_result['site_count']}

"""
    
    if score_result['site_count'] > 0:
        report += "**Sites Found:**\n"
        sites = score_result['nearby_sites']
        for idx, site in sites.head(5).iterrows():
            report += f"- {site.get('SiteName', 'Unknown')} ({site.get('City', 'Unknown')}, {site.get('State', 'N/A')})\n"
        
        if score_result['site_count'] > 5:
            report += f"\n_...and {score_result['site_count'] - 5} more sites_\n"
    
    return report
