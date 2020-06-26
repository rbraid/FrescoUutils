from ROOT import TGraph, TGraphErrors, TFile, TMultiGraph, TCanvas, TLegend
import ROOT
from array import array

# def Chop(graph):
#   if not graph:
#     return
#
#   ArrX = array('d')
#   ArrY = array('d')
#   ArrXErr = array('d')
#   ArrYErr = array('d')
#
#   for point in range(graph.GetN()):
#     xtmp = ROOT.Double(0)
#     ytmp = ROOT.Double(0)
#     graph.GetPoint(point,xtmp,ytmp)
#     extmp = graph.GetErrorX(point)
#     eytmp = graph.GetErrorY(point)
#
#     if xtmp < 100:
#       ArrX.append(xtmp)
#       ArrY.append(ytmp)
#       ArrXErr.append(extmp)
#       ArrYErr.append(eytmp)
#
#   tmpG = TGraphErrors(len(ArrX),ArrX,ArrY,ArrXErr,ArrYErr)
#   tmpG.SetName(graph.GetName()+"chopped")
#   tmpG.SetTitle(graph.GetTitle())
#   tmpG.GetXaxis().SetTitle(graph.GetXaxis().GetTitle())
#   tmpG.GetYaxis().SetTitle(graph.GetYaxis().GetTitle())
#   #tmpG.Write()
#   return tmpG


def FrescoDraw(title, name, beforeGraph,afterGraph,blurGraph,dataGraph):

  MG = TMultiGraph()
  MG.SetTitle("Fresco Results;Center of Mass Angle in Degrees;Cross Section in mb/sr")
  MG.SetTitle(title)
  MG.SetName(name)
  legend = ROOT.TLegend(0.65,.65,.9,.9)

  # afterGraph = Chop(afterGraph)
  if coulombH:
    coulombH.SetMarkerColor(ROOT.kWhite)
    coulombH.SetLineColor(ROOT.kRed)
    coulombH.SetLineStyle(10)
    coulombH.SetFillColor(ROOT.kWhite)
    coulombH.SetMarkerStyle(20)
    MG.Add(coulombH,"L")
    legend.AddEntry(coulombH,"Coulomb Only")

  if beforeGraph:
    beforeGraph.SetMarkerColor(ROOT.kWhite)
    beforeGraph.SetLineColor(ROOT.kBlack)
    beforeGraph.SetFillColor(ROOT.kWhite)
    beforeGraph.SetMarkerStyle(20)
    MG.Add(beforeGraph,"L")
    legend.AddEntry(beforeGraph,"Before sfresco Fit")

  MG.Draw("al*")
  # if args.rRuth:
  #   canvas.SetLogy(0)
  # else:
  canvas.SetLogy()

  MG.GetXaxis().SetTitle("Center of Mass Angle in Degrees")
  MG.GetYaxis().SetTitle("Cross Section in mb/sr")
  MG.Draw()
  legend.Draw()

  if args.rRuth:
    canvas.SaveAs("aa_{}_before_ruth.png".format(name))
  else:
    canvas.SaveAs("aa_{}_before.png".format(name))


  if afterGraph:
    afterGraph.SetMarkerColor(ROOT.kWhite)
    afterGraph.SetLineColor(ROOT.kGreen)
    afterGraph.SetFillColor(ROOT.kWhite)
    afterGraph.SetMarkerStyle(20)
    MG.Add(afterGraph,"L")
    legend.AddEntry(afterGraph,"After sfresco Fit")

  if blurGraph:
    blurGraph.SetMarkerColor(ROOT.kGreen)
    blurGraph.SetLineColor(ROOT.kWhite)
    blurGraph.SetFillColor(ROOT.kWhite)
    blurGraph.SetMarkerStyle(20)
    MG.Add(blurGraph,"P")
    legend.AddEntry(blurGraph,"Blurred sfresco Fit")

  if dataGraph:
    dataGraph.SetMarkerColor(ROOT.kBlue)
    dataGraph.SetLineColor(ROOT.kBlue)
    dataGraph.SetFillColor(ROOT.kWhite)
    dataGraph.SetMarkerStyle(20)
    MG.Add(dataGraph,"P")
    legend.AddEntry(dataGraph,"Data")


  MG.Draw()
  # if args.rRuth:
  #   canvas.SetLogy(0)
  # else:
  canvas.SetLogy()
  MG.GetXaxis().SetTitle("Center of Mass Angle in Degrees")
  MG.GetYaxis().SetTitle("Cross Section in mb/sr")
  MG.Draw()
  legend.Draw()

  if args.rRuth:
    canvas.SaveAs("aa_{}_ruth.png".format(name))
  else:
    canvas.SaveAs("aa_{}.png".format(name))

  # return MG


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help='Expects "Full", "Optical", or "Param"')
parser.add_argument("rRuth", help="Ratio to Rutherford?")
parser.add_argument("extras", nargs='?', default=False)
args = parser.parse_args()

if args.mode.lower() == "param":
  if not args.extras:
    print "Trying to run in param mode without specifying where to look.  Aborting plotter.py"
    quit()

if args.rRuth == "True" or args.rRuth == "TRUE":
    args.rRuth = True
else:
    args.rRuth = False

if(args.mode.lower() == "full" or args.mode.lower() == "param"):
  beforeF = TFile.Open("elastic_before.root","read")
  if args.rRuth:
    beforeF=TFile.Open("elastic_rRuth_before.root","read")
elif(args.mode.lower() == "optical"):
  beforeF = TFile.Open("elastic_opticalOnly_before.root","read")

coulombF=TFile.Open("../coulombOnly.root","read")
coulombH = False
if not coulombF:
  print "coulomb File not found"
  coulombF = False
elif args.rRuth:
  coulombF = False
else:
  coulombH = coulombF.Get("G1")

if not beforeF:
  print "beforeF not found"

if(args.mode.lower() == "full"):
  afterF = TFile.Open("elastic_after.root","read")
  if args.rRuth:
    afterF=TFile.Open("elastic_rRuth_after.root","read")
elif(args.mode.lower() == "optical"):
  afterF = TFile.Open("elastic_opticalOnly_after.root","read")
elif args.mode.lower() == "param":
  afterF = TFile.Open("elastic_after_{}.root".format(args.extras),"read")

if not afterF:
  print "afterF not found"

if(args.mode.lower() == "full"):
  #blurF = TFile.Open("blurred_after.root","read")
  blurF = False
elif(args.mode.lower() == "optical"):
  blurF = TFile.Open("blurred_opticalOnly_after.root","read")
elif args.mode.lower() == "param":
  blurF = False

#normF = TFile.Open("elastic_opticalOnly_norm.root","read")
#if not normF:
  #print "normF not found"

if blurF:
  tmpB = blurF.Get("G1_blurred")
else:
  tmpB = False

tmpTitle= "Elastic Scattering"
if args.extras:
  tmpTitle += " {}".format(args.extras)
tmpName = "elastic"
if args.extras:
  tmpName += "_{}".format(args.extras)


canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)
# canvas.Divide(2,1)

# def FrescoDraw(title, name, beforeGraph,afterGraph,blurGraph,dataGraph):
if args.rRuth:
    FrescoDraw(tmpTitle, tmpName, beforeF.Get("G1"), afterF.Get("G1"), tmpB, afterF.Get("G0"))
else:
    FrescoDraw(tmpTitle, tmpName, beforeF.Get("G0"), afterF.Get("G1"), tmpB, afterF.Get("G0"))


#tmpMGa.Draw()

# if blurF:
#   tmpB = blurF.Get("G3_blurred")
# else:
#   tmpB = False
#
# tmpTitle= "Inelastic Scattering"
# if args.extras:
#   tmpTitle += " {}".format(args.extras)
# tmpName = "inelastic"
# if args.extras:
#   tmpName += "_{}".format(args.extras)
#
# tmpMG = FrescoDraw(tmpTitle, tmpName, beforeF.Get("G1"), afterF.Get("G3"), tmpB, afterF.Get("G2"))
# pad = canvas.cd(2)
# tmpMG.Draw("al*")
# pad.SetLogy()
#tmpMG.Draw()

# if(args.mode.lower() == "full"):
#   canvas.SaveAs("aa_Scattering.png")
# elif(args.mode.lower() == "param"):
#   canvas.SaveAs("Scattering_{}.png".format(args.extras))
# elif(args.mode.lower() == "optical"):
#   canvas.SaveAs("scattering_opticalOnly.png")

