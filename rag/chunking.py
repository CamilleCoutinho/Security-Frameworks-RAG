"""Etapa 1: carregar documentos e quebrar em pedaços (chunks) com metadados."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    text: str
    source: str   # nome do arquivo, usado na citação
    heading: str  # seção onde o trecho está


def split_markdown(text: str, source: str, max_chars: int = 700) -> list[Chunk]:
    """Divide por títulos (#, ##) e depois empacota parágrafos até max_chars."""
    sections, heading, buf = [], source, []
    for line in text.splitlines():
        if line.startswith("#"):
            if buf:
                sections.append((heading, "\n".join(buf).strip()))
                buf = []
            heading = line.lstrip("#").strip()
        else:
            buf.append(line)
    if buf:
        sections.append((heading, "\n".join(buf).strip()))

    chunks = []
    for heading, body in sections:
        current = ""
        for para in (p.strip() for p in body.split("\n\n") if p.strip()):
            if current and len(current) + len(para) > max_chars:
                chunks.append(Chunk(f"{heading}\n{current}", source, heading))
                current = ""
            current = f"{current}\n\n{para}".strip()
        if current:
            # O título entra no texto do chunk: ajuda a busca a achar "A03 Injection".
            chunks.append(Chunk(f"{heading}\n{current}", source, heading))
    return chunks


def load_corpus(folder: str = "data/docs") -> list[Chunk]:
    chunks = []
    for path in sorted(Path(folder).glob("*.md")):
        chunks += split_markdown(path.read_text(encoding="utf-8"), path.name)
    return chunks
