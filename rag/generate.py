"""Etapa 4: montar o prompt com o contexto recuperado e chamar o LLM."""
import os

SYSTEM = (
    "Você é um assistente de segurança da informação. Responda SOMENTE com base nos "
    "trechos de contexto fornecidos. Cite as fontes no formato [1], [2]. Se o contexto "
    "não tiver a resposta, diga que não encontrou nas fontes. Responda no idioma da pergunta."
)


def build_prompt(question: str, hits) -> str:
    context = "\n\n".join(
        f"[{i}] ({c.source} | {c.heading})\n{c.text}" for i, (c, _) in enumerate(hits, 1)
    )
    return f"Contexto:\n{context}\n\nPergunta: {question}"


def answer(question: str, hits) -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:  # modo sem LLM: mostra os trechos recuperados (bom para depurar a busca)
        return "(Sem ANTHROPIC_API_KEY: mostrando apenas os trechos recuperados)\n\n" + "\n\n".join(
            f"[{i}] {c.source} | {c.heading}" for i, (c, _) in enumerate(hits, 1)
        )
    import anthropic

    client = anthropic.Anthropic(api_key=key)
    resp = client.messages.create(
        model=os.getenv("RAG_MODEL", "claude-sonnet-4-6"),
        max_tokens=600,
        system=SYSTEM,
        messages=[{"role": "user", "content": build_prompt(question, hits)}],
    )
    return resp.content[0].text
