# importing csv module
print "Starting"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.size'] = 18

import seaborn as sns
sns.set_context('talk', font_scale=1.2);

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("csvPath", help = "Path to CSV file", default = "output.csv", nargs='?')
args = parser.parse_args()

print "Reading"
df = pd.read_csv(args.csvPath)
print "Done Reading"

#print("Found negative at: ".format(df[((df.V_fit > 0))].index))
fitList = ['r0C_fit', 'V_vol_fit', 'r0_vol_fit', 'd_vol_fit', 'W_surf_fit', 'rW_surf_fit', 'aW_surf_fit', 'Total_ChiSquare']
for myvar in fitList:
  print "Dropping negative {}".format(myvar)
  df.drop(df[df[myvar] <= 0].index, inplace=True)

# df.drop(df[df.V_vol_fit <= 0].index, inplace=True)
# df.drop(df[df.r0_vol_fit <= 0].index, inplace=True)
df.drop(df[df.V_vol_fit > 200].index, inplace=True)
df.drop(df[df.W_surf_fit > 90].index, inplace=True)
df.dropna()
#df.drop(df[df.VI_fit > 40].index, inplace=True)
#df.drop(df[df.d_fit < .4].index, inplace=True)

#df.drop(df[df.Total_ChiSquare > 50].index, inplace=True)

#df[df.V_fit > 0]

#df_subset = df[['V_fit', 'r0_fit', 'd_fit', 'VI_fit', 'r0I_fit', 'dI_fit', 'Total_ChiSquare']]
#df.columns = ['country', 'continent', 'year', 'life_exp', 'pop', 'gdp_per_cap']
#df.head()

#print(df)
# norm_init,r0C,V_vol,r0_vol,d_vol,W_surf,rW_surf,aW_surf,V_so,r0_so,d_so,norm,r0C_fit,V_vol_fit,r0_vol_fit,d_vol_fit,W_surf_fit,rW_surf_fit,aW_surf_fit,V_so_fit,r0_so_fit,d_so_fit,Total_ChiSquare

print "Done cleaning data"

sns_plot = sns.pairplot(df,vars=['r0C_fit', 'V_vol_fit', 'r0_vol_fit', 'd_vol_fit', 'W_surf_fit', 'rW_surf_fit', 'aW_surf_fit', 'Total_ChiSquare']);
sns_plot.savefig("aa_FitVals.png")

sns_plot = sns.pairplot(df,vars=['V_vol', 'V_vol_fit', 'W_surf', 'W_surf_fit', 'Total_ChiSquare']);
sns_plot.savefig("aa_VVals.png")

sns_plot = sns.pairplot(df,vars=['r0_vol', 'r0_vol_fit', 'rW_surf', 'rW_surf_fit', 'Total_ChiSquare']);
sns_plot.savefig("aa_RVals.png")

sns_plot = sns.pairplot(df,vars=['d_vol', 'd_vol_fit', 'aW_surf', 'aW_surf_fit', 'Total_ChiSquare']);
sns_plot.savefig("aa_DVals.png")

sns_plot = sns.pairplot(df,vars=['V_vol_fit', 'd_vol_fit', 'W_surf_fit', 'aW_surf_fit', 'Total_ChiSquare']);
sns_plot.savefig("aa_ActualFits.png")

good_df = df.drop(df[df.Total_ChiSquare > 50].index)
bad_df = df.drop(df[df.Total_ChiSquare <= 50].index)

sns.set_context("talk")

sns_plot = sns.pairplot(good_df,vars=['r0C_fit','V_vol_fit', 'r0_vol_fit', 'd_vol_fit', 'W_surf_fit', 'rW_surf_fit', 'aW_surf_fit', 'Total_ChiSquare']);
sns_plot.map_lower(sns.kdeplot)
# for ax in sns_plot.axes.flatten():
    ##ax.ticklabel_format(style='sci', scilimits=(0,0), axis='both')
  # ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
  #ax.autofmt_xdate()

sns_plot.savefig("aa_FitVals_good.png")
sns_plot = sns.pairplot(bad_df,vars=['V_vol_fit', 'r0_vol_fit', 'd_vol_fit', 'W_surf_fit', 'rW_surf_fit', 'aW_surf_fit', 'Total_ChiSquare']);
sns_plot.savefig("aa_FitVals_bad.png")

#g = sns.PairGrid(good_df)
#g.map_upper(plt.scatter)
#g.map_lower(sns.kdeplot)
#g.map_diag(sns.kdeplot, lw=3, legend=False);
#g.savefig("aa_test.png")