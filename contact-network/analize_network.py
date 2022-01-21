import networkx as nx
import numpy as np
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import dzcnapy_plotlib as dzcnapy
import community
from math import log,exp
from os import path
from collections import Counter
from networkx.drawing.nx_agraph import graphviz_layout
from scipy.interpolate import interp1d

FILE = "mean-results/mean_contacts-time.csv"
with open(FILE, "rb") as infile:
    adj_mat = np.loadtxt(infile, dtype=float, delimiter=",")
    G       = nx.from_numpy_matrix(adj_mat, create_using=nx.DiGraph())
    G.edges(data=True)

#edge_weights = nx.get_edge_attributes(G, 'weight')
#G.remove_edges_from((e for e, w in edge_weights.items() if w < 15))

with open("mean_contacts-time.graphml", "wb") as ofile:
    nx.write_graphml(G, ofile)

# Number of nodes and edges
N = len(G.nodes())
E = len(G.edges())

print("Number of nodes:", N)
print("Number of edges:", E)

# Density
print("Density:", nx.density(G))

print (sorted(G.edges(data=True), key= lambda x: x[2]['weight'], reverse=True))

# Average distance (consider only Giant SCC if the network/graph is disconnected)
sorted_strongly_components = sorted((G.subgraph(c) for c in nx.strongly_connected_components(G)), key=len, reverse=True)
GSCC = sorted_strongly_components[0]
average_distance = nx.average_shortest_path_length(GSCC)
print("Average distance:", average_distance)

# Distance distribution plot
distances = nx.shortest_path_length(G)
values = [list(item[1].values()) for item in distances]
flat_values = [item for sublist in values for item in sublist]
count = Counter(flat_values)
#x: distance, y: number of paths
x = [el[0] for el in count.items() if el[0] != 0]
y = [el[1] for el in count.items() if el[0] != 0]

plt.figure(1)
plt.scatter(x, y, s=100, c="red")
plt.title("Distance distribution")
plt.xlim(0, max(x))
plt.ylim(0, max(y))
plt.xlabel("Distance")
plt.ylabel("Number of paths")
dzcnapy.plot("Distance distribution", True)

# Standard deviation of distance distribution
std_distances = np.std(flat_values)
print("Standard deviation of Gaussian (distance) distribution:", std_distances)

# Average, variance and standard deviation degree (also in and out degree)
def average_degree(degrees, str):
    average_degree = np.mean(degrees)
    print("Average", str, ":", average_degree)
    variance_degree = np.var(degrees)
    print("Variance", str, ":", variance_degree)
    std_degree = np.std(degrees)
    print("Standard deviation", str, ":" , std_degree)

# Degree
degrees = list(G.degree())
degrees_list = [degree for _, degree in degrees]
# In degree
in_degrees = list(G.in_degree())
in_degrees_list = [degree for _, degree in in_degrees]
#Out degree
out_degrees = list(G.out_degree())
out_degrees_list = [degree for _, degree in out_degrees]

average_degree(degrees_list, "degree")
average_degree(in_degrees_list, "in degree")
average_degree(out_degrees_list, "out degree")

# Degree distribution plot
count = Counter(degrees_list)
#x: degree, y: number of nodes
x = [el[0] for el in count.items()]
y = [el[1] for el in count.items()]
x, y = zip(*sorted(zip(x, y)))
xx = x[5:70]
yy = y[5:70]
xvalues = np.linspace(min(x), max(x), 100)
f = np.polyfit([log(el) for el in xx], [log(el) for el in yy], 1)
c = f[0]
a = exp(f[1])
print("Degree -> Slope:", c)
print("Degree -> Y-intercept:", a)

plt.figure(2)
plt.plot(x, y, 'bo', xvalues, a*(xvalues**c), 'r-')
plt.xscale("log")
plt.yscale("log")
plt.title("Degree distribution")
plt.xlim(1, max(x))
plt.ylim(1, max(y))
plt.xlabel("Degree")
plt.ylabel("Number of nodes")
dzcnapy.plot("Degree distribution", True)

# In degree distribution plot
count = Counter(in_degrees_list)
#x: in_degree, y: number of nodes
x = [el[0] for el in count.items()]
y = [el[1] for el in count.items()]
x, y = zip(*sorted(zip(x, y)))
xx = x[5:70]
yy = y[5:70]
xvalues = np.linspace(1, max(x), 100)
f = np.polyfit([log(el) for el in xx], [log(el) for el in yy], 1)
c = f[0]
a = exp(f[1])
print("In-degree -> Slope:", c)
print("In-degree -> Y-intercept:", a)

plt.figure(3)
plt.plot(x, y, 'bo', xvalues, a*(xvalues**c), 'r-')
plt.xscale("log")
plt.yscale("log")
plt.title("In degree distribution")
plt.xlim(1, max(x))
plt.ylim(1, max(y))
plt.xlabel("In degree")
plt.ylabel("Number of nodes")
dzcnapy.plot("In degree distribution", True)

# Out degree distribution plot
count = Counter(out_degrees_list)
#x: out_degree, y: number of nodes
x = [el[0] for el in count.items()]
y = [el[1] for el in count.items()]
x, y = zip(*sorted(zip(x, y)))
xx = x[5:70]
yy = y[5:70]
xvalues = np.linspace(1, max(x), 100)
f = np.polyfit([log(el) for el in xx], [log(el) for el in yy], 1)
c = f[0]
a = exp(f[1])
print("Out-degree -> Slope:", c)
print("Out-degree -> Y-intercept:", a)

plt.figure(4)
plt.plot(x, y, 'bo', xvalues, a*(xvalues**c), 'r-')
plt.xscale("log")
plt.yscale("log")
plt.title("Out degree distribution")
plt.xlim(1, max(x))
plt.ylim(1, max(y))
plt.xlabel("Out degree")
plt.ylabel("Number of nodes")
dzcnapy.plot("Out degree distribution", True)

G_undirected = G.to_undirected()

# Average clustering coefficient (on an undirected version of the graph)
avg_cc = nx.average_clustering(G_undirected)
print("Average clustering coefficient:", avg_cc)

# Clustering coefficient distribution (on an undirected version of the graph)
ccs = nx.clustering(G_undirected)
ccs_list = [cc for _, cc in ccs.items()]

plt.figure(5)
plt.scatter(degrees_list, ccs_list, c="black")
plt.title("Clustering coefficient distribution")
plt.xlim(0, max(degrees_list))
plt.ylim(0, max(ccs_list))
plt.xlabel("Degree")
plt.ylabel("Clustering coefficient")
dzcnapy.plot("Clustering coefficient distribution", True)

# Transitivity (on an undirected version of the graph)
tr = nx.transitivity(G_undirected)
print("Transitivity:", tr)

# Giant strongly connected component and other components (already extract)
print("Number of strongly connected components:", len(sorted_strongly_components))
print("Dimension of GSCC:", len(GSCC))

# Weakly connected components
weakly_components = sorted((G.subgraph(c) for c in nx.weakly_connected_components(G)), key=len, reverse=True)
GWCC = weakly_components[0]
print("Number of weakly connected components:", len(weakly_components))
print("Dimension of GWCC:", len(GWCC))

# Eccentricity
ecc = nx.eccentricity(GSCC)
diameter = nx.diameter(GSCC, ecc)
radius = nx.radius(GSCC, ecc)
center = nx.center(GSCC, ecc)
periphery = nx.periphery(GSCC, ecc)

print("Diameter:", diameter)
print("Radius:", radius)
print("Center:", center)
print("Center (number of nodes):", len(center))
print("Periphery (number of nodes):", len(periphery))
print("Periphery:", periphery)

# Degree assortativity (with plot)
deg_ass = nx.degree_assortativity_coefficient(G)
print("Degree assortativity:", deg_ass)

avg_neigh_degree = nx.k_nearest_neighbors(G)
# Degree
avg_neigh_degree_k = avg_neigh_degree.keys()
# Average neighbor degree
avg_neigh_degree_v = avg_neigh_degree.values()

plt.figure(6)
plt.scatter(avg_neigh_degree_k, avg_neigh_degree_v, c="green")
plt.title("Assortativeness")
plt.xlim(0, max(avg_neigh_degree_k))
plt.ylim(0, max(avg_neigh_degree_v))
plt.xlabel("Degree")
plt.ylabel("Average Neighbor Degree")
dzcnapy.plot("Assortativeness", True)

# Centralities
degree_centralities = nx.degree_centrality(G)
in_degree_centralities = nx.in_degree_centrality(G)
out_degree_centralities = nx.out_degree_centrality(G)
betweenness_centralities = nx.betweenness_centrality(G)
closeness_centralities = nx.closeness_centrality(G)
eigenvector_centralities = nx.eigenvector_centrality(G)
page_rank_centralities = nx.pagerank(G)
hits_centralities = nx.hits(G)

print(pd.DataFrame(sorted(degree_centralities.items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "Degree centrality"}))
print(pd.DataFrame(sorted(in_degree_centralities.items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "In-degree centrality"}))
print(pd.DataFrame(sorted(out_degree_centralities.items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "Out-degree centrality"}))
print(pd.DataFrame(sorted(betweenness_centralities.items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "Betweennes centrality"}))
print(pd.DataFrame(sorted(closeness_centralities.items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "Closeness centrality"}))
print(pd.DataFrame(sorted(eigenvector_centralities.items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "Eigenvector centrality"}))
print(pd.DataFrame(sorted(page_rank_centralities.items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "PageRank centrality"}))
print(pd.DataFrame(sorted(hits_centralities[0].items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "HITS Hub centrality"}))
print(pd.DataFrame(sorted(hits_centralities[1].items(), key=lambda c: c[1], reverse=True)[:10]).rename(columns={0: "Node", 1: "HITS Authority centrality"}))
