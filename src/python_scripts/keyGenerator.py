'''
    Thor: Random Number Genorator utilizing natural phenominon data (lightning data)
'''

import getDatabase # Used to get table Lightning_Data.lightning_records only from Database
import mysql.connector

from sys import stdout
from copy import deepcopy

class DataPoint:
    def __init__(self, col, data, flag):
        self.data = data
        self.flag = flag
        self.col = col

    def get_next_index(self, class_list):
        n = len(class_list) - 1
        n_digits = len(str(n))
        num_len = len(str(self.data))

        next_index = (int(self.data / n)) % n
        next_index = (int(self.data /pow(10, num_len - n_digits))) % n

        i = 0
        # if we get a number with flag used recently, we skip, and reflip flag for later use
        while class_list[next_index][self.col].flag == 1:
            i = i+1
            old_index = next_index
            next_index = (old_index + pow(i, 2)) % n

            # once we have skipped over the old once, we can reuse
            class_list[old_index][self.col].flag = 0

        return next_index

def insertPermutationsToDataBase(connection, permutations):
    stdout.write(f'{connection.is_connected()}\n')

    for every_permutation in permutations:
        try:
            cursor = connection.cursor()
            stdout.write(f'INSERT INTO Lightning_Data.permutations VALUES ("{every_permutation}");\n')
            cursor.execute(f'INSERT INTO Lightning_Data.permutations VALUES ("{every_permutation}");')
            cursor.close()
        except Exception as error:
            stdout.write(f'ERROR!!! {error}\n')
            stdout.write(f'FAILED!!! INSERT INTO Lightning_Data.permutations VALUES ("{every_permutation}");\n')
            continue

def insertCombinationsToDataBase(connection, combinations, meta_data):
    # Remove the head of the 2d list
    meta_data = meta_data[1:]

    for index in range(len(combinations)):
        # Parse the time
        strike_time, NN = meta_data[index][0].split(".")

        try:
            cursor = connection.cursor()
            stdout.write(f"INSERT INTO Lightning_Data.combinations VALUES ({combinations[index]},'{strike_time}',{NN},{meta_data[index][1]},{meta_data[index][2]},{meta_data[index][3]},{meta_data[index][4]},{meta_data[index][5]});\n")
            result = cursor.execute(f"INSERT INTO Lightning_Data.combinations VALUES ({combinations[index]},'{strike_time}',{NN},{meta_data[index][1]},{meta_data[index][2]},{meta_data[index][3]},{meta_data[index][4]},{meta_data[index][5]});\n")
            connection.commit()
            cursor.close()
            pass
        except Exception as error:
            stdout.write(f'ERROR!!! {error}\n')
            stdout.write(f"FAILED!!! INSERT INTO Lightning_Data.combinations VALUES ({combinations[index]},'{strike_time}',{NN},{meta_data[index][1]},{meta_data[index][2]},{meta_data[index][3]},{meta_data[index][4]},{meta_data[index][5]});\n")
            continue
    
# make all fields the same number of digits
def weight_fields(data_list, num_size):

    for i in range(len(data_list)): # row
        for j in range(len(data_list[0])): # col
            data_list[i][j] = abs(float(data_list[i][j]))
            num_len = len(str(int(data_list[i][j])))


            if num_len < num_size:
                data_list[i][j] = data_list[i][j] * pow(10, (num_size - num_len))

            if num_len > num_size:
                data_list[i][j] = data_list[i][j] / pow(10, (num_size - num_len))

    return data_list

# weights all fields from the database
def formatData(lightning_records):
    # 2d list of doubles for the weighted data
    weighted_data = []

    # retreives name from first field of database
    fieldNames = lightning_records[0]
    del lightning_records[0]

    # isolates the nanosecond for the use of time
    for i in range(len(lightning_records)):
        time, nanoSecond = lightning_records[i][0].split('.')
        lightning_records[i][0] = nanoSecond

    # equally weights all fields
    weighted_data = weight_fields(lightning_records, 9)

    # Update lightning record to a 2d list of datpoint objects
    for i in range(len(weighted_data)):
        for j in range(len(weighted_data[0])):
            lightning_records[i][j] = DataPoint(col = j, data=int(weighted_data[i][j]), flag=0)

    return lightning_records, fieldNames

# prints a specfied ammount of rows in a formatted table
def print_data(data, number_of_rows, fieldNames):
    print("{:12} {:12} {:12} {:12} {:12} {:12} ".format(fieldNames[0], fieldNames[1], fieldNames[2], fieldNames[3], fieldNames[4], fieldNames[5]))
    for i in range(number_of_rows):
        row = data[i]
        print("{:12.2f} {:12.2f} {:12.2f} {:12.2f} {:12.2f} {:12.2f} ".format(row[0].data, row[1].data, row[2].data, row[3].data, row[4].data, row[5].data))

# uses random fields in the data to make psudo lightning strikes
def permutationGeneration(data, requested_keys):
    permuntations = []

    # base cases for permuntation gen
    r0 = data[0][0]
    r1 = data[0][1]
    r2 = data[0][2]
    r3 = data[0][3]
    r4 = data[0][4]
    r5 = data[0][5]


    for i in range(requested_keys):
        r0_index = r0.get_next_index(data)
        r1_index = r1.get_next_index(data)
        r2_index = r2.get_next_index(data)
        r3_index = r3.get_next_index(data)
        r4_index = r4.get_next_index(data)
        r5_index = r5.get_next_index(data)

        r0 = data[r4_index][0]
        r1 = data[r1_index][1]
        r2 = data[r2_index][2]
        r3 = data[r3_index][3]
        r4 = data[r4_index][4]
        r5 = data[r4_index][5]
        r0.flag = 1
        r1.flag = 1
        r2.flag = 1
        r3.flag = 1
        r4.flag = 1
        r5.flag = 1

        number = r0.data + r1.data + r2.data + r3.data
        permuntations.append(int(number))

    duplicate_count = len(permuntations) - len(list(set(permuntations)))
    print("Generated {} permutations with {} duplicates".format(requested_keys, duplicate_count))

    return permuntations

# Combines all equally weighted fields to produce a true key
def combinationGeneration(data):
    keys = []
    for row in data:
        keys.append(int(row[0].data+ row[1].data+ row[2].data+ row[3].data))

    duplicate_count = len(keys) - len(list(set(keys)))
    print("Generated {} combinations with {} duplicates".format(len(data), duplicate_count))

    return keys

def main():
    # pulls the data base using punction from getDatabase.by in the REPO
    lightning_records = getDatabase.getDatabase()
    temp_copy = deepcopy(lightning_records)
    
    # retrives formatted and weighted double(2d array of DataPoint obj) and filedNames
    data, fieldNames = formatData(lightning_records)

    # Generates any number of specified permutations
    permutations = permutationGeneration(data, 10000)

    # Generates any number of specified permutations
    combinations = combinationGeneration(data)

    # Connect to Thor Database
    credentials_file = open('credentials', 'r')
    credentials = {} # Used for authorizing the usage of the database

    # Read in credentialing information
    for line in credentials_file.readlines():
        key, value = line.rstrip().split(':')
        credentials[key] = value

    connection = mysql.connector.connect(host     = credentials['host'],
                                         user     = credentials['user'],
                                         password = credentials['password'],
                                         database = credentials['database'])

    insertPermutationsToDataBase(connection, permutations)
    connection.commit()

    insertCombinationsToDataBase(connection, combinations, temp_copy)
    connection.commit()

    # Close connection
    connection.close()

if __name__ == '__main__':
    main()
