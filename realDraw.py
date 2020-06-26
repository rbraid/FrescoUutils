from ROOT import TGraph, TFile, TCanvas, TLegend, TGraphErrors
from array import array
from uncertainties import ufloat
import ROOT

scalefactors = []
scalefactors.append(ufloat(0.65278E-04, 0.41625E-05)) #calulated from full elastic
scalefactors.append(ufloat(0.10617E-03,0.16718E-05)) #calculated from coulomb only but using all Points
scalefactors.append(ufloat(.80224E-04,0)) #calculated by forcing first data point to align with coulomb only fresco output.

scalefactors.append(ufloat(8.39E-05,2.07E-05))#Average and STDDev of above 3 items.

scalefactors.append(ufloat(0.40226E-04,0)) #normalizing to full elastic updated FRAC calculation
scalefactors.append(ufloat(5.75979686146e-05,0)) #normalizing to single point with updated calc


scalefactor = scalefactors[3]

def killXErr(graph):
  if not graph:
    return

  ArrX = array('d')
  ArrY = array('d')
  ArrXErr = array('d')
  ArrYErr = array('d')

  for point in range(graph.GetN()):
    ArrX.append(graph.GetX()[point])
    ArrY.append(graph.GetY()[point])
    ArrXErr.append(0)
    ArrYErr.append(graph.GetEY()[point])

  tmpG = TGraphErrors(len(ArrX),ArrX,ArrY,ArrXErr,ArrYErr)
  tmpG.SetName(graph.GetName()+"_noErr")
  tmpG.SetTitle(graph.GetTitle())
  tmpG.GetXaxis().SetTitle(graph.GetXaxis().GetTitle())
  tmpG.GetYaxis().SetTitle(graph.GetYaxis().GetTitle())
  #tmpG.Write()
  return tmpG

def SumGraphs(g1,g2,name,title):
  nPoints = g1.GetN()
  if g1.GetN() != g2.GetN():
    print "Mismatch in SumGraphs Points!"
    if g2.GetN() > nPoints:
      nPoints = g2.GetN()

  ArrX = array('d')
  ArrY = array('d')
  ArrXErr = array('d')
  ArrYErr = array('d')

  for gPoint in range(nPoints):
    if int(g1.GetX()[gPoint]*1000) != int(g2.GetX()[gPoint]*1000):
      print "Mismatch in X Values!"
      continue
    else:
      ArrX.append(g1.GetX()[gPoint])

    if int(g1.GetEX()[gPoint]*1000) != int(g2.GetEX()[gPoint]*1000):
      print "Mismatch in X Error Values!"
      continue
    else:
      ArrXErr.append(g1.GetEX()[gPoint])

    g1Y = ufloat(g1.GetY()[gPoint], g1.GetEY()[gPoint])
    g2Y = ufloat(g2.GetY()[gPoint], g2.GetEY()[gPoint])
    prod = g1Y*g2Y

    ArrY.append(prod.n)
    ArrYErr.append(prod.s)

  SumG = TGraphErrors(len(ArrX),ArrX,ArrY,ArrXErr,ArrYErr)
  SumG.SetName(name)
  SumG.SetTitle(title)

  return SumG

def ScaleTGraph(graph):
  for i in range(graph.GetN()):
    grVal = ufloat(graph.GetY()[i], graph.GetEY()[i])
    newVal = grVal*scalefactor
    graph.GetY()[i] = newVal.n
    graph.GetEY()[i] = newVal.s

  graph.GetYaxis().SetTitle("Cross section in mb/sr")

  return graph

def SplitStates(Point5959,Point2590):
  BR_1m_GS = ufloat(66,4)/100
  BR_1m_2p = ufloat(34,4)/100
  BR_2p_GS = ufloat(9,5)/100
  BR_2p_2p = ufloat(91,5)/100
  N2Plus = (BR_1m_GS*Point2590 - BR_1m_2p*Point5959) / (-BR_2p_GS*BR_1m_2p + BR_2p_2p*BR_1m_GS)
  N1Minus = (BR_2p_GS*Point2590 - BR_2p_2p*Point5959) / (BR_2p_GS*BR_1m_2p - BR_2p_2p*BR_1m_GS)

  N2P = (-Point5959 + BR_1m_GS*(Point2590 + Point5959))/(BR_1m_GS - BR_2p_GS)
  # (-N5960 + BR1mGS*(N2590 + N5960))/(BR1mGS - BR2pGS)
  N1M = (Point5959 - BR_2p_GS*(Point2590 + Point5959))/(BR_1m_GS - BR_2p_GS)
  # (-N5960 + BR2pGS*(N2590 + N5960))/(BR1mGS - BR2pGS)
  # print "N2Plus: {}, N2P: {}".format(N2Plus,N2P)
  # print "N1Minus: {}, N1M: {}".format(N1Minus,N1M)

  return [N2Plus,N1Minus]

def FindCorrPoint(gr,xIn):
    for point in range(gr.GetN()):
        if int(xIn.n*1000) == int(gr.GetX()[point]*1000):
            return point
    return -1

def BuildPure(Graph5959, Graph2590):
  # print Graph5959.GetName()
  # Graph5959.Print()
  #
  # print Graph2590.GetName()
  # Graph2590.Print()

  oneMinusX = array('d')
  oneMinusXerr = array('d')
  oneMinusY = array('d')
  oneMinusYerr = array('d')

  twoPlusX = array('d')
  twoPlusXerr = array('d')
  twoPlusY = array('d')
  twoPlusYerr = array('d')

  Npoints =  Graph2590.GetN()
  if Npoints > Graph5959.GetN():
    Npoints = Graph5959.GetN()

  for point in range(Npoints):
    # print "point {}".format(point)
    X2590 = ufloat(Graph2590.GetX()[point],Graph2590.GetErrorX(point))
    # print "X2590: {}".format(X2590)

    corrPoint = FindCorrPoint(Graph5959,X2590)
    # print "CorrPoint {}".format(corrPoint)
    if corrPoint < 0:
        print "Continue on corrPoint: {}".format(corrPoint)
        continue

    X5959 = ufloat(Graph5959.GetX()[corrPoint],Graph5959.GetErrorX(corrPoint))

    if int(X5959.n) != int(X2590.n):
      print "Mismatch in X Values! 5959: {}, 2590: {}".format(X5959,X2590)
      continue
    else:
      oneMinusX.append(X5959.n)
      oneMinusXerr.append(X5959.s)
      twoPlusX.append(X2590.n)
      twoPlusXerr.append(X2590.s)

    Y5959 = ufloat(Graph5959.GetY()[corrPoint],Graph5959.GetEY()[corrPoint])
    Y2590 = ufloat(Graph2590.GetY()[point],Graph2590.GetEY()[point])
    SplitYs = SplitStates(Y5959,Y2590)

    # print "Y5959: {}, Y2590: {}".format(Y5959,Y2590)
    # print "N2Plus: {}, N1Minus: {}, Sum: {}\n".format(SplitYs[0],SplitYs[1],SplitYs[0]+SplitYs[1])


    twoPlusY.append(SplitYs[0].n)
    twoPlusYerr.append(SplitYs[0].s)
    oneMinusY.append(SplitYs[1].n)
    oneMinusYerr.append(SplitYs[1].s)

  twoPlusGraph = TGraphErrors(len(twoPlusX),twoPlusX,twoPlusY,twoPlusXerr,twoPlusYerr)
  twoPlusGraph.SetTitle("2^{+} 5958 Graph;COM Angle in Degrees;Cross section in mb/sr")
  twoPlusGraph.SetName("twoPlusGraph")

  oneMinusGraph = TGraphErrors(len(oneMinusX),oneMinusX,oneMinusY,oneMinusXerr,oneMinusYerr)
  oneMinusGraph.SetTitle("1^{-} 5959 Graph;COM Angle in Degrees;Cross section in mb/sr")
  oneMinusGraph.SetName("oneMinusGraph")

  # print twoPlusGraph.GetName()
  # twoPlusGraph.Print()
  #
  # print oneMinusGraph.GetName()
  # oneMinusGraph.Print()

  return [twoPlusGraph,oneMinusGraph]

frescoF = TFile.Open("transfer_before.root","read")
if not frescoF:
  print "No frescoF"
  quit()

dataF = TFile.Open("~/nuclear/mine/rb/angulardistribution/angOutReal.root","read")
if not dataF:
  print "No dataF"
  # quit()

gamF = TFile.Open("~/nuclear/mine/rb/angulardistribution/gammaOut.root","read")
if not gamF:
  print "No gamF"
  # quit()

outF = TFile.Open("pureStates.root","recreate")

frescoPlots = []
end = False
index = 0
while not end:
  tmpPlot = frescoF.Get("G{}".format(index))
  if not tmpPlot:
    end = True
    continue
  if tmpPlot.GetY()[1] <= 0:
    print "killed G{} due to zero".format(index)
    index += 1
    continue
  frescoPlots.append(tmpPlot)
  # tmpPlot.Print()
  index += 1

#G0 is 11Be+9Be
#G1 is 10Be&10Be GS GS - evaluates to 0
#G2 is GS and 1- 5959
#G3 is GS and 2- 6263
# print "Fresco Plots holds:"
# for ele in frescoPlots:
#   print ele.GetName()

dataPlots = []

# tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_g2589_corrected_clean_drop_gam") #corresponds to 5958 2+ state or 5959 1- state
# tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_opp_g2589_corrected_clean_drop_gam") #corresponds to 5958 2+ state or 5959 1- state
# if not tmpPlot:
#   print "No 2589"
# else:
#   tmpPlot=ScaleTGraph(tmpPlot)
#   dataPlots.append(tmpPlot)
#
# # tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_g2894_corrected_clean_drop_gam")#corresponds to 6263 2-
# tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_opp_g2894_corrected_clean_drop_gam")#corresponds to 6263 2-
# if not tmpPlot:
#   print "No 2894"
# else:
#   tmpPlot=ScaleTGraph(tmpPlot)
#   dataPlots.append(tmpPlot)
#   tmpPlot.Write("twoMinusGraph")
#
# # tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_g5958_corrected_clean_drop_gam") #corresponds to 5958 2+ or 5959 1- again
# tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_opp_g5958_corrected_clean_drop_gam") #corresponds to 5958 2+ or 5959 1- again
# if not tmpPlot:
#   print "No 5988"
# else:
#   tmpPlot=ScaleTGraph(tmpPlot)
#   dataPlots.append(tmpPlot)

tmpPlot = gamF.Get("AD_2590") #corresponds to 5958 2+ state or 5959 1- state
if not tmpPlot:
  print "No 2589"
else:
  tmpPlot=ScaleTGraph(tmpPlot)
  dataPlots.append(tmpPlot)

# tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_g2894_corrected_clean_drop_gam")#corresponds to 6263 2-
tmpPlot = gamF.Get("AD_2895")#corresponds to 6263 2-
if not tmpPlot:
  print "No 2894"
else:
  tmpPlot=ScaleTGraph(tmpPlot)
  dataPlots.append(tmpPlot)
  tmpPlot.Write("twoMinusGraph")

# tmpPlot = dataF.Get("AD_10Be_d0_s6_pid_g5958_corrected_clean_drop_gam") #corresponds to 5958 2+ or 5959 1- again
tmpPlot = gamF.Get("AD_5960_Addback") #corresponds to 5958 2+ or 5959 1- again
if not tmpPlot:
  print "No 5958"
else:
  tmpPlot=ScaleTGraph(tmpPlot)
  dataPlots.append(tmpPlot)

colors = [ROOT.kGreen, ROOT.kRed, ROOT.kBlue, ROOT.kOrange]

canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)
canvas.SetLogy()

Dummy = ROOT.TH2F("Dummy","Data compared to FRESCO outputs in dark",90,0,180,1000000,0,1000)
Dummy.GetXaxis().SetTitle("COM Angle in Degrees")
Dummy.GetYaxis().SetTitle("Cross Section in mb/sr")

Dummy.SetStats(ROOT.kFALSE)
Dummy.Draw()

Dummy.SetAxisRange(0,90,"X")
Dummy.SetAxisRange(.0001,10000,"Y")

Dummy.SetTitle("6263 2-")
Dummy.Draw()

leg = TLegend(0.5,.65,.9,.9)

fp = frescoPlots[2]
fp.SetLineColor(ROOT.TColor.GetColorDark(colors[0]))
fp.SetFillColor(ROOT.kWhite)
leg.AddEntry(fp,"Fresco Output for 6263 2- Spectroscopic Factor = 1")
fp.Draw("sameL")

dp = killXErr(dataPlots[1])
dp.SetMarkerColor(colors[0])
dp.SetLineColor(colors[0])
dp.SetFillColor(ROOT.kWhite)
dp.SetMarkerStyle(20)
leg.AddEntry(dp,"2894 Data")
dp.Draw("sameP")
leg.Draw()

canvas.SaveAs("plot_transfer_6263_2minus.png")

Dummy.SetTitle("5958 2+ / 5959 1- doublet")
Dummy.SetAxisRange(20,80,"X")
Dummy.SetAxisRange(.00001,100,"Y")

Dummy.Draw()

leg = TLegend(0.5,.65,.9,.9)

# fp = frescoPlots[1]
# fp.SetLineColor(colors[1])
# fp.SetFillColor(ROOT.kWhite)
# leg.AddEntry(fp,"Fresco Output for 5959 1- Spectroscopic Factor = 1")
# fp.Draw("sameL")
#
# fp = frescoPlots[3]
# fp.SetLineColor(colors[0])
# fp.SetFillColor(ROOT.kWhite)
# leg.AddEntry(fp,"Fresco Output for 5958 2+ Spectroscopic Factor = 1")
# fp.Draw("sameL")

dp2 = killXErr(dataPlots[2])
dp2.SetMarkerColor(colors[3])
dp2.SetLineColor(colors[3])
dp2.SetFillColor(ROOT.kWhite)
dp2.SetMarkerStyle(20)
leg.AddEntry(dp2,"5958 5959 Doublet Data")
dp2.Draw("sameP")

dp3 = killXErr(dataPlots[0])
dp3.SetMarkerColor(colors[2])
dp3.SetLineColor(colors[2])
dp3.SetFillColor(ROOT.kWhite)
dp3.SetMarkerStyle(20)
leg.AddEntry(dp3,"2589 Data")
dp3.Draw("sameP")
leg.Draw()

canvas.SaveAs("plot_transfer_5958_2plus_and_5959_1minus.png")

purePlots = BuildPure(dataPlots[2], dataPlots[0])
purePlots[0].Write()
purePlots[1].Write()

dp4 = killXErr(purePlots[1])
dp4.SetMarkerColor(ROOT.TColor.GetColorDark(colors[1]))
dp4.SetLineColor(ROOT.TColor.GetColorDark(colors[1]))
dp4.SetFillColor(ROOT.kWhite)
dp4.SetMarkerStyle(20)
leg.AddEntry(dp4,"Calculated 1- from Doublet Data")
dp4.Draw("sameP")

dp5 = killXErr(purePlots[0])
dp5.SetMarkerColor(ROOT.TColor.GetColorDark(colors[0]))
dp5.SetLineColor(ROOT.TColor.GetColorDark(colors[0]))
dp5.SetFillColor(ROOT.kWhite)
dp5.SetMarkerStyle(20)
leg.AddEntry(dp5,"Calculated 2+ from Doublet Data")
dp5.Draw("sameP")
leg.Draw()

canvas.SaveAs("plot_calclated_1m.png")


Dummy.SetTitle("Pure States")
Dummy.Draw()

leg = TLegend(0.5,.65,.9,.9)

# fp = frescoPlots[1]
# fp.SetLineColor(colors[1])
# fp.SetFillColor(ROOT.kWhite)
# leg.AddEntry(fp,"Fresco Output for 5959 1- Spectroscopic Factor = 1")
# fp.Draw("sameL")
#
# fp = frescoPlots[3]
# fp.SetLineColor(colors[0])
# fp.SetFillColor(ROOT.kWhite)
# leg.AddEntry(fp,"Fresco Output for 5958 2+ Spectroscopic Factor = 1")
# fp.Draw("sameL")

purePlots = BuildPure(dataPlots[2], dataPlots[0])

# dp = purePlots[1]
# dp.SetMarkerColor(ROOT.TColor.GetColorDark(colors[1]))
# dp.SetLineColor(ROOT.TColor.GetColorDark(colors[1]))
# dp.SetFillColor(ROOT.kWhite)
# dp.SetMarkerStyle(20)
leg.AddEntry(dp4,"Calculated 1- from Doublet Data")
dp4.Draw("sameP")

# dp = purePlots[0]
# dp.SetMarkerColor(ROOT.TColor.GetColorDark(colors[0]))
# dp.SetLineColor(ROOT.TColor.GetColorDark(colors[0]))
# dp.SetFillColor(ROOT.kWhite)
# dp.SetMarkerStyle(20)
leg.AddEntry(dp5,"Calculated 2+ from Doublet Data")
dp5.Draw("sameP")
leg.Draw()

canvas.SaveAs("plot_calclated_pure.png")
#
# Dummy.SetTitle("Checking to see if sums are the same")
# # Dummy.SetAxisRange(20,60,"X")
# # Dummy.SetAxisRange(.0001,100,"Y")
# Dummy.Draw()
#
# leg = TLegend(0.65,.65,.9,.9)
#
#
# sumData = SumGraphs(dataPlots[0],dataPlots[2],"sumData","Sum of 2590 and 5960 Angular Distributions")
# # print sumData.GetTitle()
# # sumData.Print()
# sumData.SetMarkerColor(colors[0])
# sumData.SetLineColor(colors[0])
# sumData.SetFillColor(ROOT.kWhite)
# sumData.SetMarkerStyle(20)
# leg.AddEntry(sumData,sumData.GetTitle())
# sumData.Draw("sameP")
#
# sumPure = SumGraphs(purePlots[0],purePlots[1],"sumPure","Sum of 1- and 2+ Angular Distributions")
# # print sumPure.GetTitle()
# # sumPure.Print()
# sumPure.SetMarkerColor(colors[1])
# sumPure.SetLineColor(colors[1])
# sumPure.SetFillColor(ROOT.kWhite)
# sumPure.SetMarkerStyle(20)
# leg.AddEntry(sumPure,sumPure.GetTitle())
# sumPure.Draw("sameP")
#
# leg.Draw()
# canvas.SaveAs("sums.png")
