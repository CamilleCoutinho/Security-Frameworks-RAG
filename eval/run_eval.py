import argparse
import json
import sys

from rag.chunking import load_corpus
from rag.embedders import get_embedder
from rag.retriever import Retriever


def evaluate(embedder_name: str, k: int):
    retriever = Retriever(load_corpus(), get_embedder(embedder_name))
    items = json.load(open("eval/questions.json", encoding="utf-8"))
    hits_at_k, rr, misses = 0, 0.0, []
    for it in items:
        results = retriever.search(it["q"], k)
        rank = next(
            (i for i, (c, _) in enumerate(results, 1)
             if c.source == it["source"] and it["keyword"].lower() in c.text.lower()),
            None,
        )
        if rank:
            hits_at_k += 1
            rr += 1 / rank
        else:
            misses.append(it["q"])
    n = len(items)
    return hits_at_k / n, rr / n, misses


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--embedder", default="hybrid", choices=["st", "tfidf", "hybrid"])
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--min-hit", type=float, default=0.0)
    a = ap.parse_args()
    hit, mrr, misses = evaluate(a.embedder, a.k)
    print(f"embedder={a.embedder} k={a.k} hit@k={hit:.2f} MRR={mrr:.2f}")
    for m in misses:
        print("  MISS:", m)
    sys.exit(0 if hit >= a.min_hit else 1)