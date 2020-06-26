from ROOT import TFile, TGraph, TGraphErrors, TF1, TCanvas, TMultiGraph, TColor
from array import array
import ROOT

def CalcNormByFirstPoint(fg, dg):
  datY = dg.GetY()[0]
  datX = dg.GetX()[0]

  fresY = fg.Eval(datX)

  return fresY/datY

def CalcNormByFit(fg, dg):
  minX = dg.GetX()[0]
  maxX = dg.GetX()[dg.GetN()-1]

  #func = TF1("func","[0]*exp([1]*x)",minX,maxX)
  #func.SetParName(0,"Scale")
  #func.SetParName(1,"Expo")
  ##func.SetParName(2,"Offset")

  #func.SetParameter(0,20)
  #func.SetParameter(1,-.15)
  ##func.SetParameter(2,0)

  #func = TF1("expo")

  #results = dg.Fit(func,"SEMR")
  dgresults = dg.Fit("expo","S")
  #dgresults.Print()
  dg.Write()

  fgresults = fg.Fit("expo","S","",minX,maxX)
  #fgresults.Print()
  #fg.Write()

  norm = fgresults.GetParams()[1]/dgresults.GetParams()[1]
  return norm

def CalcNorm(fg, dg):
  normSum = 0
  normNum = 0

  dg.Print()

  #for pointN in range(dg.GetN()):
  for pointN in range(2,6):
    dataX = dg.GetX()[pointN]
    dataY = dg.GetY()[pointN]

    print "Got point {}, x: {}, y: {}".format(pointN,dataX,dataY)

    fresY = fg.Eval(dataX)

    #print "dataX: {}".format(dataX)
    #print "dataY: {}".format(dataY)
    #print "fresY: {}".format(fresY)
    #print "ratio: {:.2e}\n".format(fresY/dataY)

    normSum += fresY/dataY
    normNum += 1

  norm = normSum/normNum

  #print '{:.2e}'.format(float(norm))

  return norm

def CalcNormSeek(fg, dg):
  dX = []
  dY = []
  fY = []
  for pointN in range(dg.GetN()-1):
    dX.append(dg.GetX()[pointN])
    dY.append(dg.GetY()[pointN])
    fY.append(fg.Eval(dg.GetX()[pointN]))
  combo = zip(dX,dY,fY)

  averageD = 0
  aDI = 0
  averageF = 0
  aFI = 0
  for point in combo:
    averageD += point[1]
    aDI +=1

    averageF += point[2]
    aFI +=1

  averageD = averageD/aDI
  averageF = averageF/aFI

  norm = averageF/averageD

  return norm

def Scale(graph,scale):
  if not graph:
    return

  ArrX = array('d')
  ArrY = array('d')
  ArrXErr = array('d')
  ArrYErr = array('d')

  for i in range(graph.GetN()):
    x = ROOT.Double(0)
    y = ROOT.Double(0)
    graph.GetPoint(i,x,y)
    ex = graph.GetErrorX(i)
    ey = graph.GetErrorY(i)

    ArrX.append(x)
    ArrY.append(y*scale)
    ArrXErr.append(ex)
    ArrYErr.append(ey*scale)

  retTG = TGraphErrors(len(ArrX),ArrX,ArrY,ArrXErr,ArrYErr)
  retTG.SetName(graph.GetName())
  retTG.SetTitle(graph.GetTitle())
  return retTG

def combinedDraw(frescoGraph,goodPID,badPID,goodCORR,badCORR):
  #print "combinedDraw start"
  canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)

  MG = TMultiGraph()
  legend = ROOT.TLegend(0.55,.55,.9,.9)
  ##legend.SetBorderSize(0)
  #underHisto.SetLineColor(ROOT.kBlack)
  #underHisto.SetMinimum(0)
  ##underHisto.SetMaximum(underHisto.GetMaximum() * 1.5)
  #underHisto.GetXaxis().SetRangeUser(0,180)
  #underHisto.SetTitle(title)
  #underHisto.SetLineColor(ROOT.kBlack)
  #underHisto.SetTitle(title)
  #underHisto.GetYaxis().SetTitle("Counts in Arb. Units")
  #legend.AddEntry(underHisto,"Simulated Angular Distribution")
  #underHisto.SetStats(ROOT.kFALSE)
  #underHisto.Draw()

  if frescoGraph:
    #print "frescoGraph"
    frescoGraph.SetMarkerColor(ROOT.kBlack)
    frescoGraph.SetLineColor(ROOT.kBlack)
    frescoGraph.SetFillColor(ROOT.kBlack)
    #frescoGraph.SetMarkerStyle(33)
    MG.Add(frescoGraph,"L")
    legend.AddEntry(frescoGraph,"Fresco Output")
  else:
    print "No FrescoGraph!!!"
    return

  if goodPID:
    #print "goodPID"
    goodPID.SetMarkerColor(ROOT.kGreen)
    goodPID.SetLineColor(ROOT.kGreen)
    goodPID.SetFillColor(ROOT.kGreen)
    #goodPID.SetMarkerStyle(33)
    MG.Add(goodPID,"P")
    legend.AddEntry(goodPID,"ScaledPID")
  else:
    print "No goodPID in Draw()"

  if goodCORR:
    #print "goodCORR"
    goodCORR.SetMarkerColor(TColor.GetColorDark(ROOT.kGreen))
    goodCORR.SetLineColor(TColor.GetColorDark(ROOT.kGreen))
    goodCORR.SetFillColor(TColor.GetColorDark(ROOT.kGreen))
    goodCORR.SetMarkerStyle(21)
    #afterHisto.Draw("PLsame")
    MG.Add(goodCORR,"P")
    legend.AddEntry(goodCORR,"Good Dual Det")
  else:
    print "No goodCORR in Draw()"

  if badPID:
    #print "badPID"
    badPID.SetMarkerColor(ROOT.kRed)
    badPID.SetLineColor(ROOT.kRed)
    badPID.SetFillColor(ROOT.kRed)
    badPID.SetMarkerStyle(33)
    MG.Add(badPID,"P")
    legend.AddEntry(badPID,"Discard PID")
  else:
    print "No badPID in Draw()"

  if badCORR:
    #print "badCORR"
    badCORR.SetMarkerColor(TColor.GetColorDark(ROOT.kRed))
    badCORR.SetLineColor(TColor.GetColorDark(ROOT.kRed))
    badCORR.SetFillColor(TColor.GetColorDark(ROOT.kRed))
    badCORR.SetMarkerStyle(21)
    MG.Add(badCORR,"P")
    legend.AddEntry(badCORR,"Discard Dual Det")
  else:
    print "No badCORR in Draw()"


  MG.SetTitle("Scaled Elastic Distribution for detector {};Center of Mass Angle in Degrees;Cross section in mb/sr".format(det))
  MG.SetName("MG_d{}".format(det))
  MG.Draw("AP")
  legend.Draw()
  MG.Write()
  MG.SetMaximum(500)
  MG.SetMinimum(0)

  canvas.SetLogy()
  #MG.GetYaxis().SetRangeUser(0,500)

  MG.Draw()
  canvas.SaveAs(MG.GetName()+'.png')
  #print "End Draw"


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("frescopath", help='Fresco Input Location & Name')
parser.add_argument("datapath", help='Data Input Location & Name')
parser.add_argument("outpath", help='Diagnostic Output')
args = parser.parse_args()
#print "Arguments Parsed"

frescoFile = TFile.Open(args.frescopath,'read')
dataFile = TFile.Open(args.datapath,'read')
outFile = TFile.Open(args.outpath,"recreate")


dets = [1,2]
types = ["pid","corr"]

frescoGraph = frescoFile.Get("G1")
frescoGraph.Write("FrescoGraph")

dataGraph = dataFile.Get("AD_d0_s0_pid_11Be_sub")
if not dataGraph:
  print "Didn't find sum graph"
  quit()

norm = CalcNormByFirstPoint(fg = frescoGraph, dg = dataGraph)

print "Summed norm: {}".format(norm)
ScaledGraph = Scale(dataGraph, norm)
ScaledGraph.SetName(dataGraph.GetName()+"_scaled")
ScaledGraph.SetTitle(dataGraph.GetTitle()+" in abs units")
ScaledGraph.GetYaxis().SetTitle("Cross Section in mb/sr")
ScaledGraph.Write()

#for det in dets:
  #for dettype in types:
    #dataGraph = dataFile.Get("AD_d{}_s0_{}_11Be_corrected_clean_drop".format(det,dettype))
    #if not dataGraph:
      #continue
    ##dataGraph.Write()

    #norm = CalcNormByFirstPoint(fg = frescoGraph, dg = dataGraph)

    ##print norm

    #ScaledGraph = Scale(dataGraph, norm)
    #ScaledGraph.SetName(dataGraph.GetName()+"_scaled")
    #ScaledGraph.SetTitle(dataGraph.GetTitle()+" in abs units")
    #ScaledGraph.GetYaxis().SetTitle("Cross Section in mb/sr")
    #ScaledGraph.Write()


    #discardGraph = dataFile.Get("AD_d{}_s0_{}_11Be_corrected_discard".format(det,dettype))
    #ScaledDiscard = Scale(discardGraph,norm)
    #if ScaledDiscard:
      #ScaledDiscard.SetName(discardGraph.GetName()+"_scaled")
      #ScaledDiscard.SetTitle(discardGraph.GetTitle()+" in abs units")
      #ScaledDiscard.GetYaxis().SetTitle("Cross Section in mb/sr")
      #ScaledDiscard.Write()

  ##goodPID = outFile.Get("AD_d{}_s0_{}_11Be_corrected_clean_drop_scaled".format(det,"pid"))
  ##badPID = outFile.Get("AD_d{}_s0_{}_11Be_corrected_discard_scaled".format(det,"pid"))
  ##goodCORR = outFile.Get("AD_d{}_s0_{}_11Be_corrected_clean_drop_scaled".format(det,"corr"))
  ##badCORR = outFile.Get("AD_d{}_s0_{}_11Be_corrected_discard_scaled".format(det,"corr"))
  ##combinedDraw(frescoGraph,goodPID,badPID,goodCORR,badCORR)
