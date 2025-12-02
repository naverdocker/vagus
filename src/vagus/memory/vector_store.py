import chromadb
from chromadb.utils import embedding_functions

from ..config import VECTOR_DB_PATH

class VectorStore:
    def __init__(self, collection_name="vagus_docs"):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

        # Use ChromaDB's default Sentence Transformer embedding function
        # This will download the model if not present, but runs locally.
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
        )

    def add_documents(self, texts, metadatas=None):
        """
        Adds documents to the vector store.
        Args:
            texts (List[str]): List of document texts to add.
            metadatas (List[dicts], optional): List of metadata dictionaries, one for each text.
        """
        if not texts:
            return

        # ChromaDB requires unique ID for each document.
        ids = [f"doc_{self.collection.count() + i}" for i in range(len(texts))]

        self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
        )
        print(f"Added {len(texts)} document to '{self.collection.name}' collections.")

    def query(self, query_texts, n_results=5):
        """
        Queries the vector store for similar documents.
        Args:
            query_texts (list[str]): List of texts to query with.
            n_results (int): Number of similar results to return.
        Returns:
            dict: Query results from ChromaDB.
        """
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results

    def count(self):
        """Returns the number of documents in the collection"""
        return self.collection.count()


