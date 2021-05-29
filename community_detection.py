import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import community

from network_building import graph


def community_layout(g, partition):
    # compute the layout for a modular graph.
    # g -- networkx.Graphgraph
    # partition -- dict mapping graph partitions
    # returns node positions

    pos_communities = position_communities(g, partition, scale=3.)

    pos_nodes = position_nodes(g, partition, scale=1.)

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos


def position_communities(g, partition, **kwargs):
    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos


def find_between_community_edges(g, partition):
    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges


def position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)

    return pos


def run():
    # Largest connected component
    largest_subgraph = graph.subgraph(max(nx.connected_components(graph), key=len))

    partition = community.best_partition(largest_subgraph)
    pos = community_layout(largest_subgraph, partition)

    nx.draw(largest_subgraph, pos, node_color=list(partition.values()));
    plt.show()


run()
