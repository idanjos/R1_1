
import argparse
import os


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

def main():
	args = parseArguments()
	inputFiles = getFiles(args.folder)
	docid = 0
	pmids = []
	for i in inputFiles:
		#indexBlock += 1
		print(i)
		with open(i,"r",errors="ignore") as f:
			
			for line in f:
				#print(text)
				#Saving PMID for future use, I am not 100% certain
				if "PMID-" in line:		
					pmid = line.split(" ")[1]
					pmids += [(docid,pmid)]
					docid += 1

	outputfile = open("pmid/pmids.txt","w")
	for p in pmids:
		outputfile.write(str(p[0])+":"+p[1])
	outputfile.close()

main()				
				