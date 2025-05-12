import pytest
from rag.processor import TextProcessor
from rag.retriever import Retriever

@pytest.fixture(scope='module')
def processor():
    return TextProcessor(max_chunk_chars=50)

@pytest.fixture(scope='module')
def retriever(tmp_path):
    # Create a temporary index file
    idx_file = str(tmp_path / "test.idx")
    ret = Retriever(index_path=idx_file, max_chunk_chars=50)
    # Index test documents
    docs = ["This is text document one", "Second doc with different text."]
    ret.index_documents(docs)
    return ret


def test_chunking(processor):
    text = "".join(["A phrase. " for _ in range(20)])
    chunks = processor.chunk_text(text)
    assert all(len(c) <= 50 for c in chunks)
    assert len(chunks) > 1


def test_retrieval(retriever):
    query = "test document"
    results = retriever.retrieve(query, top_k=2)
    assert isinstance(results, list)
    assert any("test document one" in r for r in results)