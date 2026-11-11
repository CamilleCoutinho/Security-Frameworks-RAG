"""Etapa 3: busca por similaridade. Com vetores normalizados, produto escalar = cosseno."""
import numpy as np

from .chunking import Chunk


class Retriever:
    def __init__(self, chunks: list[Chunk], embedder):
        self.chunks = chunks
        self.embedder = embedder
        texts = [c.text for c in chunks]
        embedder.fit(texts)
        self.matrix = embedder.encode(texts)  # shape: (n_chunks, dim)

    def search(self, query: str, k: int = 4) -> list[tuple[Chunk, float]]:
        q = self.embedder.encode([query])[0]
        scores = self.matrix @ q
        top = np.argsort(-scores)[:k]
        return [(self.chunks[i], float(scores[i])) for i in top]
