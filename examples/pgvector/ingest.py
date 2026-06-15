import os

from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
)

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY_OPENAI")

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

documents = SimpleDirectoryReader(
    input_dir="../../documents"
).load_data()

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

print(f"{len(documents)} documentos indexados com sucesso.")