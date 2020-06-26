from ROOT import TFile, TGraph, TGraphErrors, TMultiGraph, TCanvas, TColor, TLegend
import ROOT
import argparse
import random

def MakeCombined(myfile, color, fitInfo):
  info = myfile.split("_")
  curFile = TFile.Open(myfile,"read")
  if not myfile:
    print "No File found in MakeCombined"
    return
  # else:
  #   curFile.Print()

  elasticHdata = curFile.Get("G0")
  elasticH = curFile.Get("G1")
  inelasticHdata = curFile.Get("G2")
  inelasticH = curFile.Get("G3")

  canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)
  canvas.SetLogy()
  legend = TLegend(.75,.75,.9,.9)
  # title = "SFRESCO fit for initial parameters rC: {}, V_vol: {}, r_vol: {}, d_vol: {}, W_surf: {}, rW_surf: {}, aW_surf: {}".format(info[2],info[3],info[4],info[5],info[6],info[7],info[8][0:2])
  title = "Final parameters rC: {}, V_vol: {}, r_vol: {}, d_vol: {}, W_surf: {}, rW_surf: {}, aW_surf: {}".format(fitInfo[1],fitInfo[2],fitInfo[3],fitInfo[4],fitInfo[5],fitInfo[6],fitInfo[7])
  Dummy = ROOT.TH2F("Dummy","tmptitle",90,10,90,1000000,0,10000)
  Dummy.SetTitle(title)
  Dummy.GetXaxis().SetTitle("COM Angle in Degrees")
  Dummy.GetYaxis().SetTitle("Cross Section in mb/sr")

  Dummy.SetStats(ROOT.kFALSE)
  Dummy.Draw()

  Dummy.SetAxisRange(10,80,"X")

  Dummy.SetAxisRange(.0001,1000,"Y")
  graphOptions="sameP"

  # elasticColor = ROOT.kRed

  if elasticHdata:
    # elasticHdata.SetMarkerColor(color)
    # elasticHdata.SetLineColor(color)
    # elasticHdata.SetFillColor(color)
    elasticHdata.SetMarkerStyle(20)
    elasticHdata.Draw(graphOptions)
    legend.AddEntry(elasticHdata,"Elastic")
  else:
    print "No elasticH in Draw()"

  if elasticH:
    elasticH.SetMarkerColor(color)
    elasticH.SetLineColor(color)
    elasticH.SetFillColor(color)
    # elasticH.SetMarkerStyle(20)
    elasticH.SetLineWidth(5)
    elasticH.Draw("sameL")

  # inelasticColor = ROOT.kBlue
  #
  # if inelasticHdata:
  #   inelasticHdata.SetMarkerColor(inelasticColor)
  #   inelasticHdata.SetLineColor(inelasticColor)
  #   inelasticHdata.SetFillColor(inelasticColor)
  #   inelasticHdata.SetMarkerStyle(20)
  #   legend.AddEntry(inelasticHdata,"Inelastic")
  #   inelasticHdata.Draw(graphOptions)
  #
  # if inelasticH:
  #   inelasticH.SetMarkerColor(inelasticColor)
  #   inelasticH.SetLineColor(inelasticColor)
  #   inelasticH.SetFillColor(inelasticColor)
  #   #inelasticH.SetMarkerStyle(20)
  #   inelasticH.Draw("sameL")

  legend.Draw()
  saveName = "outputs/special_{}_{}_{}_{}_{}_{}_{}.png".format(info[2],info[3],info[4],info[5],info[6],info[7],info[8][0:2])
  canvas.SaveAs(saveName)


parser = argparse.ArgumentParser()

parser.add_argument("FILE", help="Files to pull from", nargs="+")

args = parser.parse_args()

MGElastic = TMultiGraph()
MGElastic.SetTitle("sFresco elastic results comparing different initial settings;Center of Mass Angle in Degrees;Cross Section in mb/sr")
legendElastic = ROOT.TLegend(0.55,.55,.9,.9)

MGInElastic = TMultiGraph()
MGInElastic.SetTitle("sFresco inelastic results comparing different initial settings;Center of Mass Angle in Degrees;Cross Section in mb/sr")
legendInElastic = ROOT.TLegend(0.55,.55,.9,.9)


# specialPlots = ["afters/elastic_after_1.1_100_1.1_.8_8_1.4_.8.root",
#                 "afters/elastic_after_1.1_15_1.3_.8_6_1.4_.8.root",
#                 "afters/elastic_after_1.1_25_1.1_.8_6_1.4_.8.root"]

specialPlots = ["afters/elastic_after_1.1_50_1.15_.4_8_1.2_.4.root",
                "afters/elastic_after_1.1_50_1.3_.8_4_1.4_.8.root",
                "afters/elastic_after_.9_50_1.15_.8_8_1.4_.8.root",
                "afters/elastic_after_1.1_15_1._.4_4_1.2_.4.root"]

convergedInfo=[]
convergedInfo.append([1.81E-04,1.3995,75.287,1.3161,0.4548,18.57,1.7541,0.92578,6.47,1.15,0.633])
convergedInfo.append([9.02E-05,0.77693,36.094,1.5103,0.70546,7.0245,1.6665,0.96545,6.47,1.15,0.633])
convergedInfo.append([7.45E-05,1.1555,45.559,1.191,0.56288,6.485,1.046,1.1883,6.47,1.15,0.633])
convergedInfo.append([6.45E-05,1.3997,11.14,0.96429,1.1884,13.793,1.026,0.95821,6.47,1.15,0.633])


colors = [TColor.GetColorDark(ROOT.kGreen),ROOT.kBlue,ROOT.kRed,ROOT.kOrange]

tmpzip = zip(specialPlots,colors,convergedInfo)

for fileName, color, info in tmpzip:
  MakeCombined(fileName,color,info)

# for plot in specialPlots: #this bit puts the speical ones at the end so they are drawn on top
#   args.FILE.remove(plot)

# args.FILE += specialPlots

args.FILE = specialPlots


for curFileString in args.FILE:
  info = curFileString.split("_")
  curFile = TFile.Open(curFileString,"read")

  #randVal = random.randint(0, 15)

  #if curFileString != specialPlots[0] and curFileString != specialPlots[1] and curFileString != specialPlots[2]:
    #if randVal != 0:
      #continue

  if not curFile:
    continue

  curGraph = curFile.Get("G1")
  curGraph.SetName("rC: {}, Vr: {}, rr: {}, ar: {}, Vi: {}, ri: {}, ai: {}".format(info[2],info[3],info[4],info[5],info[6],info[7],info[8][0:2]))
  LineColor = ROOT.kBlack
  if curFileString == specialPlots[0]:
    LineColor = colors[0]
  elif curFileString == specialPlots[1]:
    LineColor = colors[1]
  elif curFileString == specialPlots[2]:
    LineColor = colors[2]
  elif curFileString == specialPlots[3]:
    LineColor = colors[3]
  if curGraph:
    curGraph.SetMarkerColor(ROOT.kWhite)
    if LineColor != ROOT.kBlack:
      curGraph.SetLineColor(LineColor)
      curGraph.SetLineWidth(5)
      legendElastic.AddEntry(curGraph,curGraph.GetName())

    curGraph.SetFillColor(ROOT.kWhite)
    MGElastic.Add(curGraph,"L")

  curGraph = curFile.Get("G3")
  # curGraph.SetName("rC: {}, Vr: {}, rr: {}, ar: {}, Vi: {}, ri: {}, ai: {}".format(info[2],info[3],info[4],info[5],info[6],info[7],info[8][0:2]))

  if curGraph:
    curGraph.SetMarkerColor(ROOT.kWhite)
    if LineColor != ROOT.kBlack:
      curGraph.SetLineColor(LineColor)
      curGraph.SetLineWidth(5)
      legendInElastic.AddEntry(curGraph,curGraph.GetName())

    curGraph.SetFillColor(ROOT.kWhite)
    MGInElastic.Add(curGraph,"L")

# DataGraph = curFile.Get("G0")
# if DataGraph:
#   DataGraph.SetMarkerColor(TColor.GetColorDark(ROOT.kRed))
#   DataGraph.SetLineColor(TColor.GetColorDark(ROOT.kRed))
#   DataGraph.SetFillColor(ROOT.kWhite)
#   DataGraph.SetMarkerStyle(ROOT.kFullSquare)
#   MGElastic.Add(DataGraph,"P")
#   legendElastic.AddEntry(DataGraph,"Data")
#
# DataGraph = curFile.Get("G2")
# if DataGraph:
#   DataGraph.SetMarkerColor(TColor.GetColorDark(ROOT.kRed))
#   DataGraph.SetLineColor(TColor.GetColorDark(ROOT.kRed))
#   DataGraph.SetFillColor(ROOT.kWhite)
#   DataGraph.SetMarkerStyle(ROOT.kFullSquare)
#   MGInElastic.Add(DataGraph,"P")
#   legendInElastic.AddEntry(DataGraph,"Data")

canvas = TCanvas('canvas','shouldnotseethis',0,0,1280,720)

MGElastic.Draw("al*")
canvas.SetLogy()
MGElastic.Draw()
#if MGElastic.GetListOfGraphs().GetEntries() < 10:
legendElastic.Draw()
canvas.SaveAs("aa_ElasticBatch.png")

MGInElastic.Draw("al*")
#canvas.SetLogy()
MGInElastic.Draw()
#if MGInElastic.GetListOfGraphs().GetEntries() < 10:
legendInElastic.Draw()
canvas.SaveAs("aa_InElasticBatch.png")

outFile = TFile("Batch.root","recreate")
MGElastic.Write()
MGInElastic.Write()

couOnlyFile = TFile("../coulombOnly.root","read")
if couOnlyFile:
  couOnlyGraph = couOnlyFile.Get("G1")
  if couOnlyGraph:
    couOnlyGraph.SetMarkerColor(ROOT.kWhite)
    couOnlyGraph.SetLineColor(ROOT.kMagenta)
    couOnlyGraph.SetFillColor(ROOT.kWhite)
    couOnlyGraph.SetLineWidth(5)
    couOnlyGraph.SetLineStyle(5)
    MGElastic.Add(couOnlyGraph,"L")
    legendElastic.AddEntry(couOnlyGraph,"Coulomb Only")

MGElastic.Draw("al*")
canvas.SetLogy()
MGElastic.Draw()
#if MGElastic.GetListOfGraphs().GetEntries() < 10:
legendElastic.Draw()
canvas.SaveAs("aa_ElasticBatch_cou.png")
outFile.cd()
MGElastic.Write()
