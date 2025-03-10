"""
rag.py

This module implements Retrieval-Augmented Generation (RAG) capabilities.
It integrates document processing and retrieval using SentenceTransformers for
embeddings and FAISS for similarity search.
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List

class RetrievalAugmentedGeneration:
    def __init__(self):
        # Load an open source SentenceTransformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        self.documents = []  # List of documents
        self.doc_embeddings = []  # List of document embeddings
        self.index = faiss.IndexFlatL2(self.embedding_dim)  # FAISS index for document embeddings

    def index_documents(self, documents: List[str]) -> None:
        """
        Process and index a list of documents.
        """
        self.documents = documents
        self.doc_embeddings = [self.model.encode(doc) for doc in documents]
        embeddings_np = np.array(self.doc_embeddings).astype('float32')
        self.index = faiss.IndexFlatL2(self.embedding_dim)  # Reset index
        self.index.add(embeddings_np)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve the top_k documents relevant to the query.
        """
        query_embedding = self.model.encode(query)
        np_query = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(np_query, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])
        return results
