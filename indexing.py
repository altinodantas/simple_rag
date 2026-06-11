import os
from pathlib import Path

from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings
)

from llama_index.readers.file import PDFReader
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

loader = PDFReader()

documents = []

for pdf_file in Path("documents").glob("*.pdf"):

    docs = loader.load_data(file=pdf_file)

    # Adiciona metadados do arquivo
    for doc in docs:
        doc.metadata["arquivo"] = pdf_file.name

    documents.extend(docs)

print(f"Total de documentos carregados: {len(documents)}")

index = VectorStoreIndex.from_documents(documents)

index.storage_context.persist(
    persist_dir="./storage"
)

print("Índice persistido.")
