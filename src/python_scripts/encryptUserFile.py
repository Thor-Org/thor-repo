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
from sys import argv, stdout
import base64

# Thor Imports
from connectThorDatabase import connectThorDatabase

# None Standard Imports
from Crypto.Cipher import AES # pip3 install pycrypto, then pip3 pycryptodome
from Crypto.Random import get_random_bytes

def getCombination():
    connection = connectThorDatabase()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT combination FROM Lightning_Data.combinations;")
        result = cursor.fetchall()[0][0]

        cursor.close()
        connection.close()

        stdout.write(f'{result}\n')
        return result

    except Exception as error:
        stdout.write(f'ERROR!!! {error}\n')

    return False

def deleteCombination(combination):
    connection = connectThorDatabase()
    cursor = connection.cursor()

    try:
        cursor.execute(f"DELETE FROM Lightning_Data.combinations WHERE combination = '{combination}';")

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as error:
        stdout.write(f'ERROR!!! {error}\n')

def recordKeyUsed(key):
    connection = connectThorDatabase()
    cursor = connection.cursor()

    try:
        cursor.execute(f'INSERT INTO Lightning_Data.keys_used VALUES ("{key}");')

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as error:
        stdout.write(f'ERROR!!! {error}\n')

# Functions
def main():
    # Read in file
    targetFile = open("../../uploads/" + argv[1], 'r')
    targetFile = targetFile.read().encode("utf8")
    stdout.write(f'ORIGINAL\n{targetFile}\n')

    # Get combination from Database
    key = getCombination()

    stdout.write(f'key = {key}\n')

    # Record key used
    recordKeyUsed(key)

    # Delete combination from Database
    deleteCombination(key)

    ################################
    # Encrypt
    ################################
    # Key must be 16 bytes
    key += key[0:6]

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(targetFile)

    file_out = open("encrypted.bin", "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()

    # ################################
    # # Decrypt
    # ################################


if __name__ == "__main__":
    main()
