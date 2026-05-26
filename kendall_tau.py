import csv
from sys import argv
import scipy

DEBUG = False

def main():
    if len(argv) != 4:
        print("usage kendall <file.csv> <X> <Y> where X and Y are which prototype you want and not the same")


    test = []
    X = []
    Y = []
    with open(argv[1], "r") as csv_file: #get file name and grade for 2 prototype
        file = csv.reader(csv_file)
        for line in file:
            if "File" not in line:
                X.append(line[int(argv[2])])
                Y.append(line[int(argv[3])])

    n = len(X)

    for i in range(n):# if some of the value are integer we cast it into float 
        if not isinstance(X[i],int):
            X[i] = float(X[i])
        if not isinstance(Y[i],int):
            Y[i] = float(Y[i])
            

    rankX = [x for x in range(1,n+1)] #X ranking from 1 to X in order

    #bubble sort (yeah it's bad but it's like less than 20 element)
    #sort X and put the same order for the files and Y (the second prototypes)
    for i in range(n-1):
        for j in range(n-i-1):
            if X[j] > X[j+1]:
                X[j], X[j+1] = X[j+1], X[j]
                Y[j], Y[j+1] = Y[j+1], Y[j]

    # https://www.docstring.fr/glossaire/sorted/
    #give a rank to each index of Y
    sorted_Y_indice = sorted(range(n), key=lambda i: Y[i]) 

    rankY = [0] * n

    rank = 1
    for i in sorted_Y_indice:
        rankY[i] = rank
        rank += 1

    # print(Y)
    # print(sorted_Y_indice)
    # print(rankY)

    sum = 0
    for i in range(n-1):
        for j in range(i+1,n):
            if rankY[i] < rankY[j]:
                sum += 1
            else :
                sum -= 1
    
    if DEBUG:
        print(sorted_Y_indice)
        print(rankY)
        print(Y)
        print()
        print(rankX)
        print(X)
        print()

    print(sum/(n*(n-1))*2)
    #https://web.archive.org/web/20181008171919/https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kendalltau.html
    print(scipy.stats.kendalltau(rankX,rankY))


if __name__== "__main__":   
    main()