import time
import VRPTW
import BaseCase
import csv

def maxTime(times):
    maxTime = 0
    for clusterTime in times:
        maxTime = max(maxTime, clusterTime)
    return maxTime

solveTimesNew = []
solveTimesOld = []
timeTakenNew = []
timeTakenOld = []
typesOfData = ["R", "C", "RC"]
fileNames = []
for type in typesOfData:
    for i in range(1, 3):
        for j in range(1, 6):
            #Add Other Variations of Data Here
            fileName = "TestCases/Synopsys Solomon Data - " + type + str(i) + "0" + str(j)
            fileNames.append(fileName)

            startTime = time.time()
            times = VRPTW.main(fileName)
            solveTimesNew.append(time.time() - startTime)
            timeTakenNew.append(maxTime(times))

            startTime = time.time()
            times = BaseCase.main(fileName)
            solveTimesOld.append(time.time() - startTime)
            timeTakenOld.append(maxTime(times))
            print("Finished: " + fileName)

with open('base.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(['FileName', 'SolveTime', 'MaxTime'])
    for i in range(len(fileNames)):
        writer.writerow([fileNames[i], solveTimesOld[i], timeTakenOld[i]])


    # write the data
print("Finished")
