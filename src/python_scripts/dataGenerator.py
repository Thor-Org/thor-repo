# -*- coding: utf-8 -*-
# MySQL Workbench Python script
# <description>
# Written in MySQL Workbench 8.0.26



'''
data = ['0:UFAL', '1:NetType', '2:Year', '3:Month', '4:Day', '5:Hour',
        '6:Minute', '7:Second', ':Nanosecond', ':Latitude', ':Longitude', ':Altitude',
        ':AltUncertinty', ':PeakCurrent', ':VFR', ':Multiplicity', ':PulseCount', ':SensorCount',
        ':DegreeOfFreedom', ':EllipseAngle', ':Error1', ':Error2', ':ChiSquard', ':RiseTime',
        ':PeakToZero', ':RateOfRise', ':CloudIndicator', ':AngleIndicator', ':Signal Indicator', ':TimingIndicator']

'''
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

# inports the data from local csv
def localDataLoad():
    df = pd.read_csv('./00.txt', sep='	')

    return df_list

# would push all data in field to data bas 
def pushData(data):

    # connects to the data base
    mydb = mysql.connector.connect(
        host='97.102.250.88',
        user='root',
        password='Sadie1289',
        database='Lightning_Data'
    )

    mycursor = mydb.cursor()


    # pushes evver row in the ASCII file to the data base with object datetime and nanosecond additoinal field
    for row in data:
        sampleTime = str('%s-%s-%d %s:%s:%s' % (int(row[2]), int(row[3]), int(
            row[4]), int(row[5]), int(row[6]), int(row[7])))

        mycursor.execute(
            f"INSERT INTO Lightning_Data.lightning_record VALUES ('{sampleTime}',{row[8]}, {row[9]},{row[10]},{row[23]},{row[24]},{row[13]})")

        print(
            f"INSERT INTO Lightning_Data.lightning_record VALUES ('{sampleTime}',{row[8]}, {row[9]},{row[10]},{row[23]},{row[24]},{row[13]})")

        mydb.commit()


# NEED TO FIX, ONLY WORKS FOR DATA FRAME NOT 2D LIST
# plots the data from point to points
def scatterPlot(df):
    plt.xlabel("Lightning Strike")
    plt.ylabel("Random Number Generated")
    plt.scatter(df['Range'], abs(df['Latitude']
                * df['Longitude'] * df['Nanosecond']), s=100, marker='|', alpha=0.5)

    # marker = r'$\clubsuit$'
    plt.show()


# Prints that stddev of all fields in df
def printStandardDev(df):
    print("\nSTD DEV:")
    # prints the standard deviatoin of all items in data frame
    for name in df.iteritems():
        print(f'{name[0]:15} STD = {df[name[0]].std():.2f})')

# Prints that varof all fields in df
def printVar(df):
    print("\nVAR:")
    # prints the standard deviatoin of all items in data frame
    for name in df.iteritems():
        print(f'{name[0]:15} STD = {df[name[0]].var():.2f})')

# finds the differnce between all values and returns average
def averageDiff(numberCol):
    prevNumber = 0
    diff = []

    # finds the avearge difference in numbers
    for number in numberCol:
        diff.append(abs(number - prevNumber))
        prevNumber = number

    averageDiff = sum(diff) / len(diff)

    return averageDiff

# gerneates a scatter plot based on fields
def scatterPlot(df, columnVector):
    plt.scatter(df['Range'][0:len(columnVector)],
                columnVector, s=100, marker='|', alpha=0.5,)
    plt.xlabel("Lightning Strike")
    plt.ylabel("Random Number Generated")
    plt.show()



def main():


    # inports the data from local csv
    df = pd.read_csv('./00.txt', sep='	')

    # takes the absolute value of all fields in the data frame
    df = df.abs()


    # adds labels to all data imported
    df.columns = ['UFAL', 'NetType', 'Year', 'Month', 'Day', 'Hour',
                'Minute', 'Second', 'Nanosecond', 'Latitude', 'Longitude', 'Altitude',
                'AltUncertinty', 'PeakCurrent', 'VFR', 'Multiplicity', 'PulseCount', 'SensorCount',
                'DegreeOfFreedom', 'EllipseAngle', 'Error1', 'Error2', 'ChiSquard', 'RiseTime',
                'PeakToZero', 'RateOfRise', 'CloudIndicator', 'AngleIndicator', 'Signal Indicator', 'TimingIndicator']


    # adds another field to the data for ease of plotting
    df['Range'] = np.transpose(range(0, len(df['Latitude'])))
    df['TestLatitude'] = (df['Latitude'] % 1) * 100000
    df['TestLongitude'] = (df['Longitude'] % 1) * 100000
    df['TestEllipseAngle'] = df['EllipseAngle'] * 100


    # prints the stddev of all fields
    printStandardDev(df)
    printVar(df)



    # printing the new vs old long and lat
    print(df[['Latitude',
          'Longitude','TestLatitude', 'TestLongitude']].head(4))

    print(df[['EllipseAngle', 'TestEllipseAngle', 'Nanosecond']].head(4))



    # wordlist is all fields I used in research
    wordlist = ['Latitude', 'Longitude', 'TestLatitude',
                'TestLongitude', 'EllipseAngle', 'TestEllipseAngle', 'Nanosecond']

    # prints the varience of all fields in wordlist
    for word in wordlist:
        print(f'{word:18} VAR = {df[word].var():.2f}')

    # prints all standard deviations for all fields in wordlist
    for word in wordlist:
        print(f'{word:18} StdDev = {df[word].std():.2f}')

    
    # milestone 1 method of data generation
    Version1 = df['Latitude'] * df['Longitude'] * df['Nanosecond']


    # using experimental lat and long that is made above
    Version2 = (df['TestLatitude'] + df['TestLongitude'] +
                df['Nanosecond']) + (df['EllipseAngle'] * 100)

    # finds av differnce of all numbers in data set
    averageDifference = averageDiff(Version2)


    # version 3 is version 2 but removing large clumps by excluding any num within (10% of avaerage difference) of eachother
    Version3 = []
    prevNumber = 0
    for number in Version2:
        if abs(number - prevNumber) > (averageDifference / 10):
            Version3.append(number)
        prevNumber = number



    # plots the data from point to points
    scatterPlot(df, Version3)


    


if __name__ == '__main__':
    main()
