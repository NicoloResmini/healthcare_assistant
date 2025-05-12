from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class Generator:
    """
    Generation component for RAG, using sequence-to-sequence model
    """
    def __init__(
        self,
        model_name: str = "google/flan-t5-base",
        device: str = None,
        max_length: int = 256
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
        self.max_length = max_length

    def generate(self, question: str, context_docs: list[str]) -> str:
        # Prepare prompt by concatenating documents and question
        context = "\n".join(context_docs)
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        ).to(self.device)

        out = self.model.generate(
            **inputs,
            max_length=self.max_length,
            num_beams=4,
            early_stopping=True
        )
        answer = self.tokenizer.decode(out[0], skip_special_tokens=True)
        return answer