"""RAG retriever contracts and adapters."""

from rag.azure_search import AzureSearchRetriever, build_azure_search_retriever
from rag.base import Retriever

__all__ = ["AzureSearchRetriever", "Retriever", "build_azure_search_retriever"]
