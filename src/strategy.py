"""
Strategy Pattern: Data Backend Interface
Enables swapping between CSV (Phase 1) and Vector Store (Phase 2) backends.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path
import config.settings as settings


class IDataBackend(ABC):
    """Interface for data backend strategies."""
    
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Load SuperFund site data (deprecated, use load_superfund_data)."""
        pass
    
    @abstractmethod
    def load_superfund_data(self) -> pd.DataFrame:
        """Load SuperFund site data."""
        pass
    
    @abstractmethod
    def load_policy_data(self) -> pd.DataFrame:
        """Load insurance policy data."""
        pass
    
    @abstractmethod
    def query(self, specification) -> pd.DataFrame:
        """Query data using a Specification pattern (deprecated, use query_superfund)."""
        pass
    
    @abstractmethod
    def query_superfund(self, specification) -> pd.DataFrame:
        """Query SuperFund data using a Specification pattern."""
        pass
    
    @abstractmethod
    def query_policies(self, specification) -> pd.DataFrame:
        """Query policy data using a Specification pattern."""
        pass
    
    @abstractmethod
    def get_all_sites(self) -> pd.DataFrame:
        """Retrieve all SuperFund sites."""
        pass
    
    @abstractmethod
    def get_all_policies(self) -> pd.DataFrame:
        """Retrieve all policies."""
        pass


class CSVBackend(IDataBackend):
    """
    CSV-based backend for Phase 1.
    Simple file-based storage and filtering.
    """
    
    def __init__(self, superfund_csv: str = None, policy_csv: str = None):
        self.superfund_csv = superfund_csv or settings.SUPERFUND_DATA_FILE
        self.policy_csv = policy_csv or getattr(settings, 'POLICY_DATA_FILE', './data/raw/policies.csv')
        self._superfund_data: pd.DataFrame = None
        self._policy_data: pd.DataFrame = None
    
    def load_data(self) -> pd.DataFrame:
        """Load SuperFund data from CSV file (deprecated, use load_superfund_data)."""
        return self.load_superfund_data()
    
    def load_superfund_data(self) -> pd.DataFrame:
        """Load SuperFund site data from CSV."""
        if self._superfund_data is None:
            try:
                self._superfund_data = pd.read_csv(self.superfund_csv)
                print(f"✓ Loaded {len(self._superfund_data)} SuperFund sites from CSV")
            except FileNotFoundError:
                print(f"⚠ CSV file not found: {self.superfund_csv}")
                # Return empty DataFrame with expected schema
                self._superfund_data = pd.DataFrame(columns=[
                    "Id","SiteName","PollutionClass","PollutionType","RemediationStatus","RemediationStart","RemediationFinish","AddressLine","City","StateProvince","PostalCode","Country","Latitude","Longitude"
                ])
        return self._superfund_data
    
    def load_policy_data(self) -> pd.DataFrame:
        """Load insurance policy data from CSV."""
        if self._policy_data is None:
            try:
                self._policy_data = pd.read_csv(self.policy_csv)
                print(f"✓ Loaded {len(self._policy_data)} insurance policies from CSV")
            except FileNotFoundError:
                print(f"⚠ Policy CSV file not found: {self.policy_csv}")
                # Return empty DataFrame with expected schema
                self._policy_data = pd.DataFrame(columns=[
                    "Id","PolicyNumber","PolicyType","EffectiveDate","ExpirationDate","Status","EndorsementAmount","Address","City","State","PostalCode","Country","Latitude","Longitude"
                ])
        return self._policy_data
    
    def query(self, specification) -> pd.DataFrame:
        """Apply Specification pattern to filter SuperFund data (deprecated, use query_superfund)."""
        return self.query_superfund(specification)
    
    def query_superfund(self, specification) -> pd.DataFrame:
        """Query SuperFund data using Specification pattern."""
        data = self.load_superfund_data()
        return specification.is_satisfied_by(data)
    
    def query_policies(self, specification) -> pd.DataFrame:
        """Query policy data using Specification pattern."""
        data = self.load_policy_data()
        return specification.is_satisfied_by(data)
    
    def get_all_sites(self) -> pd.DataFrame:
        """Return all SuperFund sites."""
        return self.load_superfund_data()
    
    def get_all_policies(self) -> pd.DataFrame:
        """Return all policies."""
        return self.load_policy_data()


class VectorStoreBackend(IDataBackend):
    """
    Vector store backend for Phase 2.
    Enables semantic search and RAG capabilities.
    """
    
    def __init__(self, superfund_collection: str = "superfund_sites", policy_collection: str = "policies"):
        self.superfund_collection = superfund_collection
        self.policy_collection = policy_collection
        self._client = None
        self._superfund_collection = None
        self._policy_collection = None
        self._superfund_metadata_cache: pd.DataFrame = None
        self._policy_metadata_cache: pd.DataFrame = None
    
    def _init_client(self):
        """Initialize ChromaDB client."""
        if self._client is None:
            try:
                import chromadb
                self._client = chromadb.PersistentClient(
                    path=str(settings.EMBEDDINGS_PATH)
                )
                self._superfund_collection = self._client.get_or_create_collection(
                    name=self.superfund_collection
                )
                self._policy_collection = self._client.get_or_create_collection(
                    name=self.policy_collection
                )
                print(f"✓ Connected to vector stores: {self.superfund_collection}, {self.policy_collection}")
            except ImportError:
                print("⚠ ChromaDB not installed. Install with: pip install chromadb")
                raise
    
    def load_data(self) -> pd.DataFrame:
        """Load SuperFund metadata from vector store (deprecated, use load_superfund_data)."""
        return self.load_superfund_data()
    
    def load_superfund_data(self) -> pd.DataFrame:
        """Load SuperFund metadata from vector store."""
        if self._superfund_metadata_cache is None:
            self._init_client()
            
            # Get all documents with metadata
            results = self._superfund_collection.get(include=["metadatas"])
            
            if results['metadatas']:
                self._superfund_metadata_cache = pd.DataFrame(results['metadatas'])
                print(f"✓ Loaded {len(self._superfund_metadata_cache)} sites from vector store")
            else:
                print("⚠ SuperFund vector store is empty")
                self._superfund_metadata_cache = pd.DataFrame()
        
        return self._superfund_metadata_cache
    
    def load_policy_data(self) -> pd.DataFrame:
        """Load policy metadata from vector store."""
        if self._policy_metadata_cache is None:
            self._init_client()
            
            # Get all documents with metadata
            results = self._policy_collection.get(include=["metadatas"])
            
            if results['metadatas']:
                self._policy_metadata_cache = pd.DataFrame(results['metadatas'])
                print(f"✓ Loaded {len(self._policy_metadata_cache)} policies from vector store")
            else:
                print("⚠ Policy vector store is empty")
                self._policy_metadata_cache = pd.DataFrame()
        
        return self._policy_metadata_cache
    
    def query(self, specification) -> pd.DataFrame:
        """Apply specification to SuperFund vector store metadata (deprecated, use query_superfund)."""
        return self.query_superfund(specification)
    
    def query_superfund(self, specification) -> pd.DataFrame:
        """Apply specification to SuperFund vector store metadata."""
        data = self.load_superfund_data()
        return specification.is_satisfied_by(data)
    
    def query_policies(self, specification) -> pd.DataFrame:
        """Apply specification to policy vector store metadata."""
        data = self.load_policy_data()
        return specification.is_satisfied_by(data)
    
    def get_all_sites(self) -> pd.DataFrame:
        """Return all SuperFund sites from vector store."""
        return self.load_superfund_data()
    
    def get_all_policies(self) -> pd.DataFrame:
        """Return all policies from vector store."""
        return self.load_policy_data()
    
    def semantic_search_superfund(self, query_text: str, n_results: int = 10) -> pd.DataFrame:
        """Perform semantic search on SuperFund site descriptions."""
        self._init_client()
        
        results = self._superfund_collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=["metadatas", "distances"]
        )
        
        if results['metadatas'][0]:
            df = pd.DataFrame(results['metadatas'][0])
            df['similarity_score'] = results['distances'][0]
            return df
        
        return pd.DataFrame()
    
    def semantic_search_policies(self, query_text: str, n_results: int = 10) -> pd.DataFrame:
        """Perform semantic search on policy data."""
        self._init_client()
        
        results = self._policy_collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=["metadatas", "distances"]
        )
        
        if results['metadatas'][0]:
            df = pd.DataFrame(results['metadatas'][0])
            df['similarity_score'] = results['distances'][0]
            return df
        
        return pd.DataFrame()


class BackendFactory:
    """Factory for creating data backend instances."""
    
    @staticmethod
    def create_backend(backend_type: str = "csv") -> IDataBackend:
        """
        Create a data backend instance.
        
        Args:
            backend_type: 'csv' or 'vector_store'
        
        Returns:
            IDataBackend implementation
        """
        if backend_type.lower() == "csv":
            return CSVBackend()
        elif backend_type.lower() == "vector_store":
            return VectorStoreBackend()
        else:
            raise ValueError(f"Unknown backend type: {backend_type}")


# Global backend instance (can be swapped at runtime)
_current_backend: IDataBackend = None


def get_backend() -> IDataBackend:
    """Get current backend instance (singleton pattern)."""
    global _current_backend
    if _current_backend is None:
        _current_backend = BackendFactory.create_backend("csv")  # Default to CSV
    return _current_backend


def set_backend(backend: IDataBackend):
    """Change the current backend."""
    global _current_backend
    _current_backend = backend
    print(f"✓ Backend switched to: {backend.__class__.__name__}")
