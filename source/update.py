#!/usr/bin/env python

"""update.py  :  Update specific or many documents in the desired MongoDB and collection """

__author__ = "Marta Huertas"
__version__ = "0.1"
__maintainer__ = "Marta Huertas"
__email__ = "marta.huertas@crg.eu"
__status__ = "development"

from . import meta

# Insert one function
def updateOne(operation, db, collection_name, update_criteria, update_field, new_value, name, method):
    """
    Update one document in a specific collection from database
    """
    
    # Access the collection:
    collection = db[collection_name]
    
    # Find the document before the update to retrieve the previous value
    previous_document = collection.find_one(update_criteria)
    
    # Check if the document with the specified criteria exists in the collection
    if previous_document:
        # Get the previous value of the field
        previous_value = previous_document.get(update_field)

        # Insert metadata about the update process
        process_id = meta.insertMeta(db, name, method, operation, collection_name)

        # Get the existing meta_info, or an empty dictionary if it doesn't exist
        existing_meta_info = previous_document.get("meta_info", {})

        # Define the new metadata to be added
        new_meta_info_key = f"{operation}_{len(existing_meta_info)}"  # Create a unique key
        new_meta_info = {
            "process_id": process_id,
            "modified_field": update_field,
            "previous_value": previous_value
        }

        # Merge the new metadata with the existing meta_info
        updated_meta_info = {**existing_meta_info, new_meta_info_key: new_meta_info}

        # Update the document
        result = collection.update_one(update_criteria, {"$set": {update_field: new_value, "meta_info": updated_meta_info}})
        
        # Print whether the document was updated or not
        if result.modified_count > 0:
            print(f'Field {update_field} updated successfully in the document with {list(update_criteria.keys())[0]}: {list(update_criteria.values())[0]}')
        else:
            print(f"The field {update_field} already has the specific value")
    else:
        print(f"The document you are searching for is not in the collection.") 


def updateAll(operation, db, collection_name, update_field, new_value, name, method):
    """
    Update all documents in a specific collection from database
    """
    # Access the collection:
    collection = db[collection_name]

    # Find all documents before the update to retrieve the previous values
    previous_documents = collection.find({})
    
    # Insert metadata about the update process
    process_id = meta.insertMeta(db, name, method, operation, collection_name)
    
    print( "Updating documents")
    # Iterate over each document to retrieve previous values and update with metadata
    for previous_document in previous_documents:
        # Get the previous value of the field
        previous_value = previous_document.get(update_field)

        # Get the existing meta_info, or an empty dictionary if it doesn't exist
        existing_meta_info = previous_document.get("meta_info", {})

        # Define the new metadata to be added
        new_meta_info_key = f"{operation}_{len(existing_meta_info)}"  # Create a unique key
        new_meta_info = {
            "process_id": process_id,
            "modified_field": update_field,
            "previous_value": previous_value
        }

        # Merge the new metadata with the existing meta_info
        updated_meta_info = {**existing_meta_info, new_meta_info_key: new_meta_info}

        # Update the document with the new metadata
        collection.update_one({"_id": previous_document["_id"]}, {"$set": {update_field: new_value, "meta_info": updated_meta_info}})
    
    print(f'Field {update_field} updated successfully in all the documents. New value: {new_value}')


def updateMany(operation, db, collection_name, update_criteria, update_field, new_value, name, method):
    """
    Update multiple documents in a specific collection based on given criteria
    """
    # Access the collection
    collection = db[collection_name]
    
    # Find documents matching the criteria before the update to retrieve the previous values
    previous_documents = list(collection.find(update_criteria))
    
    # Insert metadata about the update process
    process_id = meta.insertMeta(db, name, method, operation, collection_name)
    
    # Iterate over each matching document to retrieve previous values and update with metadata
    for previous_document in previous_documents:
        # Get the previous value of the field
        previous_value = previous_document.get(update_field)

        # Get the existing meta_info, or an empty dictionary if it doesn't exist
        existing_meta_info = previous_document.get("meta_info", {})

        # Define the new metadata to be added
        new_meta_info_key = f"{operation}_{len(existing_meta_info)}"  # Create a unique key
        new_meta_info = {
            "process_id": process_id,
            "modified_field": update_field,
            "previous_value": previous_value
        }

        # Merge the new metadata with the existing meta_info
        updated_meta_info = {**existing_meta_info, new_meta_info_key: new_meta_info}

        # Update the document with the new metadata
        collection.update_one({"_id": previous_document["_id"]}, {"$set": {update_field: new_value, "meta_info": updated_meta_info}})
    
    print(f'Field {update_field} updated successfully in {len(previous_documents)} documents matching the criteria. New value: {new_value}')

