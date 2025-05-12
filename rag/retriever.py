from vector_db.embeddings import Embedder
from vector_db.retrieval import FAISSVectorStore
from rag.processor import TextProcessor
from typing import List

class Retriever:
    """
    Component for retrieving documents.
    """
    def __init__(
        self,
        embedder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        index_path: str = "data/faiss_index.idx",
        max_chunk_chars: int = 1000
    ):
        self.processor = TextProcessor(max_chunk_chars=max_chunk_chars)
        self.embedder = Embedder(model_name=embedder_model)
        # embedding dimension known for the model
        dim = self.embedder.embed_texts(["test"]).shape[1]
        self.store = FAISSVectorStore(
            embedder=self.embedder,
            dim=dim,
            index_path=index_path
        )

    def index_documents(self, docs: List[str]):
        """
        Chunk and index a list of documents
        """
        chunks = []
        for doc in docs:
            chunks.extend(self.processor.chunk_text(doc))
        self.store.add_documents(chunks)

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """
        Returns the top_k most relevant chunks for a gievn query
        """
        results = self.store.search(query, top_k=top_k)
        # results is list of (chunk, score)
        return [chunk for chunk, _ in results]