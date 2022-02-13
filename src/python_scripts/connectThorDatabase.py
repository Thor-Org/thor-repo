import mysql.connector

def connectThorDatabase():
    credentials_file = open("credentials", 'r')
    credentials = {} # Used for authorizing the usage of the database

    # Read in credentialing information
    for line in credentials_file.readlines():
        key, value = line.rstrip().split(':')
        credentials[key] = value

    return mysql.connector.connect(host     = credentials['host'],
                                   user     = credentials['user'],
                                   password = credentials['password'],
                                   database = credentials['database']
                                   )
