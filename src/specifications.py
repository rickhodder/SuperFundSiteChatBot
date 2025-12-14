"""
Specification Pattern: Composable Query Logic
Enables building complex queries from simple, testable components.
"""
from abc import ABC, abstractmethod
from typing import Any
import pandas as pd
from geopy.distance import geodesic
import config.settings as settings


class ISpecification(ABC):
    """Interface for specification pattern."""
    
    @abstractmethod
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Check if data satisfies this specification.
        Returns filtered DataFrame.
        """
        pass
    
    def and_spec(self, other: 'ISpecification') -> 'AndSpecification':
        """Combine with AND logic."""
        return AndSpecification(self, other)
    
    def or_spec(self, other: 'ISpecification') -> 'OrSpecification':
        """Combine with OR logic."""
        return OrSpecification(self, other)
    
    def not_spec(self) -> 'NotSpecification':
        """Negate this specification."""
        return NotSpecification(self)


class GeospatialSpecification(ISpecification):
    """Filter sites within a radius of a location."""
    
    def __init__(self, latitude: float, longitude: float, radius_miles: float):
        self.latitude = latitude
        self.longitude = longitude
        self.radius_miles = radius_miles
        self.center = (latitude, longitude)
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return sites within radius."""
        if data.empty:
            return data
        
        def within_radius(row):
            try:
                site_location = (row['Latitude'], row['Longitude'])
                distance = geodesic(self.center, site_location).miles
                return distance <= self.radius_miles
            except (KeyError, ValueError, TypeError):
                return False
        
        mask = data.apply(within_radius, axis=1)
        return data[mask].copy()


class StatusSpecification(ISpecification):
    """Filter sites by remediation status."""
    
    def __init__(self, status: str):
        """
        Args:
            status: One of 'Completed', 'In Progress', 'Not Started', 'Deleted'
        """
        self.status = status
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return sites matching status."""
        if data.empty or 'RemediationStatus' not in data.columns:
            return data

        return data[data['RemediationStatus'].str.lower() == self.status.lower()].copy()


class StateSpecification(ISpecification):
    """Filter sites by state."""
    
    def __init__(self, state: str):
        """
        Args:
            state: Two-letter state code (e.g., 'CA', 'NY')
        """
        self.state = state.upper()
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return sites in specified state."""
        if data.empty or 'State' not in data.columns:
            return data
        
        return data[data['State'].str.upper() == self.state].copy()


class ContaminantSpecification(ISpecification):
    """Filter sites by specific contaminant."""
    
    def __init__(self, contaminant: str):
        """
        Args:
            contaminant: Contaminant name to search for (case-insensitive)
        """
        self.contaminant = contaminant.lower()
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return sites with specified contaminant."""
        if data.empty or 'contaminants' not in data.columns:
            return data
        
        mask = data['contaminants'].fillna('').str.lower().str.contains(
            self.contaminant, case=False, regex=False
        )
        return data[mask].copy()


class AndSpecification(ISpecification):
    """Combine two specifications with AND logic."""
    
    def __init__(self, spec1: ISpecification, spec2: ISpecification):
        self.spec1 = spec1
        self.spec2 = spec2
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return data satisfying both specifications."""
        result = self.spec1.is_satisfied_by(data)
        return self.spec2.is_satisfied_by(result)


class OrSpecification(ISpecification):
    """Combine two specifications with OR logic."""
    
    def __init__(self, spec1: ISpecification, spec2: ISpecification):
        self.spec1 = spec1
        self.spec2 = spec2
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return data satisfying either specification."""
        result1 = self.spec1.is_satisfied_by(data)
        result2 = self.spec2.is_satisfied_by(data)
        
        # Combine and remove duplicates
        combined = pd.concat([result1, result2]).drop_duplicates()
        return combined


class NotSpecification(ISpecification):
    """Negate a specification."""
    
    def __init__(self, spec: ISpecification):
        self.spec = spec
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return data NOT satisfying the specification."""
        satisfied = self.spec.is_satisfied_by(data)
        
        # Return rows not in satisfied set
        if data.empty:
            return data
        
        # Use index difference to find unsatisfied rows
        unsatisfied_indices = data.index.difference(satisfied.index)
        return data.loc[unsatisfied_indices].copy()


class UnremediatedSpecification(ISpecification):
    """Filter for unremediated sites (status != 'Completed')."""
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return sites that are not completed."""
        if data.empty or 'RemediationStatus' not in data.columns:
            return data
        
        # Consider both 'In Progress' and 'Not Started' as unremediated
        mask = data['RemediationStatus'].str.lower() != 'Completed'
        return data[mask].copy()


# Policy-specific Specifications

class PolicyGeospatialSpecification(ISpecification):
    """Filter policies within a radius of a location."""
    
    def __init__(self, latitude: float, longitude: float, radius_miles: float):
        self.latitude = latitude
        self.longitude = longitude
        self.radius_miles = radius_miles
        self.center = (latitude, longitude)
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return policies within radius."""
        if data.empty:
            return data
        
        def within_radius(row):
            try:
                policy_location = (row['Latitude'], row['Longitude'])
                distance = geodesic(self.center, policy_location).miles
                return distance <= self.radius_miles
            except (KeyError, ValueError, TypeError):
                return False
        
        mask = data.apply(within_radius, axis=1)
        return data[mask].copy()


class PolicyStateSpecification(ISpecification):
    """Filter policies by state."""
    
    def __init__(self, state: str):
        """
        Args:
            state: Two-letter state code (e.g., 'CA', 'NY')
        """
        self.state = state.upper()
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return policies in specified state."""
        if data.empty or 'State' not in data.columns:
            return data

        return data[data['State'].str.upper() == self.state].copy()


class PolicyCitySpecification(ISpecification):
    """Filter policies by city."""
    
    def __init__(self, city: str):
        """
        Args:
            city: City name (case-insensitive)
        """
        self.city = city.lower()
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return policies in specified city."""
        if data.empty or 'City' not in data.columns:
            return data

        return data[data['City'].str.lower() == self.city].copy()


class PolicyCoverageTypeSpecification(ISpecification):
    """Filter policies by coverage type."""
    
    def __init__(self, coverage_type: str):
        """
        Args:
            coverage_type: Coverage type (e.g., 'Comprehensive', 'Fire & Liability')
        """
        self.coverage_type = coverage_type.lower()
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return policies with specified coverage type."""
        if data.empty or 'PolicyType' not in data.columns:
            return data

        mask = data['PolicyType'].fillna('').str.lower().str.contains(
            self.coverage_type, case=False, regex=False
        )
        return data[mask].copy()


class PolicyValueRangeSpecification(ISpecification):
    """Filter policies by property value range."""
    
    def __init__(self, min_value: float = None, max_value: float = None):
        """
        Args:
            min_value: Minimum property value (inclusive)
            max_value: Maximum property value (inclusive)
        """
        self.min_value = min_value
        self.max_value = max_value
    
    def is_satisfied_by(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return policies within value range."""
        if data.empty or 'property_value' not in data.columns:
            return data
        
        result = data.copy()
        
        if self.min_value is not None:
            result = result[result['property_value'] >= self.min_value]
        
        if self.max_value is not None:
            result = result[result['property_value'] <= self.max_value]
        
        return result


# Example usage factory methods
def unremediated_within_radius(lat: float, lon: float, radius: float = None) -> ISpecification:
    """
    Create specification for unremediated sites within radius.
    Default radius from settings.
    """
    radius = radius or settings.PROXIMITY_RADIUS_MILES
    
    geospatial = GeospatialSpecification(lat, lon, radius)
    unremediated = UnremediatedSpecification()
    
    return geospatial.and_spec(unremediated)


def sites_by_state_and_contaminant(state: str, contaminant: str) -> ISpecification:
    """Create specification for sites in a state with specific contaminant."""
    state_spec = StateSpecification(state)
    contaminant_spec = ContaminantSpecification(contaminant)
    
    return state_spec.and_spec(contaminant_spec)


# Policy factory methods

def policies_in_state(state: str) -> ISpecification:
    """Get all policies in a state."""
    return PolicyStateSpecification(state)


def policies_near_location(lat: float, lon: float, radius: float = 10) -> ISpecification:
    """Get policies within radius of a location."""
    return PolicyGeospatialSpecification(lat, lon, radius)


def policies_by_coverage_type(coverage_type: str) -> ISpecification:
    """Get policies by coverage type."""
    return PolicyCoverageTypeSpecification(coverage_type)


def high_value_policies(min_value: float = 1000000) -> ISpecification:
    """Get high-value policies (default: $1M+)."""
    return PolicyValueRangeSpecification(min_value=min_value)
