# Faraz Ahmad

# Information Retrieval 



import math
import sys

fname = ""
if (len(sys.argv) == 2):
	fname = sys.argv[1]
else:
	print "Correct format of running this is test.py [space] path_to_input_file"
	quit()



# dictionary of tuples i.e. Dictionary<int, Tuple<float,float>>
# Dictionary<point#, Tuple<f1, f2>>
points = {} 

# dictionary of dictionaries i.e. Dictionary<int, Dictionary<int,float>>
# Dictionary<point#, Dictionary<point#, distance>>
distances = {}  

# dictionary of sets i.e. Dictionary<int, Hashset<int>>
# Dictionary<point#, Hashset<point#>>
mergings = {} 

def computeDistance(p1,p2):
	return math.sqrt(math.pow((points[p1][0]-points[p2][0]),2) + 
			math.pow((points[p1][1]-points[p2][1]),2))

def getClosestPoints(dstncs):
	minn = float("inf")
	p1 = 0; p2 = 0
	keylist = dstncs.keys()
	for key in keylist:
		nextkeylist = dstncs[key].keys()
		for k in nextkeylist:
			if(dstncs[key][k] != float("inf") and dstncs[key][k] < minn):
				minn = dstncs[key][k]
				p1 = key; p2 = k

	dstncs[p1][p2] = float("inf")
	return p1, p2, minn

def merge(p1, p2):
	mergings[p1] = mergings[p1] | mergings[p2]
	for val in mergings[p1]:
		mergings[val] = mergings[val] | mergings[p1]

def syncDistances(p1, p2, mrgngs):
	for key in mrgngs[p1]:
		for k in mrgngs[p1]:
			if(k>key and distances.get(key,-1)!=-1):
				distances[key][k] = float("inf")


try:
	fh = open(fname)
except:
	print "No such file found, please check and enter correct path to text file"
	quit()
	
# initialize points and mergings dictionaries
i = 0;
for line in fh:
	# print line
	words = line.split()
	if words == [] : continue
	elif len(words) == 2:
		f1 = float(words[0])
		f2 = float(words[1])
		points[i] = (f1, f2)
		mergings[i] = set([i])
		i = i + 1	
		# print f1 + "---" + f2

# print points

# initialize distances 
keylist = points.keys()
keylist.remove(keylist[len(keylist)-1])
for key in keylist:
	i = key+1
	while i<len(keylist)+1:
		if(distances.get(key,-1) == -1):
			distances[key] = {i:computeDistance(key, i)}
		else:
			distances[key][i] = computeDistance(key, i)
		i = i + 1

f = open("distance.txt", 'w')
keylist = distances.keys()
dist = []
for key in keylist:
	# f.write(str(key) + ": "+ str(distances[key]))
	for v in distances[key].values():
		dist.append(v)
dist.sort()
f.write(str(dist))
f.close()

# clustering ...
noOfPoints = len(points)
clustersMade = 0
clustersCounter = 0
THRESHOLD = float("inf") # THRESHOLD = 125

f = open('output.txt','w')
step = 1;
while clustersCounter != noOfPoints - 1:
	p1,p2,pdist = getClosestPoints(distances)
	if pdist < THRESHOLD:
		print "Step", step, ":", list(mergings[p1]), "+", list(mergings[p2])
		f.write("Step " + str(step) + ": " + str(list(mergings[p1])) + " + " + str(list(mergings[p2])))
		f.write("\n")
		step = step + 1
		merge(p1, p2)
		syncDistances(p1, p2, mergings)
		clustersMade = clustersMade + 1
	clustersCounter = clustersCounter + 1
print "Step", step, ":", list(mergings[p1]), "+", list(mergings[p2])
f.write("Step " + str(step) + ": " + str(list(mergings[p1])) + " + " + str(list(mergings[p2])))
# f.write('hi there\n') # python will convert \n to os.linesep

f.close()

print clustersMade

