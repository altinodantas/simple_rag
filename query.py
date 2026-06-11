import os
from pathlib import Path

from dotenv import load_dotenv

from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    Settings
)

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv()

Settings.llm = OpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    api_key=os.getenv("API_KEY_OPENAI")
)

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_key=os.getenv("API_KEY_OPENAI")
)

storage_context = StorageContext.from_defaults(
    persist_dir="./storage"
)

index = load_index_from_storage(
    storage_context
)


query_engine = index.as_query_engine(
    similarity_top_k=3
)

# pergunta = "Quando a disciplina será encerrada?"
pergunta = "Quando a disciplina Engenharia de Software para Modelos de IA será encerrada?"

resposta = query_engine.query(pergunta)

print("\nResposta:")
print(resposta)

print("\nTRECHOS RECUPERADOS:")

for node in resposta.source_nodes:
    print("-" * 50)
    print(node.text[:500])
