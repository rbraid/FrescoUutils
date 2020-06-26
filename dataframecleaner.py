import pandas as pd

def num_after_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return len(s) - s.index('.') - 1

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("csvPath", help = "Path to input CSV file", default = "output.csv", nargs='?')
parser.add_argument("csvPathOut", help = "Path to output CSV file", default = "output_clean.csv", nargs='?')
args = parser.parse_args()

df = pd.read_csv(args.csvPath)
df.dropna()

print "test 1.1: {}".format(num_after_point(1.1))

print "test 1.1345: {}".format(num_after_point(1.1345))

df.drop(df[num_after_point(df.r0_fit) > 1].index, inplace=True)

df.to_csv(args.csvPathOut)