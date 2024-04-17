#!/usr/bin/env python

"""main.py  :  Run any operation needed in the mongoDB """

__author__ = "Marta Huertas"
__version__ = "0.1"
__maintainer__ = "Marta Huertas"
__email__ = "marta.huertas@crg.eu"
__status__ = "development"

# Import packages
import sys
from pymongo import MongoClient
import conf
from source import insert, update, mongoConnection

# Functions
def print_help():
    print('USAGE:')
    print('This script combines different tools to manage the BioMongoDB in EGA')
    print('First thing to do is to write your needs in the conf.py file')
    print('Follow the guidelines in that file.')

def connect_mongo():
    try:
        # Connect to MongoDB
        client = MongoClient(mongoConnection.mongo_host, mongoConnection.mongo_port, username=mongoConnection.username, password=mongoConnection.password, authSource=mongoConnection.auth_source)
        # Acces the database:
        db = client[conf.database_name]
        # If connection successful, print success message
        print("Connection to BioMongoDB established.")

        return db
    except ConnectionError as e:
        # If connection fails, print error message
        print("Failed to connect to MongoDB:", e)

def run_operation():
    """
    Run operations in the BioMongoDB by reading the conf file
    """
    # Get database connection:
    db = connect_mongo()

    if conf.operation == 'insert_one':
        insert.insertOne(conf.operation, db, conf.collection_name, conf.json_documents, conf.name, conf.method)

    elif conf.operation == 'insert_many':
        insert.insertMany(conf.operation, db, conf.collection_name, conf.json_documents, conf.name, conf.method)
    
    elif conf.operation == 'update_one':
        update.updateOne(db, conf.collection_name, conf.update_criteria, conf.update_field, conf.new_value)

    elif conf.operation == 'update_many':
        update.updateMany(db, conf.collection_name, conf.update_criteria, conf.update_field, conf.new_value)
    
    elif conf.operation == 'update_all':
        update.updateAll(db, conf.collection_name, conf.update_field, conf.new_value)


def main():
    if conf.operation == '':
        # First print help message just in case.
        print_help()
    else:
        print(f'Operation: {conf.operation}')
        print(f'Database: {conf.database_name}')

        # Run the operation determined in conf:
        run_operation()

if __name__ == main():
    main


        