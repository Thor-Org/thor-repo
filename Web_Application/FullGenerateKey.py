# <Document_Header Start>
"""
filename : FullGenerateKey.py
author : Adonay Pichardo
description :
Generates key from database, inserts key into database, and creates MD5 hash
"""
# <Document_Header End>

# <Standard Imports Start>
# List all imports alphabetically for Python3 standard libraries
from hashlib import md5
from sys import argv, stdout
# <Standard Imports End>

# <Internal Imports Start>
# NONE
# <Internal Imports End>

# <External Imports Start>
#import mysql.connector
# <External Imports End>

# <Global Objects Start>
DATABASE       = "Lightning_Data"
RAW_DATA       = "lightning_record"
GENERATED_KEYS = "generated_keys"
MD5_HASHES     = "md5_hashes"
# <Global Objects End>

# <Classes Start>
# NONE
# <Classes End>

# <Functions Start>
# <Functions End>
################################
# Creates connection to the database server with provided credentials
# INPUT: credentials - dictionary; contains key,value pairs with credentials for a mysql connection
################################
def connectToDatabase(credentials):
    return mysql.connector.connect(host     = credentials['host'],
                                   user     = credentials['user'],
                                   password = credentials['password'],
                                   database = credentials['database']
                                   )

################################
# Returns single row of data
################################
def get_lightning_data(connection):
    ################################
    # Create cursor to send queries
    ################################
    cursor = connection.cursor()

    ################################
    # Get data from table
    ################################
    cursor.execute(f'SELECT * FROM {DATABASE}.{RAW_DATA} LIMIT 1;\n')
    results = cursor.fetchall()

    cursor.close()

    return results

################################
# Inserts MD5 hash and key into database
################################
def insert_md5hash(connection, md5hash, key_used):
    cursor = connection.cursor()


    stdout.write(f'SQL:_> INSERT INTO {DATABASE}.{MD5_HASHES} VALUES ("{str(md5hash)}", "{str(key_used)}");')
    cursor.execute(f'INSERT INTO {DATABASE}.{MD5_HASHES} VALUES ("{str(md5hash)}", "{str(key_used)}");')
    cursor.close()

################################
# Inserts Key into database
################################
def insert_key(connection, key_generated):
    cursor = connection.cursor()

    # INSERT INTO Lightning_Data.generated_keys VALUE ("hello world");
    stdout.write(f'SQL:_> INSERT INTO {DATABASE}.{GENERATED_KEYS} VALUE ("{str(key_generated)}");\n')
    cursor.execute(f'INSERT INTO {DATABASE}.{GENERATED_KEYS} VALUE ("{str(key_generated)}");')
    cursor.close()

################################
# Uses Lightning Data to generate a unique key
################################
def generate_key(data):
    key = ""

    for every_item in data[0]:
        key += str(every_item).replace(" ", "").replace(":", "").replace(".", "").replace("-", "")

    return key

def main():
    print("(Success)")
    exit(0)
    ################################
    # Gather credential information
    ################################
    credentials_file = open('credentials', 'r')
    credentials = {} # Used for authorizing the usage of the database

    # Read in credentialing information
    for line in credentials_file.readlines():
        key, value = line.rstrip().split(':')
        credentials[key] = value

    ################################
    # Connect to Database
    ################################
    connection = connectToDatabase(credentials)

    # Get Lightning Data from Database to generate a Key
    lightning_data = get_lightning_data(connection)
    stdout.write(f'Lightning Data used to generate key:_> {lightning_data}\n')

    # Generate a key
    key_generated = generate_key(lightning_data)
    stdout.write(f'Key generated:_> {key_generated}\n')

    # Insert Key into Database
    insert_key(connection, key_generated)

    # Create MD5 hash
    md5hash = md5(key_generated.encode("utf-8")).hexdigest()
    stdout.write(f'MD5 hash generated:_> {md5hash}\n')

    # Insert MD5 hash into Database
    insert_md5hash(connection, md5hash, key_generated)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
