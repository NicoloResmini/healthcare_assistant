from typing import List
from vector_db.embeddings import Embedder
import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

class DoctorRecommender:
    """
    Recommends doctors based on the similarity between the problem description and specialization.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedder = Embedder(model_name=model_name)

    def rank(self, doctors: List[dict], problem: str) -> List[dict]:
        """
        :param doctors: list of dicts with keys 'id','first_name','last_name','specialization', ...
        :param problem: description of the patient's problem
        :return: doctors sorted by descending score
        """
        # Generate embedding for problem
        prob_emb = self.embedder.embed_texts([problem]).numpy()[0]

        # Calculate embedding for each specialization and similarity
        scores = []
        for doc in doctors:
            spec = doc.get("specialization", "")
            spec_emb = self.embedder.embed_texts([spec]).numpy()[0]
            score = cosine_similarity(prob_emb, spec_emb)
            scores.append((score, doc))

        # Order by descending score
        ranked = [doc for score, doc in sorted(scores, key=lambda x: x[0], reverse=True)]
        return ranked