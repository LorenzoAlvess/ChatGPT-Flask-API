from pymongo import MongoClient
import os
from typing import List, Dict, Any

host = os.getenv('MONGO_HOST', 'localhost')
port = os.getenv('MONGO_PORT', 27017)
db_name = os.getenv('MONGO_DB_NAME', 'test')

class MongoDB:
    def __init__(self) -> None:
        """
        Initialize MongoDB client and connect to the specified database.
        """
        try:
            self.client = MongoClient(host, port)
            self.db = self.client[db_name]
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def list_collections(self) -> List[str]:
        """
        List all collections in the current database.

        Returns:
        - List[str]: List of collection names.
        """
        return self.db.list_collection_names()

    def create_collection(self, collection_name: str) -> None:
        """
        Create a new collection in the database.

        Parameters:
        - collection_name (str): Name of the new collection.
        """
        self.db[collection_name]

    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> Any:
        """
        Insert a document into the specified collection.

        Parameters:
        - collection_name (str): Name of the collection to insert the document into.
        - document (Dict[str, Any]): Document to be inserted.

        Returns:
        - Any: The result of the insertion operation.
        """
        collection = self.db[collection_name]
        return collection.insert_one(document)

    def list_documents(self, collection_name: str) -> List[Dict[str, Any]]:
        """
        List all documents in the specified collection.

        Parameters:
        - collection_name (str): Name of the collection to list documents from.

        Returns:
        - List[Dict[str, Any]]: List of documents in the collection.
        """
        collection = self.db[collection_name]
        documents = []
        for document in collection.find():
            formatted_document = {
                "role": document["role"],
                "content": document["content"]
            }
            documents.append(formatted_document)
        return documents
