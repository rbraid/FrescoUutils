from ROOT import TFile, TGraph, TGraphErrors
from array import array

def Average(g,low,high):
  debug = False

  npoints = 100
  irange = high-low
  rangeiter = irange/npoints

  if debug:
    print "Integrating from {} to {} in {} steps".format(low,high,npoints)

  isum = 0
  for n in range(npoints+1):
    tmp = g.Eval(low+n*rangeiter)
    isum += tmp
    #if debug:
      #print "{} evals to {}".format(low+n*rangeiter,tmp)

  #if debug:
    #print "Average is calculated as sum: {} / range: {} = {}".format(isum,irange,isum/irange)

  return isum/npoints

def Blur(graph):
  if graph.GetN() < 30:
    print "Caution, graph has few points, maybe you are grabbing the data by mistake?"

  ringGraph = ringFile.Get("COM_d1_s0_Be11")
  XArr = array('d')
  XErrArr = array('d')
  YArr = array('d')
  YErrArr = array('d')

  for point in range(ringGraph.GetN()):
    x = ringGraph.GetY()[point]
    xerr = (ringGraph.GetEYhigh()[point]+ringGraph.GetEYlow()[point])/2
    tmp = Average(graph,x-xerr,x+xerr)
    XArr.append(x)
    XErrArr.append(xerr)
    YArr.append(tmp)
    YErrArr.append(0)

  #outGraph = TGraphErrors(len(XArr),XArr,YArr,XErrArr,YErrArr)
  outGraph = TGraph(len(XArr),XArr,YArr)
  outGraph.SetName(graph.GetName()+"_blurred")
  outGraph.SetTitle(graph.GetTitle()+" blurred")
  outGraph.Write()


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("inpath", help='Input Location & Name')
parser.add_argument("outpath", nargs="?" ,help='Output Location & Name',default = "blurFrescoOut.root")
args = parser.parse_args()

inFile = TFile.Open(args.inpath,"read")
if not inFile:
  print "Can't open {}".format(inpath)
  quit()

directory = "~/nuclear/mine/analysis/inputRootFiles/"
ringFile = TFile.Open(directory+"DumbRings.root","read")
if not ringFile:
  print "Can't open {}".format(directory+"DumbRings.root")
  quit()

outfile = TFile.Open(args.outpath,"recreate")

frescoGraph = inFile.Get("G1")
if not frescoGraph:
  print "Didn't find a G1 in the file"
  quit()
else:
  Blur(frescoGraph)

frescoGraph = inFile.Get("G3")
if not frescoGraph:
  print "Didn't find a G3 in the file"
else:
  Blur(frescoGraph)

