import uuid
import chromadb
from chromadb.utils import embedding_functions

from ..config import VECTOR_DB_PATH, DEFAULT_EMBEDDING_MODEL

class VectorStore:
    def __init__(self, collection_name="vagus_docs"):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        
        # Use ChromaDB's default Sentence Transformer embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=DEFAULT_EMBEDDING_MODEL
        )
        
        # Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_documents(self, texts, metadatas=None):
        """
        Adds documents to the vector store.
        Args:
            texts (list[str]): List of document texts to add.
            metadatas (list[dict], optional): List of metadata dictionaries,
                                               one for each text.
        """
        if not texts:
            return

        # Generate unique IDs using UUID4 to avoid race conditions
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]

        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(texts)} documents to '{self.collection.name}' collection.")

    def query(self, query_texts, n_results=5, where=None):
        """
        Queries the vector store for similar documents.
        Args:
            query_texts (list[str]): List of texts to query with.
            n_results (int): Number of similar results to return.
            where (dict, optional): Metadata filtering dictionary.
        Returns:
            dict: Query results from ChromaDB.
        """
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )
        return results

    def count(self):
        """Returns the number of documents in the collection"""
        return self.collection.count()


