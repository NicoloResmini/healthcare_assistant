import nltk
from nltk.tokenize import sent_tokenize

# Make sure to have downloaded this
nltk.download('punkt')

class TextProcessor:
    """
    Splits text into chunks of a specified max number of characters
    """
    def __init__(self, max_chunk_chars: int = 1000):
        self.max_chunk_chars = max_chunk_chars

    def chunk_text(self, text: str) -> list[str]:
        sentences = sent_tokenize(text)
        chunks = []
        current = []
        current_len = 0
        for sent in sentences:
            if current_len + len(sent) <= self.max_chunk_chars:
                current.append(sent)
                current_len += len(sent)
            else:
                # finalize chunk
                chunks.append(" ".join(current))
                current = [sent]
                current_len = len(sent)
        if current:
            chunks.append(" ".join(current))
        return chunks