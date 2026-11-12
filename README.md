# SecRAG: assistente RAG para frameworks de segurança

Responde perguntas sobre NIST CSF 2.0, CIS Controls v8 e OWASP Top 10, citando o trecho de origem.

## Arquitetura
documentos .md -> chunking (um chunk por seção/controle) -> embeddings -> busca por similaridade (top-k) -> prompt com contexto -> LLM -> resposta com citações

## Como rodar
    python -m venv .venv
    .venv\Scripts\Activate.ps1         # Windows (no Linux/Mac: source .venv/bin/activate)
    pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "..."     # opcional; sem ela o app mostra só os trechos recuperados
    streamlit run app.py

Com Docker: `docker build -t secrag .` e `docker run -p 8501:8501 -e ANTHROPIC_API_KEY secrag`.

## Avaliação da recuperação
    python -m eval.run_eval --embedder hybrid --k 3     # também: st, tfidf

Três estratégias comparadas em 20 perguntas: 12 usadas durante o desenvolvimento e 8 parafraseadas, escritas depois e não usadas para ajustes.

| Embedder | hit@3 (20) | MRR (20) | Acertos nas 8 novas |
|---|---|---|---|
| tfidf (lexical) | 0,80 | 0,71 | 4/8 |
| st (semântico, MiniLM multilíngue) | 0,75 | 0,72 | 4/8 |
| **hybrid** (alpha = 0,5) | **0,95** | **0,82** | **7/8** |

**O que aprendi**
- Chunks que agrupavam 6 controles diluíam o significado de cada um; separar um controle por seção corrigiu uma falha da busca semântica.
- O `TfidfVectorizer` descarta tokens de 1 caractere por padrão, o que escondia o "8" de "controle 8". Corrigido com `token_pattern`.
- Embeddings semânticos erram em perguntas por número ou sigla; o TF-IDF erra em paráfrases. Os erros são em perguntas diferentes, e a combinação (busca híbrida) compensa os dois.

**Limitações**
- Conjunto pequeno: cada pergunta vale 5 pontos percentuais, e o alpha não foi otimizado.
- Uma pergunta é ambígua ("funcionários caindo em golpes" aceita só o Controle 14 do CIS, mas o Controle 9 também seria razoável) e todos os métodos erram nela. Mantive o rótulo original.
- Avalio apenas a recuperação, não a qualidade da resposta final do LLM.

## Testes e CI
`pytest` roda localmente e no GitHub Actions, junto com a avaliação TF-IDF (falha se hit@3 < 0,8). O CI não baixa o modelo semântico.

## Aviso
Os arquivos em `data/docs` são resumos escritos para este projeto, não os documentos oficiais. Para uso real, substitua pelos textos oficiais.
