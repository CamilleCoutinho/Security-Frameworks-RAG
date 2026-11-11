"""Etapa 2: transformar texto em vetores. Dois "motores" com a mesma interface."""
import numpy as np


class SentenceTransformerEmbedder:
    """Embeddings semânticos (entende sinônimos e português). Usado em produção."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        from sentence_transformers import SentenceTransformer  # import tardio: é pesado

        self.model = SentenceTransformer(model_name)

    def fit(self, texts):  # nada a treinar
        pass

    def encode(self, texts) -> np.ndarray:
        return np.asarray(self.model.encode(list(texts), normalize_embeddings=True))


class TfidfEmbedder:
    """Baseline lexical, leve e sem download. Serve para testes e CI."""

    def __init__(self):
        from sklearn.feature_extraction.text import TfidfVectorizer

        self.vec = TfidfVectorizer(strip_accents="unicode", lowercase=True, sublinear_tf=True)

    def fit(self, texts):
        self.vec.fit(list(texts))

    def encode(self, texts) -> np.ndarray:
        return self.vec.transform(list(texts)).toarray()  # já vem normalizado (L2)


def get_embedder(name: str):
    return TfidfEmbedder() if name == "tfidf" else SentenceTransformerEmbedder()
