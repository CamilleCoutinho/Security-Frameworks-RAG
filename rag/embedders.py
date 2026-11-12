
import numpy as np


class SentenceTransformerEmbedder:

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        from sentence_transformers import SentenceTransformer  # import tardio: é pesado

        self.model = SentenceTransformer(model_name)

    def fit(self, texts):  # nada a treinar
        pass

    def encode(self, texts) -> np.ndarray:
        return np.asarray(self.model.encode(list(texts), normalize_embeddings=True))


class TfidfEmbedder:

    def __init__(self):
        from sklearn.feature_extraction.text import TfidfVectorizer

        self.vec = TfidfVectorizer(
            strip_accents="unicode", lowercase=True, sublinear_tf=True,
            token_pattern=r"(?u)\b\w+\b",  # mantém tokens de 1 caractere, como o "8" de "controle 8"
        )

    def fit(self, texts):
        self.vec.fit(list(texts))

    def encode(self, texts) -> np.ndarray:
        return self.vec.transform(list(texts)).toarray()  # já vem normalizado (L2)


class HybridEmbedder:
    def __init__(self, alpha: float = 0.5, dense=None, sparse=None):
        self.alpha = alpha
        self.dense = dense or SentenceTransformerEmbedder()
        self.sparse = sparse or TfidfEmbedder()

    def fit(self, texts):
        self.dense.fit(texts)
        self.sparse.fit(texts)

    def encode(self, texts) -> np.ndarray:
        d = self.dense.encode(texts) * np.sqrt(self.alpha)
        s = self.sparse.encode(texts) * np.sqrt(1 - self.alpha)
        return np.hstack([d, s])


def get_embedder(name: str):
    if name == "tfidf":
        return TfidfEmbedder()
    if name == "hybrid":
        return HybridEmbedder()
    return SentenceTransformerEmbedder()
