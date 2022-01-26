# Document_Header Start
"""
author : Adonay Pichardo
description :
"Python Template for all *.py files originally authored for Thor"
"""
# Standard Imports Start
# List all imports alphabetically for Python3 standard modules
import os

# Internal Imports Start
# List all imports alphabetically for modules authored for Thor

# External Imports Start
# List all imports alphabetically for modules NOT authored for Thor
import mysql.connector

# Classes Start
class Thor:
    # To interact with the Thor Database
    def __init__(self):
        ################################################################
        # 1. Establish credentials
        ################################################################
        credentials_file = open("credentials", 'r')
        self.credentials = {} # Used for authorizing the usage of the database

        # Read in credentialing information
        for line in credentials_file.readlines():
            key, value = line.rstrip().split(':')
            self.credentials[key] = value

        self.credentials = None

        ################################################################
        # 2. Connect to database
        ################################################################
        self.connection = mysql.connector.connect(host = credentials['host'],
                                                  user     = credentials['user'],
                                                  password = credentials['password'],
                                                  database = credentials['database'])

    # To add new tables defined in a local DDL file
    def send_ddl(ddl_file):
        ################################################################
        # 0. Create cursor
        ################################################################
        cursor = self.connection.cursor()
        cursor.close()

        ################################################################
        # 1. Open local DDL file
        ################################################################
        ddl_file = open(ddl_file, 'r')

        ################################################################
        # 2. Read file
        ################################################################
        ddl_file = ddl_file.read()

        ################################################################
        # 3. Send DDL to database
        ################################################################


    def get_table(target_table):
        ################################################################
        # 0. Create cursor
        ################################################################
        cursor = self.connection.cursor()
        cursor.close()

    def get_entire_database():
        ################################################################
        # 0. Create cursor
        ################################################################
        cursor = self.connection.cursor()
        cursor.close()

        entire_database = {}
        pass

    def update_table(target_table):
        ################################################################
        # 0. Create cursor
        ################################################################
        cursor = self.connection.cursor()
        cursor.close()

        pass

    def generate_key():
        ################################################################
        # 0. Create cursor
        ################################################################
        cursor = self.connection.cursor()
        cursor.close()

        pass

    def insert_record(target_table, new_data):
        ################################################################
        # 0. Create cursor
        ################################################################
        cursor = self.connection.cursor()
        cursor.close()

        pass
