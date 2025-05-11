import faiss
import numpy as np
from typing import List, Tuple
from .embeddings import Embedder

class FAISSVectorStore:
    """
    Wrapper for FAISS: indexing and semantic search.
    """
    def __init__(self, embedder: Embedder, dim: int = 384, index_path: str = None):
        """
        :param embedder: instance of Embedder
        :param dim: dimension of the embeddings (depends on the model)
        :param index_path: if provided, load/save the index here
        """
        self.embedder = embedder
        self.dim = dim
        self.index_path = index_path
        # Use IndexFlatIP for cosine similarity (we will normalize first)
        self.index = faiss.IndexFlatIP(dim)
        self.id_to_doc = {}     # map internal id -> textual document
        self.next_id = 0

        if index_path:
            try:
                self.index = faiss.read_index(index_path)
                # Note: you should also reconstruct id_to_doc from an external file
            except Exception:
                pass

    def add_documents(self, docs: List[str]):
        """
        Adds a list of documents to the vector store.
        """
        embs = self.embedder.embed_texts(docs).numpy()
        # Normalize in-place for IP = cosine
        faiss.normalize_L2(embs)
        n = embs.shape[0]
        ids = np.arange(self.next_id, self.next_id + n)
        self.index.add_with_ids(embs, ids)
        for i, doc in zip(ids, docs):
            self.id_to_doc[int(i)] = doc
        self.next_id += n

        if self.index_path:
            faiss.write_index(self.index, self.index_path)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Returns the top_k most similar documents to the query.
        """
        q_emb = self.embedder.embed_texts([query]).numpy()
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            results.append((self.id_to_doc[int(idx)], float(score)))
        return results