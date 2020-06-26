from ROOT import TFile, TGraph, TGraphErrors
from array import array

def is_float(s):
  try:
      float(s)
      return True
  except ValueError:
      return False

def MakeGraph(mgX,mgY):
  assert len(mgX) == len(mgY),"X and Y lengths not equal"
     
  graph = TGraph(len(mgX),mgX,mgY)

  #graph.GetXaxis().SetTitle(xAxis)
  #graph.GetYaxis().SetTitle(yAxis)
  #graph.SetTitle(title+" "+legend)
  #graph.SetName(title+" "+legend)
  #print "Created {}".format(graph.GetTitle())
  outfile.cd()
  graph.Write()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("inpath", help='Input Location & Name')
parser.add_argument("outpath", help='Output Location & Name')
args = parser.parse_args()
#print "Arguments Parsed"

infile = open(args.inpath,'r')
outfile = TFile.Open(args.outpath,"recreate")

if not infile:
  print "Failed to open infile: {}".format(args.inpath)
  
if not outfile:
  print "Failed to open outfile: {}".format(args.outpath)

data = False
x, y= array( 'd' ), array( 'd' )
  
prvX = 0

for line in infile:
  if "CROSS SECTIONS FOR" in line:
    data = True
    continue
  
  if data:
    if "Integrated" in line:
      data = False
      MakeGraph(x,y)
      x, y= array( 'd' ), array( 'd' )
      prvX = 0
      continue
    if "/R" in line:
      continue
    
    bits = line.split()
    if len(bits) < 1:
      continue
    #print "***************"
    #print line
    #print "len(bits): {}".format(len(bits))

    #for bit in bits:
      #print bit
    #print "Pulling x: {}, y: {}".format(bits[0],bits[4])
    
    assert is_float(bits[0]), "Pulling non-float {} for x".format(bits[0])
    assert is_float(bits[4]), "Pulling non-float {} for y".format(bits[4])
    
    if float(bits[0]) > prvX:
      #print "{} > {}".format(float(bits[0]),prvX)
      prvX = float(bits[0])
    else:
      #data = False
      MakeGraph(x,y)
      x, y= array( 'd' ), array( 'd' )
      prvX = 0
      continue
    
    x.append(float(bits[0]))
    y.append(float(bits[4]))


