from ROOT import TGraph, TFile, TCanvas, TLegend, TGraphErrors
from array import array
from uncertainties import ufloat
import ROOT

def ScaleTGraph(graph):
  scalefactor = .80224E-04
  for i in range(graph.GetN()):
    graph.GetY()[i] *= scalefactor;
    graph.GetEY()[i] *= scalefactor
    graph.GetYaxis().SetTitle("Cross section in mb/sr")

  return graph

def backwardSplit(point1m, point2p):
    BR_1m_GS = ufloat(66,4)/100 #
    BR_1m_2p = ufloat(34,4)/100
    BR_2p_GS = ufloat(9,5)/100
    BR_2p_2p = ufloat(91,5)/100

    point5960 = point1m*BR_1m_GS + point2p*BR_2p_GS
    point2590 = point1m*BR_1m_2p + point2p*BR_2p_2p
    return [point2590.n, point5960.n]

def GetBackward(hlist):
    ArrX = array('d')
    ArrY2590 = array('d')
    ArrY5960 = array('d')

    if hlist[0].GetN() != hlist[1].GetN():
        print "unequal number of points in graphs in GetBackward"
        return False

    for point in range(hlist[0].GetN()):
        if int(hlist[0].GetX()[point]*100) != int(hlist[1].GetX()[point]*100):
            print "Mismatched X values! {} and {}".format(hlist[0].GetX()[point], hlist[1].GetX()[point])
            continue

        splitVals = backwardSplit(hlist[1].GetY()[point], hlist[0].GetY()[point])
        if splitVals:
            ArrX.append(hlist[0].GetX()[point])
            ArrY2590.append(splitVals[0])
            ArrY5960.append(splitVals[1])

    if len(ArrX) <= 0:
        return False

    G2590 = TGraph(len(ArrX),ArrX,ArrY2590)
    G2590.SetName("G2590")
    G2590.SetTitle("Back Calculated 2590 Peak from SFresco Varying Spectroscopic Amplitude;COM Angle in Degrees;Cross Section in mb/sr")
    G2590.Write()

    G5960 = TGraph(len(ArrX),ArrX,ArrY5960)
    G5960.SetName("G5960")
    G5960.SetTitle("Back Calculated 5960 Peak from SFresco Varying Spectroscopic Amplitude;COM Angle in Degrees;Cross Section in mb/sr")
    G5960.Write()

def DrawBackward(zipped):
    canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)
    leg = TLegend(.5,.65,.9,.9)
    canvas.SetLogy()
    for rawP, backP in zipped:
        Energy = 0
        color = ROOT.kRed
        if "2590" in rawP.GetName():
            Energy = 2590
            color = ROOT.kBlue
        elif "5960" in rawP.GetName():
            Energy = 5960
            color = ROOT.kOrange
        else:
            print "No energy detected in {}".format(rawP.GetName())

        rawP.SetLineColor(color)
        rawP.SetMarkerColor(color)
        rawP.SetMarkerStyle(20)
        rawP.SetFillColor(ROOT.kWhite)
        leg.AddEntry(rawP,"Raw {} Cut Angular Distribution Data".format(Energy))

        backP.SetLineWidth(2)
        backP.SetFillColor(ROOT.kWhite)
        leg.AddEntry(backP,"Back-Calculated from FRESCO and Branching Ratios")

        backP.SetTitle("Comparing {} Gamma Cut Data to The Weighted FRESCO Output".format(Energy))
        backP.Draw("AP")
        rawP.Draw("sameP")
        leg.Draw()
        canvas.SaveAs(backP.GetName()+"_check.png")

types = ["twoPlus","oneMinus"]
files = []
histos = []
for atype in types:
    tmpF= TFile.Open("{}.root".format(atype),"read")
    if not tmpF:
        print "No {}.root".format(atype)
        quit()
    files.append(tmpF)
    tmpG = tmpF.Get("G1")
    tmpG.SetName(atype)
    histos.append(tmpG)
outF = TFile.Open("backward.root","recreate")

GetBackward(histos)

rawPlots = []
backPlots = []
gamF = TFile.Open("~/nuclear/mine/rb/angulardistribution/gammaOut.root","read")
if not gamF:
    print "No gamF"
GamEnergies = [2590, 5960]
for GE in GamEnergies:
    tmpPlot = gamF.Get("AD_{}".format(GE))
    if not tmpPlot:
        print "No {}".format(GE)
    else:
        tmpPlot = ScaleTGraph(tmpPlot)
        rawPlots.append(tmpPlot)
    tmpPlot = outF.Get("G{}".format(GE))
    if not tmpPlot:
        print "No backward {}".format(GE)
    else:
        backPlots.append(tmpPlot)
zipPlots = zip(rawPlots,backPlots)
DrawBackward(zipPlots)
