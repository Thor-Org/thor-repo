# Document_Header
"""
author : Adonay Pichardo
description :
Used to encrypt a file with AES

Usage:
user@host#:_>python3 encryptUserFile.py myLittleFile.txt
File:_> myLittleFile.txt
Encryption:_> AES
Key:_> 237692730480928346

myLittleFile_encrypted
myLittleFile_receipt
"""
# Standard Imports
from Crypto.Cipher import AES
from sys import stdout

# Thor Imports
from connectThorDatabase import connectThorDatabase

def getCombination():
    connection = connectThorDatabase()
    cursor = connection.cursor()

    try:
        result = cursor.execute("SELECT 1 FROM Lightning_Data.combinations;")
        connection.commit()

        stdout.write(f'{result}\n')
    except Exception as error:
        stdout.write(f'ERROR!!! {error}\n')

    cursor.close()
    connection.close()

    return

def deleteCombination(combination):
    connection = connectThorDatabase()
    cursor = connection.cursor()



    pass

# Functions
def main():
    # Read in file
    # targetFile = open("../../uploads/" + argv[1], 'r')
    # targetFile = targetFile.read()

    # Get combination from Database
    key = getCombination()

    # # Delete combination from Database
    # deleteCombination(key)

    # AESObject = AES.new()

if __name__ == "__main__":
    main()
