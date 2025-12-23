"""
memory_stream.py
Handling ChromaDB interaction and retrieval logic.
"""
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from datetime import datetime
from typing import List, Optional
import uuid

from models import Memory, ScoredMemory
from utils import get_hash, cosine_similarity, normalize_score
import scoring
import config

class MemoryStream:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.client = chromadb.PersistentClient(path=config.CHROMA_PERSIST_DIR)
        
        # Use default embedding function (all-MiniLM-L6-v2) for MVP simplicity
        # If OpenAI key is available, we could switch to OpenAIEmbeddingFunction
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        collection_name = f"memories_{agent_name}"
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def add_memory(self, memory: Memory):
        """
        Add a memory to the ChromaDB collection.
        Enforces LRU cap (Neon Society architecture).
        """
        # Check current count
        count = self.collection.count()
        
        # If at capacity, remove oldest memory (LRU)
        if count >= config.MAX_MEMORIES:
            # Get all memories sorted by creation time
            all_results = self.collection.get(
                include=['metadatas']
            )
            
            if all_results['ids']:
                # Find oldest memory ID
                oldest_id = None
                oldest_time = None
                
                for i, meta in enumerate(all_results['metadatas']):
                    created_at = datetime.fromisoformat(str(meta["created_at"]))
                    if oldest_time is None or created_at < oldest_time:
                        oldest_time = created_at
                        oldest_id = all_results['ids'][i]
                
                # Delete oldest
                if oldest_id:
                    self.collection.delete(ids=[oldest_id])
        
        # Prepare metadata
        # Chroma metadata values must be int, float, str, or bool. No lists/dicts.
        metadata = {
            "type": memory.memory_type,
            "created_at": memory.created_at.isoformat(),
            "importance": memory.importance,
            "source": memory.source or "",
            "tags": ",".join(memory.tags) if memory.tags else ""
        }
        
        self.collection.add(
            documents=[memory.content],
            metadatas=[metadata],
            ids=[memory.id]
        )

    def retrieve(self, query: str, k: int = config.K_FINAL_RETRIEVAL) -> List[ScoredMemory]:
        """
        Retrieve top-k relevant memories using 2-stage pipeline.
        1. Vector Search (Top-N)
        2. Re-ranking (Scoring)
        """
        top_n = config.TOP_N_RETRIEVAL
        
        # 1. Vector Search
        results = self.collection.query(
            query_texts=[query],
            n_results=top_n
            # include=['documents', 'metadatas', 'distances', 'embeddings'] # default includes these except embeddings
        )
        
        if not results['ids'] or not results['ids'][0]:
            return []
            
        # Parse results into ScoredMemory candidates
        candidates = []
        ids = results['ids'][0]
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0] # Cosine distance
        
        current_time = datetime.now()
        
        for i in range(len(ids)):
            meta = metadatas[i]
            doc = documents[i]
            dist = distances[i]
            
            # Reconstruct Memory object
            created_at = datetime.fromisoformat(str(meta["created_at"]))
            memory = Memory(
                id=ids[i],
                content=doc,
                memory_type=str(meta["type"]),
                created_at=created_at,
                importance=int(meta["importance"]),
                source=str(meta["source"]),
                tags=str(meta["tags"]).split(",") if meta["tags"] else []
            )
            
            # Calculate Scores
            # Chroma returns distance. Similarity = 1 - distance (approx for cosine)
            similarity = 1.0 - dist
            
            recency = scoring.calculate_recency_score(
                created_at, 
                current_time, 
                decay_factor=config.DECAY_FACTOR
            )
            
            importance_score = calculate_importance_norm(memory.importance)
            
            final_score = scoring.calculate_final_score(
                similarity,
                recency,
                memory.importance,
                w_sim=config.WEIGHT_SIMILARITY,
                w_rec=config.WEIGHT_RECENCY,
                w_imp=config.WEIGHT_IMPORTANCE
            )
            
            candidates.append(ScoredMemory(
                memory=memory,
                similarity_score=similarity,
                recency_score=recency,
                importance_score=importance_score,
                final_score=final_score
            ))
            
        # 2. Sort by Final Score
        candidates.sort(key=lambda x: x.final_score, reverse=True)
        
        return candidates[:k]

def calculate_importance_norm(importance: int) -> float:
    return (importance - 1) / 9.0
