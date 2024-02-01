


import sys
import csv
import networkx as nx #https://networkx.github.io/documentation/stable/install.html
import matplotlib.pyplot as plt #https://matplotlib.org/users/installing.html
from matplotlib.pyplot import cm
import numpy as np

#Input edge list
argv = sys.argv
if len(argv) < 2:
	print("Usage: # python %s filename" % argv[0])
	quit()
input_file = argv[1]

dataFile = csv.reader(open(input_file))
next(dataFile)

# Create a network
G = nx.Graph()
P = {} # edge attribute dictionary: "weight" and "media"
M = ["Multi"] # attribute list to calculate the number of node colors ("nColor")
for data in dataFile:
	data = list(map(lambda x:x.strip(), data))
	if data[2] not in M:
		M.append(data[2])
	e = (data[0], data[1])
	if G.has_edge(*e):
		if e in P:
			P[e]["weight"] += 1.0
			P[e]["media"] = "Multi"
		else:
			P[(e[1], e[0])]["weight"] += 1
			P[(e[1], e[0])]["media"] = "Multi"
	else:
		G.add_edge(*e)
		P[e] = {"weight":1.0, "media":data[2]}

# Find out the highest-degree node (i.e., the ego)
highestDegreeNode = sorted(G.degree(), key=lambda x:x[1], reverse=True)[0][0]

# Create colors for network visualization
ColorMap = {}
nColor = len(M)
color=plt.get_cmap("Set1")(np.linspace(0,1, nColor))
#color = ["r", "g", "b", "c", "m", "y", "violet", "indigo", "orange", "gold"]

for i in range(nColor):
	if M[i] == "Multi":
		ColorMap[M[i]] = [0.4, 0.4, 0.4, 1.0]
	else:
		ColorMap[M[i]] = color[i]

Weight = []
EdgeColor = []
NodeMedia = {}
for e in G.edges():
	# Assingn edge weight and color
	media = None
	if e in P:
		Weight.append(P[e]["weight"] * 1.5)
		EdgeColor.append(ColorMap[P[e]["media"]])
		media = P[e]["media"]
	else:
		Weight.append(P[(e[1], e[0])]["weight"] * 1.5)
		EdgeColor.append(ColorMap[P[(e[1], e[0])]["media"]])
		media = P[(e[1], e[0])]["media"]

	# Find a node type based on the meida type to connect with the ego
	if e[0] == highestDegreeNode:
		if (e[1]) in NodeMedia:
			if NodeMedia[e[1]] != media:
				NodeMedia[e[1]] = "Multi"
		else:
			NodeMedia[e[1]] = media
	elif e[1] == highestDegreeNode:
		if (e[0]) in NodeMedia:
			if NodeMedia[e[0]] != media:
				NodeMedia[e[0]] = "Multi"
		else:
			NodeMedia[e[0]] = media


NodeMedia["Me"] = "Me"
ColorMap["Me"] = [1.0, 1.0, 1.0, 1.0]

# Create node list based on the media type to connect with the ego
#print(NodeMedia)
#print(G.nodes())

NodeList = {}
for n in G.nodes():

	nm = NodeMedia[n]
	if nm in NodeList:
		NodeList[nm].append(n)
	else:
		NodeList[nm] = [n]

# Making a network figure for observation (with node labels)
fig, ax = plt.subplots(1, figsize=(10,10))
pos = nx.spring_layout(G)
for k, v in NodeList.items():
	nList = v
	nc = ColorMap[k]
	nodes = nx.draw_networkx_nodes(G, pos, nodelist=nList, node_size=1500, label=k, linewidths=1.0) #1500
	nodes.set_facecolor(nc)
	nodes.set_edgecolor('k')
nx.draw_networkx_edges(G, pos, width=Weight, edge_color=EdgeColor)
nx.draw_networkx_labels(G, pos)
ax.legend(scatterpoints=1, markerscale=0.3, loc="lower right", framealpha=0.8)
plt.axis("off")
plt.savefig("network1_for_observation.pdf")

# Making another network figure for observation (without node labels)
fig, ax = plt.subplots(1, figsize=(10,10))
pos = nx.spring_layout(G)
for k, v in NodeList.items():
	nList = v
	nc = ColorMap[k]
	nodes = nx.draw_networkx_nodes(G, pos, nodelist = nList, node_size=1500, label=k, linewidths=1.0)
	nodes.set_facecolor(nc)
	nodes.set_edgecolor('k')
nx.draw_networkx_edges(G, pos, width=Weight, edge_color=EdgeColor)
ax.legend(scatterpoints=1, markerscale=0.3, loc="lower right", framealpha=0.8)
plt.axis("off")
plt.savefig("network2_for_submission.pdf")
