from itertools import combinations
import csv
def read_csv(csvfilename):
    """
    Reads a csv file and returns a list of list
    containing rows in the csv file and its entries.

    CSV file first row is header
    2nd row onwards if data

    """
    rows = []

    with open(csvfilename, encoding='utf-8') as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows.append(row)
    return rows

#inputs 2 numbers, gives me a range of numbers

def expand(start,end):
    var = []
    start = int(start)
    end = int(end)
    for i in range(start,end):
        var.append(i)
    return var

def classify(modules):
    dictionary = {'1':0,'2':0,'3':0,'4':0}
    for mod in modules:
        dictionary[mod[3]] += 1
    return dictionary


#Reads df
#index:
'''
0 = module code
1 = day of the week, 1 = Monday, 5 = Friday for 1st slot
2 = start time of mod for 1st slot
3 = end time of mod for 1st slot

4 = day of the week, 1 = Monday, 5 = Friday for 2nd slot
5 = start time of mod for 2nd slot
6 = end time of mod for 2nd slot

7 = day of the week, 1 = Monday, 5 = Friday for 3rd slot
8 = start time of mod for 3rd slot
9 = end time of mod for 3rd slot

10 = day of the week, 1 = Monday, 5 = Friday for 4th slot
11 = start time of mod for 4th slot
12 = end time of mod for 4th slot

'''
df = read_csv('mods1.csv')
df = df[1:]
#print(df)

def timetable(df):
    #--Initialise Timetable matrix--#
    #Init day row first
    row = [0 for j in range(10)]

    #init 5 days
    wk = [row.copy() for j in range(5)]
    #print(df)
    for mod in df:
        #print('new')
        #for day in wk:
            #print(day)

        #this gives me a list of things to populate the matrix with
        expanded_time = expand(mod[2],mod[3])
        for period in expanded_time:
            if wk[int(mod[1])-1][int(period)-8] == 0:
                wk[int(mod[1])-1][int(period)-8] = mod[0]
            else:
                #print(f"CONFLICT WITH {mod[0]} and {wk[int(mod[1])-1][int(period)-8]}")
                return 'CONFLICT'



        if int(mod[4]) == 0:
            continue
        expanded_time = expand(mod[5],mod[6])
        for period in expanded_time:
            if wk[int(mod[4])-1][int(period)-8] == 0:
                wk[int(mod[4])-1][int(period)-8] = mod[0]
            else:
                #print(f"CONFLICT WITH {mod[0]} and {wk[int(mod[4])-1][int(period)-8]}")
                return 'CONFLICT'


        if int(mod[7]) == 0:
            continue
        expanded_time = expand(mod[8],mod[9])
        for period in expanded_time:
            if wk[int(mod[7])-1][int(period)-8] == 0:
                wk[int(mod[7])-1][int(period)-8] = mod[0]
            else:
                #print(f"CONFLICT WITH {mod[0]} and {wk[int(mod[7])-1][int(period)-8]}")
                return 'CONFLICT'


        if int(mod[10]) == 0:
            continue
        expanded_time = expand(mod[11],mod[11])
        for period in expanded_time:
            if wk[int(mod[10])-1][int(period)-8] == 0:
                wk[int(mod[10])-1][int(period)-8] = mod[0]
            else:
                #print(f"CONFLICT WITH {mod[0]} and {wk[int(mod[10])-1][int(period)-8]}")
                return 'CONFLICT'


    lst = []
    print('\n')
    for day in wk:
        print(day)
        for mod in day:
            if mod != 0:
                if mod not in lst:
                    lst.append(mod)

    print(f'Mods: {lst}')
    #print('PASS')
    return lst

N_mods = 5


combi = []

for mm in combinations(df,N_mods):
    #print(mm)
    switch = 0

    for i in range(N_mods):
        for j in range(i+1,N_mods):
            if mm[i][0] == mm[j][0]:
                switch = 1

    if switch == 0:
        combi.append(mm)


mods_lst = []

for mm in combi:
    ml = timetable(mm)
    if ml != 'CONFLICT':
        if sorted(ml) not in mods_lst:
            mods_lst.append(sorted(ml))

##Further selection Criteria##

#Below are maximum mods of 1k,2k,3k,4k mods you wanna take in a sem
N_4k = 4
N_3k = 2
N_2k = 4
N_1k = 1

print('\nList of Mods you can take')
for lst_mods in mods_lst:
    ddict = classify(lst_mods)
    if ddict['4'] <= N_4k and ddict['3'] <= N_3k and ddict['2'] <= N_2k and ddict['1'] <= N_1k:
        print(lst_mods)