from ROOT import TGraphErrors, TFile
from array import array
import ROOT

def WriteGraph(graph):
  for i in range(graph.GetN()):
    outfile.write(" {}  {}  {}\n".format(graph.GetX()[i],graph.GetY()[i],graph.GetEY()[i]))

# def WriteExternalFile(gr):
#   exName = "undefined"
#   if "sub" in gr.GetName():
#     exName = "Elastic"
#   elif "gam" in gr.GetName():
#     exName = "Inelastic"
#
#   scale = 7.97863393126e-05
#
#   TextFile = open(exName+".txt","w")
#   CSVFile = open(exName+".csv","w")
#   CSVFile.write("CM angle,Cross-section,ErrorX,ErrorY\n")
#   for i in range(graph.GetN()):
#     TextFile.write(" {}  {}  {}\n".format(gr.GetX()[i],gr.GetY()[i]*scale,gr.GetEY()[i]*scale))
#     CSVFile.write("{},{},{},{}\n".format (gr.GetX()[i],gr.GetY()[i]*scale,gr.GetEX()[i],gr.GetEY()[i]*scale))
#
#   CSVFile.write("SFRESCO is run with ")
#   CSVFile.write("idir=0 lab=F abserr=T\n\n")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("inpath", help='Input Location & Name', default="~/nuclear/mine/rb/angulardistribution/angOutReal.root", nargs="?")
parser.add_argument("outpath", help='Output Location & Name', default="elastic.search", nargs="?")
parser.add_argument("rRuth", help='Ratio to Rutherford', default="False", nargs="?")

args = parser.parse_args()
#print "Arguments Parsed"

if args.rRuth == "True" or args.rRuth == "TRUE":
    args.rRuth = True
else:
    args.rRuth = False

infile = TFile.Open(args.inpath,'read')
outfile = open(args.outpath,"w")

if not infile:
  print "Failed to open infile: {}".format(args.inpath)
  quit()

if not outfile:
  print "Failed to open outfile: {}".format(args.outpath)

#graph = Normalize(graph)

outfile.write("'elastic.in'")#first line is the original fresco input file
outfile.write(" 'elastic.frout'\n")# still first line, we need the output file

outfile.write('11 ')#print number of variables
outfile.write('1\n')#number of experimental data sets.  ...

#There are 3 &pot namelist lines in IN for the nuclear parts of potential kp=1, so the variables of the interaction potentials (kind=1) in the search are identified by the specification of kp and pline in the &variable namelist in FROUT, along with col for the index to the p array. The potential value gives the initial value for the search, and step the initial magnitude for trial changes.

outfile.write(" &variable kind=5 name='norm' dataset=1 datanorm= 8.02241928938e-05/\n")

###Coulomb Potential
outfile.write(" &variable kind=1 name='r0C' kp=1 pline=1 col=3 potential=1.2 valmin=.4 valmax=1.4 step=.01/\n")
##Real Woods-Saxon
outfile.write(" &variable kind=1 name='V' kp=1 pline=2 col=1 potential=60  step=.1/\n")
outfile.write(" &variable kind=1 name='r0' kp=1 pline=2 col=2 potential=1.18 step=.01/\n")
outfile.write(" &variable kind=1 name='a' kp=1 pline=2 col=3 potential=.6 step=.01/\n")
###Imaginary Woods-Saxon
outfile.write(" &variable kind=1 name='W' kp=1 pline=2 col=4 potential=32.6 step=.1/\n")
outfile.write(" &variable kind=1 name='rW' kp=1 pline=2 col=5 potential=1.18 step=.01/\n")
outfile.write(" &variable kind=1 name='aW' kp=1 pline=2 col=6 potential=.6 step=.01/\n")
###Spin orbit
outfile.write(" &variable kind=1 name='Vso' kp=1 pline=3 col=1 potential=5.7  step=.02/\n")
outfile.write(" &variable kind=1 name='rso' kp=1 pline=3 col=2 potential=1.15 step=.01/\n")
outfile.write(" &variable kind=1 name='aso' kp=1 pline=3 col=3 potential=.7  step=.01/\n")
####


if args.rRuth:
    outfile.write(" &data idir=2 lab=F abserr=T iscale=-1 ic=1 ia=1/\n")
else:
    outfile.write(" &data idir=0 lab=F abserr=T iscale=-1 ic=1 ia=1/\n")
#outfile.write(" &data type=0 data_file='Elastic0.txt' iscale=2  idir=0 lab=F abserr=T ic=1 ia=1/\n")

#iscale is -1 for dimensionless data, and 0 absolute data in units of fm2/sr, 1 for b/sr, 2 for mb/sr (the default) and 3 for $\mu$b/sr.
#idir is -1 for cross-section data given as astrophysical S-factors, 0 for data given in absolute units (the default), and 1 as ratio to Rutherford.
#lab is default false
#abserr is default FALSE
graph = infile.Get("AD_d0_s0_pid_11Be_sub")
if not graph:
  print "Error! No elastic angular distribution found!"
if graph:
  WriteGraph(graph)
  # WriteExternalFile(graph)
#graph = infile.Get("AD_d1_s0_corr_11Be_corrected_clean_drop")
#if graph:
  #WriteAbsGraph(graph)

#outfile.write(" &data type=0 data_file='Elastic1.txt' iscale=2  idir=0 lab=F abserr=T ic=1 ia=2/\n")
# outfile.write(" &data idir=0 lab=F abserr=T ic=1 ia=2/\n")
# graph = infile.Get("AD_sum_s0_pid_11Be_gtag_320_corrected_clean_drop_gam")
# if graph:
#   WriteAbsGraph(graph)
#   WriteExternalFile(graph)

outfile.write("&\n")


