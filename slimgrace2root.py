from ROOT import TFile, TGraph, TGraphErrors
from array import array

def is_float(s):
  try:
      float(s)
      return True
  except ValueError:
      return False

def MakeGraph(mgX,mgY,mgXerr,mgYerr,nw):
  assert len(mgX) == len(mgY),"X and Y lengths not equal"
  assert len(mgXerr) == len(mgYerr),"Xerr and Yerr lengths not equal"
  assert len(mgX) == len(mgXerr),"X and Xerr lengths not equal"

  Yerrs = False
  for err in mgYerr:
    if err >0:
      Yerrs = True

  graph = TGraph(len(mgX),mgX,mgY)
  if Yerrs:
    graph = TGraphErrors(len(mgX),mgX,mgY,mgXerr,mgYerr)
  #graph.GetXaxis().SetTitle(xAxis)
  #graph.GetYaxis().SetTitle(yAxis)
  #graph.SetTitle(title+" "+legend)
  graph.SetName("G{}".format(nw))
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
x, y, xerr, yerr= array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
nWrites = 0

for line in infile:
  bits = line.split()

  if len(bits) <2:
    if data:
      data = False
      MakeGraph(x,y,xerr,yerr,nWrites)
      nWrites += 1
      x, y, xerr, yerr= array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )

  elif is_float(bits[0]) and is_float(bits[1]):
    data = True
    x.append(float(bits[0]))
    y.append(float(bits[1]))
    xerr.append(float(0))
    appendval = float(0)
    if len(bits) > 2:
      if is_float(bits[2]):
        appendval = float(bits[2])
    yerr.append(appendval)

  else:
    if data:
      data = False
      MakeGraph(x,y,xerr,yerr,nWrites)
      nWrites += 1
      x, y, xerr, yerr= array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )

