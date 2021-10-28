#!/usr/bin/env python3
import argparse
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--input-file", help="zwavejs2mqtt nodes dump json file for input",
                    required=True)
parser.add_argument("-o", "--output-file", help="the name of the png file to output (default: %(default)s)",
                    default="neighbor_graph.png")
parser.add_argument("-c", "--color-map", help="The matplotlib colormap to use (default: %(default)s)",
                    default="RdBu")
args = parser.parse_args()

with open(args.input_file, "r") as nodes_file:
    nodes = json.load(nodes_file)

nodelist = [ node['id'] for node in nodes ]

matrix = dict()

for node in nodes:
  matrix[node['id']] = dict()
  for n in nodelist:
    if n == node['id']:
      matrix[node['id']][n] = 0
    elif n in node['neighbors']:
      matrix[node['id']][n] = 1
    else:
      matrix[node['id']][n] = -1

df = pd.DataFrame(matrix)

sns.set(rc={"figure.figsize":(15, 15)})
sns.heatmap(df, cmap=args.color_map, square=True, xticklabels=True, yticklabels=True, cbar=False)
#plt.show()
plt.savefig(args.output_file)

