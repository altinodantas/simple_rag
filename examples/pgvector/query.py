import os

from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings,
)

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY_OPENAI")

Settings.llm = OpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
)

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY,
)

vector_store = PGVectorStore.from_params(
    database=os.getenv("POSTGRES_DB"),
    host=os.getenv("POSTGRES_HOST"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=int(os.getenv("POSTGRES_PORT")),
    user=os.getenv("POSTGRES_USER"),
    table_name="documents",
    embed_dim=1536,
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)

query_engine = index.as_query_engine(
    similarity_top_k=3
)

while True:

    pergunta = input("\nPergunta: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        break

    response = query_engine.query(pergunta)

    print("\nResposta:")
    print(response.response)

    print("\nFontes:")

    for node in response.source_nodes:
        print("-" * 80)

        arquivo = node.metadata.get(
            "file_name",
            "Arquivo desconhecido"
        )

        print(f"Arquivo: {arquivo}")

        print(
            node.text[:300]
            .replace("\n", " ")
        )