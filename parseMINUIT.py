import argparse

def printHeader():
  #outFile.write("r0C,V,r0,d,VI,r0I,dI,Vso,r0so,dso,surfV,surfR,surfA,")
  #outFile.write("r0C,V,r0,d,VI,r0I,dI,Vso,r0so,dso,surfV,surfR,surfA,")
  #outFile.write("Total ChiSquare, ChiSquare Elastic, ChiSquare Inelastic\n")
  outFile.write("norm_init,r0C,V_vol,r0_vol,d_vol,W_surf,rW_surf,aW_surf,V_so,r0_so,d_so,")
  outFile.write("norm,r0C_fit,V_vol_fit,r0_vol_fit,d_vol_fit,W_surf_fit,rW_surf_fit,aW_surf_fit,V_so_fit,r0_so_fit,d_so_fit,")
  outFile.write("Total_ChiSquare\n")

def Condense(myList):
  chiList = []
  goodMIGRANDList = []
  badMIGRANDList = []

  for item in myList:
    if "ChiSq/N" in item:
      if item.strip().split()[2] != '=':
        chiList.append(item)
    elif "r0" in item and "W" in item:
      goodMIGRANDList.append(item)
    else:
      print "Killing: "
      print item
      badMIGRANDList.append(item)



  if len(chiList) < 1:
    #print "Error in Condense: No chiList detected"
    return False

  if len(goodMIGRANDList) < 2:
    print "Error in Condense: Not enough Good MIGRAND prints"
    return False

  tmpList = []
  #if len(myList) >=2 :
    #tmpList.append(myList[0])
    #tmpList.append(myList[-1])
  tmpList.append(goodMIGRANDList[0])
  tmpList.append(goodMIGRANDList[-1])
  tmpList.append(chiList[-1])

  return tmpList

def ingestDataFile(datafile):
  built = []
  intake = False

  if args.verbose:
    print "Ingesting"

  for line in datafile:
    if args.verbose:
        print line
    if "NO.   NAME         VALUE" in line or "NO.   NAME        VALUE" in line:
      intake = True
      tmpstr = str()
      #print "beginning intake"

    elif "STATUS=FAILED" in line or "STATUS=CALL LIMIT" in line:
      if args.verbose:
        print "Killing Failure"
      # return False
    #elif "STATUS=" in line:
      #if "INITIATE" not in line and "OK" not in line and "CONVERGED" not in line:
        #print "Interesting Status: {}".format(line)

    elif "NO DATA POINTS" in line:
      return False

    elif "ChiSq/N" in line:
      built.append(line)

    elif intake:
      #print line
      #for ele in line.strip().split():
        #print ele

      if "MINUIT WARNING" in line:
        continue
      elif "===========" in line:
        continue

      elif len(line.strip().split()) < 3 or "ERR DEF" in line:
        #print "stopping intake"
        intake = False
        built.append(tmpstr)
        continue

      tmpstr += line
  if args.verbose:
     print "Built:"
     for asdf in built:
       print asdf
  return built

def breakDownAndOutput(output):
  for chunk in output:
    chunk = chunk.split("\n")
    for line in chunk:
      #print line
      if "ChiSq/N" in line:
        # outFile.write(line.strip().split()[2]+','+line.strip().split()[4]+','+line.strip().split()[5])  #This line pulls both elastic and inelastic
        outFile.write(line.strip().split()[2])
      elif len(line.strip().split()) <= 0:
        continue
      elif line.strip().split()[2] == "'":
        outFile.write(line.strip().split()[3]+',')
      else:
        outFile.write(line.strip().split()[2]+',')

  outFile.write("\n")

parser = argparse.ArgumentParser()
parser.add_argument("FILE", help="Files to pull from", nargs="+")
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

if args.verbose:
  print "Verbose"

outFile = file('output.csv','w')

printHeader()

for curFileString in args.FILE:
  tmpFile = file(curFileString)

  GoodStuff = ingestDataFile(tmpFile)
  if GoodStuff == False:
    continue
  #print "After ingestion"
  #for chunk in GoodStuff:
    #print chunk
    #print "\n"

  GoodStuffTM = Condense(GoodStuff)
  if GoodStuffTM == False:
    continue

  #print "After Condensing"
  #for chunk in GoodStuffTM:
    #print chunk
    #print "\n"

  breakDownAndOutput(GoodStuffTM)

