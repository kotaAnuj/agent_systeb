"""
semantic_memory.py

This module extends the base memory functionality by adding semantic memory
capabilities using open source libraries SentenceTransformers and FAISS.
"""

import numpy as np
import faiss
from memory import Memory
from sentence_transformers import SentenceTransformer

class SemanticMemory(Memory):
    def __init__(self, max_items: int = 10, enabled: bool = True):
        super().__init__(max_items, enabled)
        # Load a free, open source sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        self.embeddings = []  # List to store embeddings for each message
        self.index = faiss.IndexFlatL2(self.embedding_dim)  # FAISS index for similarity search

    def add(self, role: str, content: str) -> None:
        if not self.enabled:
            return
        # Add the message to the base memory
        super().add(role, content)
        # Compute embedding for the new content
        embedding = self.model.encode(content)
        self.embeddings.append(embedding)
        # Convert embedding to numpy array and add to FAISS index
        np_embedding = np.array([embedding]).astype('float32')
        self.index.add(np_embedding)
        # Maintain memory size; if exceeded, trim the oldest messages and rebuild the index
        if len(self.messages) > self.max_items:
            self.messages = self.messages[-self.max_items:]
            self.embeddings = self.embeddings[-self.max_items:]
            self.index.reset()
            if self.embeddings:
                embeddings_np = np.array(self.embeddings).astype('float32')
                self.index.add(embeddings_np)

    def retrieve_similar(self, query: str, top_k: int = 3) -> list:
        """
        Retrieve messages semantically similar to the query using FAISS.
        Returns a list of message dictionaries.
        """
        if not self.messages:
            return []
        query_embedding = self.model.encode(query)
        np_query = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(np_query, top_k)
        similar_messages = []
        for idx in indices[0]:
            if idx < len(self.messages):
                similar_messages.append(self.messages[idx])
        return similar_messages
