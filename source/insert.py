#!/usr/bin/env python

"""insert.py  :  Insert document in the desired MongoDB and collection """

__author__ = "Marta Huertas"
__version__ = "0.1"
__maintainer__ = "Marta Huertas"
__email__ = "marta.huertas@crg.eu"
__status__ = "development"


# Import Packages
import json
from . import meta

# Insert one function
def insertOne(operation, db, collection_name, json_documents, name, method):
    """
    Insert one document in a specific collection from a database.
    The collection will be created if it doesn't exist.
    """
    # Read the JSON file
    with open(json_documents) as f:
        documents = json.load(f)

    # Access the collection:
    collection = db[collection_name]
    
    print(f"Documents inserted into {collection_name} collection")

    # Check if a document with the same ID already exists
    existing_document = collection.find_one({'stable_id': documents["stable_id"]})

    if existing_document:
        print(f"A document with the same stable_id already exists in the {collection_name} collection.")
    else:
        # Insert the document into the collection
        result = collection.insert_one(documents)

        doc_id = result.inserted_id

        # Print the inserted document ID
        print("Inserted document ID:", result.inserted_id)

        print("Generating meta information about the process.")

        # Get the ObjectId of the inserted process document
        process_id = meta.insertMeta(db, name, method, operation, collection_name)

        # Update inserted document with a reference to the meta document and operation
        meta_info = [
            {
            "meta_id" : str(process_id),
            "operation": operation
            }
        ]
        # Merge the meta_info with the existing document
        collection.update_one({"_id": doc_id}, {"$set": {"meta_info": meta_info}})

# Insert many function
def insertMany(operation, db, collection_name, json_documents, name, method):
    """
    Insert one document in a specific collection from a database.
    The collection will be created if it doesn't exist.
    """
    # Read the JSON file
    with open(json_documents) as f:
        documents = json.load(f)

    # Access the collection:
    collection = db[collection_name]

    print(f"Inserting into {collection_name} collection")

    # Get the unique identifier or combination of fields for each document
    unique_identifiers = [doc['stable_id'] for doc in documents]

    # Find existing documents with the same identifiers
    existing_documents = collection.find({'stable_id': {'$in': unique_identifiers}})

    # Get the list of existing identifiers
    existing_identifiers = [doc['stable_id'] for doc in existing_documents]

    # Filter out documents that are not already in the collection
    new_documents = [doc for doc in documents if doc['stable_id'] not in existing_identifiers]

    print(f"{len(existing_identifiers)} of your documents already exist in the {collection_name} collection.")
    # Insert only new documents into the collection
    if new_documents:
        result = collection.insert_many(new_documents)

        # Print the number of inserted documents
        print(f"Number of inserted documents: {len(result.inserted_ids)}")

        print("Generating meta information about the process.")
        # Get the ObjectId of the inserted process document
        process_id = meta.insertMeta(db, name, method, operation, collection_name)

        # Update each inserted document with a reference to the meta document and operation
        for doc_id in result.inserted_ids:
            meta_info = [
                {
                    "meta_id": str(process_id),
                    "operation": operation
                }
            ]
            # Merge the meta_info with the existing document
            collection.update_one({"_id": doc_id}, {"$set": {"meta_info": meta_info}})
    else:
        print("No new documents to insert.")