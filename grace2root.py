from ROOT import TFile, TGraph
from array import array

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("inpath", help='Input Location & Name')
parser.add_argument("outpath", help='Output Location & Name')
args = parser.parse_args()
print "Arguments Parsed"

infile = open(args.inpath,'r')
outfile = TFile.Open(args.outpath,"recreate")

if not infile:
  print "Failed to open infile: {}".format(args.inpath)
  
if not outfile:
  print "Failed to open outfile: {}".format(args.outpath)
  
title = "unset"
xAxis = "unset"
yAxis = "unset"
legend = "unset"
data = False
x, y = array( 'd' ), array( 'd' )
  
for line in infile:
  if 'END' in line:
    data = False
    graph = TGraph(len(x),x,y)
    graph.GetXaxis().SetTitle(xAxis)
    graph.GetYaxis().SetTitle(yAxis)
    graph.SetTitle(title+" "+legend)
    graph.SetName(title+" "+legend)
    print "Created {}".format(graph.GetTitle())
    outfile.cd()
    graph.Write()

    x, y = array( 'd' ), array( 'd' )
    
    data = True

  elif data:
    print line
    tmp = line.split()
    x.append(float(tmp[0]))
    y.append(float(tmp[1]))
    #print "{},".format(float(tmp[1])),
    
  elif '@subtitle' in line:
    if '"' in line:
      title = line.split('"')[1]
      title.strip()
  elif '@xaxis label' in line:
    xAxis = line.split('"')[1]
    xAxis.strip()
  elif '@yaxis label' in line:
    yAxis = line.split('"')[1]
    yAxis.strip()
  elif '@legend string' in line:
    legend = line.split('"')[1]
    legend.strip()
  elif 'Theta' in line:
    data = True

  #else:
    #print "Throwing out: "+line
