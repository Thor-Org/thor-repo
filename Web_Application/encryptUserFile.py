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

myLittleFile_ENCRYPTED
myLittleFile_RECEIPT
"""
# Standard Imports
from sys import argv, stdout
import base64

# Thor Imports
from connectThorDatabase import connectThorDatabase

# None Standard Imports
from Cryptodome.Cipher import AES # pip3 install pycrypto, then pip3 pycryptodome

def getCombination():
    connection = connectThorDatabase()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT combination FROM Lightning_Data.combinations;")
        result = cursor.fetchall()[0][0]

        cursor.close()
        connection.close()

        # stdout.write(f'{result}\n')
        output = f'{result}'
        output = int(output)
        print(output)
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
    targetFile = open("uploads/" + argv[1], 'r')
    targetFile = targetFile.read()

    # Encode for AES
    targetFile = targetFile.encode("utf8")

    # Get combination from Database
    key = getCombination()
    # AES requires a key divisible by 16
    key += key[0:6]

    # Record key used
    recordKeyUsed(key)

    # Delete combination from Database
    deleteCombination(key)

    ################################
    # Encrypt
    ################################
    # Key must be 16 bytes
    key = key.encode("utf8")

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(targetFile)

    fileOut = open("uploads/" + argv[1] + "_ENCRYPTED", "wb")
    [ fileOut.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    fileOut.close()

    fileOut = open("uploads/" + argv[1] + "_RECEIPT", "w")
    fileOut.write(f'File:_> {argv[1]}\nEncryption:_> AES\nKey:_> {str(key)[2:-3]}\n')
    fileOut.close()

    # ################################
    # # Decrypt
    # ################################
    fileIn = open("uploads/" + argv[1] + "_ENCRYPTED", "rb")
    nonce, tag, ciphertext = [ fileIn.read(x) for x in (16, 16, -1) ]

    # let's assume that the key is somehow available again
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # stdout.write(f'\n{str(data)[2:-3]}\n')

if __name__ == "__main__":
    main()
