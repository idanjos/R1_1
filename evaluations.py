import pprint
import os
import argparse
import Relevancy
#Argument parser
def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()
   

    # Optional arguments
       
    parser.add_argument("-f", "--folder", help="Directory of files", type=str, default="test")
 
   
    # Print version
    parser.add_argument("--version", action="version", version='%(prog)s - Version 3.0')

    # Parse arguments
    args = parser.parse_args()
   


    return args

#Now loads all files from input folder
def getFiles(path):
	if path[-1] == "/":
		path = path[0:-1]
	if not os.path.isdir(path):
		return [path]
	files = os.listdir(path)
	output = []
	for file in files:
		if os.path.isdir(path+"/"+file):
			output += getFiles(path+"/"+file)
			continue
		if path[-1] == "/":
			
			output += [path+file]
		else:
			output += [path+"/"+file]
	return output


def main(args):
	queryResults = getFiles("queryResults")
	#print(queryResults)
	r = Relevancy.Relevancy()
	table = dict()
	for query in queryResults:
		print("Processing "+query)
		with open(query,"r") as f:
			data = []
			for line in f:
				data += [line.strip()]
			data[2] = float(data[2])
			data[1] = eval(data[1])
			data[0] = data[0][0:3]
			index = query.split(".")[0].split("query")[-1]
			r.addTime(data[2])
			r.setResult(data,index)
			table[index] = [] + list(r.getSimpleMetrics()) + [r.getNDCG()]
			
		
	pprint.pprint(table)
	mean = [0,0,0,0,0]
	for i in range(1,51):
		mean[0] += table[str(i)][0]
		mean[1] += table[str(i)][1]
		mean[2] += table[str(i)][2]
		mean[3] += table[str(i)][3]
		mean[4] += table[str(i)][4]
		print(str(i)+":"+str(table[str(i)]))
	mean[0] /= 50
	mean[1] /= 50
	mean[2] /= 50
	mean[3] /= 50
	mean[4] /= 50
	print(mean)
	pass

if __name__== "__main__":
	args = parseArguments()
	main(args)

