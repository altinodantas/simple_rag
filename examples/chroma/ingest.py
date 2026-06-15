import os
from pathlib import Path
from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings
)
from llama_index.readers.file import PDFReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

import chromadb

load_dotenv()

# Embeddings
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_key=os.getenv("API_KEY_OPENAI")
)

# Chroma Persistente
chroma_client = chromadb.PersistentClient(
    path="../../chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="documentos"
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# Carrega PDFs
loader = PDFReader()

documents = []

for pdf_file in Path("../../documents").glob("*.pdf"):

    docs = loader.load_data(file=pdf_file)

    for doc in docs:
        doc.metadata["arquivo"] = pdf_file.name

    documents.extend(docs)

# Cria índice
VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

print("Indexação concluída.")