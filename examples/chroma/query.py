import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv

from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    Settings, VectorStoreIndex
)

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

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

# Conecta ao Chroma existente
chroma_client = chromadb.PersistentClient(
    path="../../chroma_db"
)

collection = chroma_client.get_collection(
    "documentos"
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# Carrega índice
index = VectorStoreIndex.from_vector_store(
    vector_store
)


query_engine = index.as_query_engine(
    similarity_top_k=3
)

# # pergunta = "Quando a disciplina será encerrada?"
# pergunta = "Quando a disciplina Engenharia de Software para Modelos de IA será encerrada?"
#
# resposta = query_engine.query(pergunta)
#
# print("\nResposta:")
# print(resposta)
#
# print("\nTRECHOS RECUPERADOS:")
#
# for node in resposta.source_nodes:
#     print("-" * 50)
#     print(node.text[:500])

while True:

    pergunta = input("\nPergunta: ")

    if pergunta.lower() == "sair":
        break

    response = query_engine.query(
        pergunta
    )

    print("\nResposta:")
    print(response)

    print("\nFontes:")

    for node in response.source_nodes:

        print("-" * 50)

        print(
            node.metadata.get("arquivo")
        )

        print(
            node.get_content()[:200]
        )