import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statistics import mean
import random
from scipy.stats import entropy
from hashlib import md5

class DataPoint:
    def __init__(self, row, data, flag):
        self.data = data
        self.flag = flag
        self.row = row

    def get_next_index(self, class_list, n):
        next_index = (int(self.data / n)) % n
        
        i = 0
        # if we get a number with flag used recently, we skip, and reflip flag for later use
        while class_list[self.row][next_index].flag == 1:
            i = i+1
            old_index = next_index
            next_index = (old_index + pow(i, 2)) % n

            # once we have skipped over the old once, we can reuse
            class_list[self.row][old_index].flag = 0
            

            if( i > 30):
                print('Error with row: ' + str(self.row) + ' ' +str(next_index) + ' ' +str(i))
            

        print(self.data, next_index)


        return next_index





# returns data frame (df) and word list of all fields imported
def read_data():
    # inports the data from local csv
    df = pd.read_csv('./00.txt', sep='	')

    # takes the absolute value of all fields in the data frame
    df = df.abs()

    masterWordList = ['UFAL', 'NetType', 'Year', 'Month', 'Day', 'Hour',
                'Minute', 'Second', 'Nanosecond', 'Latitude', 'Longitude', 'Altitude',
                'AltUncertinty', 'PeakCurrent', 'VFR', 'Multiplicity', 'PulseCount', 'SensorCount',
                'DegreeOfFreedom', 'EllipseAngle', 'Error1', 'Error2', 'ChiSquard', 'RiseTime',
                'PeakToZero', 'RateOfRise', 'CloudIndicator', 'AngleIndicator', 'Signal Indicator', 'TimingIndicator']

    df.columns = masterWordList

    # adds another field to the data for ease of plotting
    df['Range'] = np.transpose(range(0, len(df['Latitude'])))
    masterWordList.append('Range ')

    return df, masterWordList

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
        print(f'{name[0]:15} VAR = {df[name[0]].var():.2f})')

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

# generates genertic histogram
def histogram(data):
    plt.hist(data)
    plt.show

# histrogram of all fields to compare
def hisoComparison(data1, data2, data3):
    
    sns.set(style="whitegrid")

    fig, axs=plt.subplots(1, 2, figsize=(15, 6))
    axs[0].hist(data1, 50, color = "r")
    axs[0].set_title("Milestone 2 Distribution")
    axs[0].set_xlabel(f'Key values per 100Million')
    axs[0].set_ylabel('Distribution')

    axs[1].hist(data2, 50, color = "m") 
    axs[1].set_title("Milestone 3 Distribution")
    axs[1].set_xlabel(f'Key values per 100Billion')
    axs[1].set_ylabel('Distribution')

    plt.show()



    '''
    sns.set(rc={"figure.figsize": (15, 6)})

    
    plt.subplot(1,2,1)
    range_in_box = (max(data2) - min(data2)) / 50
    ax = sns.displot(data2, 50, color='b')
    ax.set_title('Where we started')
    ax.set_xlabel(f'Key values per 100Billion')
    ax.set_ylabel('How many numbers in bin')
    plt.ylim(1,50)




    plt.subplot(1,2,2)
    ax = sns.distplot(data3, 50, color='g')
    ax.set_title('Where we are at')
    ax.set_xlabel(f'Key values per 100Million')
    ax.set_ylabel('How many numbers in bin')

    

    plt.show()

    '''


# generates a list of random numbers from random library for baseline
def version0Gen(df):
    v0 = []

    for i in range(len(df['Range'])):
        v0.append(random.random() * 10000000000000000)
    return v0

# was mutiplyng random numbers to increase randomness gaps
# theory was incorct, assumed lightning fields were random
def version1Gen(df):
    return list(df['Latitude'] * df['Longitude'] * df['Nanosecond'])

# used random numbers behind decimal point to get more randomness and to eliminate trends based on locaiton
# theory was incorct, assumed lightning fields were random behind decimal point
def version2Gen(df):
    return list((df['TestLatitude'] + df['TestLongitude'] + df['Nanosecond']) + (df['EllipseAngle'] * 100))

# used version2 and forcably spread out clumps
# theory was incorct, still iteraive
def version3Gen(df, Version2):
    # finds av differnce of all numbers in data set
    averageDifference = averageDiff(Version2)


    # version 3 is version 2 but removing large clumps by excluding any num within (10% of avaerage difference) of eachother
    Version3 = []
    prevNumber = 0
    for number in Version2:
        if abs(number - prevNumber) > (averageDifference / 10):
            Version3.append(number)
        prevNumber = number

    return list(Version3)

# simply adjusted how v3 was generated for use in v5
def version4Gen(df):
    return list(df['TestLatitude'] + df['TestLongitude'] + df['Nanosecond'] + df['TestEllipseAngle'])

# another attemp at removing clumps but still had iterative problrm
def version5Gen(df, version4):
    averageDifference = averageDiff(version4)

    prevNumber = 0
    version5 = []
    for number in version4:
        if abs(number - prevNumber) > (averageDifference / 10):
            version5.append(number)
        prevNumber = number

    return version4

# using v5 as the seed, and running it through random function
def version6Gen(df, version5):
    #mean = mean(version5)
    #np.random.seed(mean)

    version6 = []
    for i in range(1, len(version5)):
        random.seed(version5[i])
        version6.append(random.random() * 10000000000000000)

    return version6

# flattens the curve from version6
# this is probably really bad
def version7Gen(df, version6):
    # Rayleigh distribution: https://math.stackexchange.com/questions/153097/flattening-a-2d-normal-distribution
    # a way to flatten curve
    version7 = 7
    
def main():

    # df: df (data frame) is all data from provided 00.txt file in an object
    # masterWordList: all fields used in data frame
    print('reading data...')
    df, masterWordList = read_data()
    print('data import complete')


    print('generating new fields...')
    # adding test fields by removing numbers before decimal point (101.1234 -> 1234)
    df['TestLatitude'] = (df['Latitude'] % 1) * 100000000
    df['TestLongitude'] = (df['Longitude'] % 1) * 100000000
    df['TestEllipseAngle'] = df['EllipseAngle'] * 100000
    df['TestNano'] = df['Nanosecond'] % 100000000

    # adding new fields to masterWordList
    masterWordList.append('TestLatitude')
    masterWordList.append('TestLongitude')
    masterWordList.append('TestEllipseAngle')
    masterWordList.append('TestNano')
    print('fields generation complete')

    
    print('generating all latest versions...')
    # generates all versions of the key value based on lightning data
    v0 = version0Gen(df)
    v1 = version1Gen(df)
    v2 = version2Gen(df)
    v3 = version3Gen(df, v2)
    v4 = version4Gen(df)
    v5 = version5Gen(df, v4)
    v6 = version6Gen(df, v5)
    v7 = version7Gen(df, v6)
    print('verion generation complete')

    # prints entrophy of all versions
    # print(f'Entrphy of V0: {entropy(v0):.5}')
    # print(f'Entrphy of V1: {entropy(v1):.5}')
    # print(f'Entrphy of V2: {entropy(v2):.4}')
    # print(f'Entrphy of V3: {entropy(v3):.4}')
    # print(f'Entrphy of V4: {entropy(v4):.4}')
    # print(f'Entrphy of V5: {entropy(v5):.4}')
    # print(f'Entrphy of V6: {entropy(v6):.5}')


    print('Plotting hist compare')
    # gernerates histograms used for senior design presentation
    #hisoComparison(v1, v5, v5)
    # scatterPlot(df, v6)
    print('Graphing complate')

    '''

    # makes a line graph of all data points IOT display iteration
    plt.plot(list(df['Range'])[:-1], v5, color='blue', marker='|')
    plt.title('Lightning strike', fontsize=14)
    plt.xlabel('Year', fontsize=1)
    plt.ylabel('Number Generated', fontsize=14)
    plt.grid(True)
    plt.show()

    '''

    test = []
    #data_list = df.values.tolist()

    #print(len(data_list))

    
    test.append(df['TestLatitude'].values.T.tolist())
    test.append(df['TestLongitude'].values.T.tolist())
    test.append(df['TestEllipseAngle'].values.T.tolist())
    test.append(df['TestNano'].values.T.tolist())


    test_class = [[], [], [], []]
    for i in range(0,4):
        for j in range(0,1000):
            test_class[i].append(DataPoint(row = i, data=int(test[i][j]), flag=0))
        print('added ' + str(i))


    r1 = test_class[0][0]
    r2 = test_class[1][0]
    r3 = test_class[2][0]
    r4 = test_class[3][0]
    print('r1 bellow')
    print(r1)
    
    output = []
    n = 1000
    # generate 20 random numbers
    for i in range(1000):

        
        r1_index = r1.get_next_index(test_class, 1000)
        r2_index = r2.get_next_index(test_class, 1000)
        r3_index = r3.get_next_index(test_class, 1000)
        r4_index = r4.get_next_index(test_class, 1000)
        
        r1 = test_class[0][r1_index]
        r1.flag = 1
        r2 = test_class[1][r2_index]
        r2.flag = 1
        r3 = test_class[2][r3_index]
        r3.flag = 1
        r4 = test_class[3][r4_index]
        r4.flag = 1


        number = r1.data + r2.data + r3.data + r4.data
        print(r1_index, r2_index, r3_index, r4_index, int(number))

        output.append(int(number))

    rang = list(range(0,len(output)))
    plt.scatter(output, rang)
    plt.show()
    
    print(f'Entrphy of V8: {entropy(output, base=len(output)):.5}')

    hisoComparison(v1, output, v5)






    

if __name__ == '__main__':
    main()
