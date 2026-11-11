from rag.chunking import load_corpus, split_markdown
from rag.embedders import TfidfEmbedder
from rag.retriever import Retriever


def test_chunks_keep_metadata():
    chunks = split_markdown("# T\n\n## A03 Injection\nTexto sobre SQL.", "x.md")
    assert chunks[0].source == "x.md" and chunks[0].heading == "A03 Injection"


def test_retrieval_finds_right_source():
    r = Retriever(load_corpus(), TfidfEmbedder())
    top, _ = r.search("Como mitigar SQL injection?", 1)[0]
    assert top.source == "owasp_top10_2021.md"
