from typing import List
from transformers import AutoTokenizer, AutoModel
import torch

class Embedder:
    """
    Class for embedding texts using a transformer model
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def embed_texts(self, texts: List[str]) -> torch.Tensor:
        """
        Returns a tensor [len(texts), dim_embedding]
        """
        # Tokenization with padding and truncation
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)

        # Model inference
        with torch.no_grad():
            output = self.model(**encoded, return_dict=True)
            # Mean pooling on the tokens
            embeddings = (
                output.last_hidden_state
                * encoded.attention_mask.unsqueeze(-1)
            ).sum(dim=1) / encoded.attention_mask.sum(dim=1, keepdim=True)
        return embeddings.cpu()
