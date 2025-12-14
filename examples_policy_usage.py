"""
Example usage of Policy data with Strategy and Specification patterns.
"""
from src.strategy import get_backend
from src.specifications import (
    policies_in_state,
    policies_near_location,
    policies_by_coverage_type,
    high_value_policies,
    PolicyGeospatialSpecification,
    PolicyStateSpecification
)
from src.safety_scorer import SafetyScorer


def example_1_load_all_policies():
    """Example 1: Load all policies from CSV."""
    print("\n=== Example 1: Load All Policies ===")
    backend = get_backend()
    policies = backend.get_all_policies()
    
    print(f"Loaded {len(policies)} policies")
    print(policies.head())


def example_2_query_policies_by_state():
    """Example 2: Query policies in a specific state."""
    print("\n=== Example 2: Policies in New York ===")
    backend = get_backend()
    
    # Use specification to filter
    ny_spec = policies_in_state("NY")
    ny_policies = backend.query_policies(ny_spec)
    
    print(f"Found {len(ny_policies)} policies in NY")
    print(ny_policies[['policy_id', 'address', 'city', 'state']])


def example_3_policies_near_location():
    """Example 3: Find policies near a location."""
    print("\n=== Example 3: Policies Near Brooklyn (40.68, -73.94) ===")
    backend = get_backend()
    
    # Find policies within 10 miles of Brooklyn
    brooklyn_spec = policies_near_location(40.6782, -73.9442, radius=10)
    nearby = backend.query_policies(brooklyn_spec)
    
    print(f"Found {len(nearby)} policies within 10 miles")
    print(nearby[['policy_id', 'address', 'city']])


def example_4_comprehensive_coverage():
    """Example 4: Find comprehensive coverage policies."""
    print("\n=== Example 4: Comprehensive Coverage Policies ===")
    backend = get_backend()
    
    comp_spec = policies_by_coverage_type("Comprehensive")
    comp_policies = backend.query_policies(comp_spec)
    
    print(f"Found {len(comp_policies)} comprehensive policies")
    print(comp_policies[['policy_id', 'address', 'coverage_type']])


def example_5_high_value_policies():
    """Example 5: Find high-value policies ($1M+)."""
    print("\n=== Example 5: High-Value Policies ($1M+) ===")
    backend = get_backend()
    
    high_val_spec = high_value_policies(min_value=1000000)
    high_val = backend.query_policies(high_val_spec)
    
    print(f"Found {len(high_val)} policies valued at $1M+")
    print(high_val[['policy_id', 'address', 'property_value']])


def example_6_composite_query():
    """Example 6: Composite query - NY state AND comprehensive coverage."""
    print("\n=== Example 6: Comprehensive Policies in NY ===")
    backend = get_backend()
    
    # Combine specifications with AND
    ny_comp_spec = policies_in_state("NY").and_spec(
        policies_by_coverage_type("Comprehensive")
    )
    
    results = backend.query_policies(ny_comp_spec)
    
    print(f"Found {len(results)} comprehensive policies in NY")
    print(results[['policy_id', 'address', 'city', 'coverage_type']])


def example_7_batch_score_all_policies():
    """Example 7: Score all policies from CSV."""
    print("\n=== Example 7: Batch Score All Policies ===")
    scorer = SafetyScorer()
    
    # Score all policies from CSV
    results = scorer.batch_score_from_csv()
    
    print(f"Scored {len(results)} policies")
    print("\nTop 5 riskiest policies:")
    print(results.sort_values('score')[['policy_id', 'address', 'score', 'risk_level', 'site_count']].head())
    
    print("\nTop 5 safest policies:")
    print(results.sort_values('score', ascending=False)[['policy_id', 'address', 'score', 'risk_level']].head())


def example_8_high_risk_policies_in_state():
    """Example 8: Find high-risk policies in a specific state."""
    print("\n=== Example 8: Score NY Policies Only ===")
    backend = get_backend()
    scorer = SafetyScorer()
    
    # Get NY policies
    ny_spec = policies_in_state("NY")
    ny_policies = backend.query_policies(ny_spec)
    
    print(f"Scoring {len(ny_policies)} NY policies...")
    
    results = []
    for _, policy in ny_policies.iterrows():
        result = scorer.score_policy(
            latitude=policy['latitude'],
            longitude=policy['longitude']
        )
        results.append({
            'policy_id': policy['policy_id'],
            'address': policy['address'],
            'score': result['score'],
            'risk_level': result['risk_level'],
            'site_count': result['site_count']
        })
    
    import pandas as pd
    results_df = pd.DataFrame(results)
    print(results_df.sort_values('score'))


if __name__ == "__main__":
    print("=" * 70)
    print("Policy Data Examples - Strategy & Specification Patterns")
    print("=" * 70)
    
    # Run all examples
    example_1_load_all_policies()
    example_2_query_policies_by_state()
    example_3_policies_near_location()
    example_4_comprehensive_coverage()
    example_5_high_value_policies()
    example_6_composite_query()
    example_7_batch_score_all_policies()
    example_8_high_risk_policies_in_state()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
