# Projeto RAG com LlamaIndex e ChromaDB

Este projeto implementa um sistema de Geração Aumentada por Recuperação (RAG) utilizando LlamaIndex para indexação de documentos e diferentes opções de armazenamento vetorial: **armazenamento local padrão**, **ChromaDB** e **PostgreSQL com PgVector**.

## Estrutura do Projeto

```
examples/
  local/
    ingest.py
    query.py
  chroma/
    ingest.py
    query.py
  pgvector/
    ingest.py
    query.py
chroma_db/
  chroma.sqlite3
  4c389f2e-a604-4614-8e7e-7604f62f4b46/
documents/
storage/
  default__vector_store.json
  docstore.json
  graph_store.json
  image__vector_store.json
  index_store.json
```
## Configuração

Para configurar o ambiente, siga os passos abaixo:

1. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Copie o arquivo de exemplo `.env.example` para `.env` e preencha suas credenciais:
   ```bash
   cp .env.example .env
   ```

3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o PostgreSQL e a extensão `pgvector` para o exemplo `pgvector`:
   - Crie um banco PostgreSQL
   - Instale a extensão `pgvector`
   - Ajuste a variável `DATABASE_URL` no `.env`

## Uso

### Estrutura de exemplos

- `examples/local/` — armazenamento local padrão do LlamaIndex
- `examples/chroma/` — ChromaDB como backend vetorial
- `examples/pgvector/` — PostgreSQL com `pgvector`

### 1. Ingestão de documentos

Coloque seus documentos PDF no diretório `documents/`. Cada exemplo possui seu próprio script de ingestão.

- Local:
  ```bash
  python examples/local/ingest.py
  ```
- ChromaDB:
  ```bash
  python examples/chroma/ingest.py
  ```
- PgVector:
  ```bash
  python examples/pgvector/ingest.py
  ```

### 2. Consulta

Após a ingestão, rode o script de consulta correspondente.

- Local:
  ```bash
  python examples/local/query.py
  ```
- ChromaDB:
  ```bash
  python examples/chroma/query.py
  ```
- PgVector:
  ```bash
  python examples/pgvector/query.py
  ```

### 3. Perguntas comuns

- Use `sair` no prompt de `examples/chroma/query.py` e `examples/pgvector/query.py` para encerrar.
- Para alterar o modelo, edite o `model` em `Settings.llm` / `Settings.embed_model` nos scripts.
