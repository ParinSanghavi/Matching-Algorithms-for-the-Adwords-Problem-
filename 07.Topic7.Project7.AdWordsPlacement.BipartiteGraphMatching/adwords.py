import sys
import csv
import math
from random import shuffle
import random

if len(sys.argv) != 2:
	sys.exit(1)  
algo = sys.argv[1]

def Advertisers(a,b):
	aList = []
	for i in a:
		if b[i[0]] >= float(i[2]):
			aList.append(i)
	return aList

def Greedy(aList):
	return [i for i in aList if i[2] == max(i[2] for i in aList)][0]
	
def Msvv(aList,b,dummy):
	highest = 0.0
	dum = []
	for i in aList:
		temp = 1 - math.exp((dummy[i[0]]-b[i[0]])/dummy[i[0]]-1)
		if (float(i[2]) * temp) > highest:
			highest = (float(i[2]) * temp)
			dum = i
	return dum
	
def Balance(aList,b):
	highest = 0.0
	dum = []
	for i in aList:
		if b[i[0]] > highest:
			highest = b[i[0]]
			dum = i
	return dum

# Completing csv file tasks		
csvFile = open("bidder_dataset.csv")
bidder = []
for i in csv.reader(csvFile):   
	bidder.append(i)    

b = {}
for i in bidder[1:]:
	if(i[3]):
		b[i[0]] = float(i[3])
ib = b.copy()
calculated = sum(b.values())

# Completing queries file task
qFile = open("queries.txt")
queries = []
for i in qFile:
	queries.append(i.replace("\n",""))

# Part 1
cR = 0.0
for q in queries:
	aList = Advertisers([x for x in bidder if x[1] == q],b)
	
	if len(aList) >= 1:
		if algo == "greedy":
			chosen = Greedy(aList)
		elif algo == "msvv":
			chosen = Msvv(aList,b,ib)
		elif algo == "balance":
			chosen = Balance(aList,b)

		tem = float(chosen[2])
		cR += tem
		b[chosen[0]] -= tem

print "Calculated revenue is:" + str(cR)

# Part 2
rList = []
random.seed(0)

for i in range(1,101):
	
	temp = 0.0
	shuffle(queries)
	b = ib.copy()

	for q in queries:
		aList = Advertisers([x for x in bidder if x[1] == q],b)
		
		if len(aList) >= 1:
			if algo == "greedy":
				chosen = Greedy(aList)
			elif algo == "msvv":
				chosen = Msvv(aList,b,ib)
			elif algo == "balance":
				chosen = Balance(aList,b)

			
			tem = float(chosen[2])
			temp += tem
			b[chosen[0]] -= tem
			
	rList.append(temp)

print "Estimation of competitive ratio is: " + str(min(rList)/calculated)