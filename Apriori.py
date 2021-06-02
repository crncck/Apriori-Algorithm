import itertools
from collections import Counter
import pandas as pd
import sys

def getTransactions(path, transactions):
    C1 = []
    with open(path, "r") as filestream:
        for x, line in enumerate(filestream):
            currentLine = line.split(",")
            lineSet = set()
            for i in currentLine:
                lineSet.add(i.rstrip("\n"))
                # init pass to C1
                C1.append(i.rstrip("\n"))
            # get transactions
            transactions[x] = lineSet

    return C1

def getXlsxTransactions(path, transactions):
    data_frame = pd.read_excel(path, engine='openpyxl')
    del data_frame['Unnamed: 2']
    df_grouped = data_frame.groupby(data_frame['Transaction ID'])['Product ID'].apply(set)

    C1 = []
    for index, value in df_grouped.items():
        for item in value:
            C1.append(item)
        transactions[index] = value
    return C1


#to delete last comma from print statement
def deleteLastComma():
    sys.stdout.write("\033[A")
    sys.stdout.write('\b\b')
    print(" ")
    sys.stdout.flush()


def getF1(itemCounts, n, minSup):
    F1 = {}
    for item in itemCounts:
        itemSet = frozenset([item])
        # add items whose count/n value is greater than or equal to the minimum support
        if itemCounts[item]/n > minSup or itemCounts[item]/n == minSup:
            F1[itemSet] = itemCounts[item]
    return F1


def candidate_gen(F, k):
    Ck = {}
    count = 0
    for a in F:
        for b in F:
            a = sorted(a)
            b = sorted(b)
            # check pairs of frequent itemsets that only differ in the last item
            if a[:k-2] == b[:k-2] and a[k-2] < b[k-2]:
                c = frozenset(a + b)
                Ck[c] = 0
                count = count + 1
                # for each k-1 subset s of c check if it is in Fk-1, if not delete the c from Candidate set (Ck)
                for s in itertools.combinations(c, k-1):
                    flag = False
                    for x in F:
                        if tuple(x) == s:
                            flag = True
                if not flag:
                    del Ck[c]

    return Ck


def main():
    transactions = {}

    file_name = "Transactions.txt"
    file_type = file_name.split(".", 1)[1]

    # get C1 and transactions from file
    if file_type == 'txt':
        C1 = getTransactions(file_name, transactions)
        #sys.stdout = open('txt_output.txt', 'w')
        # minimum support value
        minSup = 30/100

    elif file_type == 'xlsx':
        C1 = getXlsxTransactions(file_name, transactions)
        #sys.stdout = open('xlsx_output.txt', 'w')
        minSup = 1/100

    itemCounts = Counter(C1)
    n = len(transactions)

    print("File: ", file_name, "\nMinimum Support Value: ", minSup, "\nNumber of transactions: ", n)

    # get F1
    F = getF1(itemCounts, n, minSup)
    print("\nF1:")
    for key in F:
        print(set(key), ":", F[key], sep='', end=', ', flush=True)
    deleteLastComma()

    k = 2
    while len(F) != 0:
        C = candidate_gen(F, k)
        print("\n\nC{}:".format(k))
        for c in C:
            print(set(c), sep='', end=', ', flush=True)
            count = 0
            # check the number of c in transactions
            for t in transactions:
                if c.issubset(transactions[t]):
                    count = count + 1
            C[c] = count
        deleteLastComma()
        F = {}
        for c in C:
            # if c.count/n is greater than or equal to minimum support value add c to Fk
            if C[c] / n > minSup or C[c] / n == minSup:
                F[c] = C[c]

        print("\n\nF{}: ".format(k))
        for key in F:
            print(set(key), ":", F[key], sep='', end=', ', flush=True)
        deleteLastComma()
        k = k + 1

    #sys.stdout.close()


if __name__ == '__main__':
    main()
