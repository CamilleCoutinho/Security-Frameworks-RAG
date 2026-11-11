# SecRAG: assistente RAG para frameworks de segurança

Responde perguntas sobre NIST CSF 2.0, CIS Controls v8 e OWASP Top 10 citando o trecho de origem.

## Arquitetura
documentos .md -> chunking -> embeddings -> busca por similaridade (top-k) -> prompt com contexto -> LLM -> resposta com citações

## Como rodar
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=...      # opcional; sem ela o app mostra só os trechos
    streamlit run app.py
    # ou: docker build -t secrag . && docker run -p 8501:8501 -e ANTHROPIC_API_KEY secrag

## Avaliação
    python -m eval.run_eval --embedder st --k 3      # semântico
    python -m eval.run_eval --embedder tfidf --k 3   # baseline lexical

| Embedder | hit@3 | MRR |
|---|---|---|
| tfidf | 1.00 | 0.90 |
| st (preencha após rodar) | | |

## Aviso
Os arquivos em data/docs são resumos de exemplo. Substitua/adicione os documentos oficiais.
