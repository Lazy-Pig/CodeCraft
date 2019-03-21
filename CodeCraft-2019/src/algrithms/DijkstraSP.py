# -*- coding: UTF-8 -*-
from algrithms.IndexMinPQ import IndexMinPQ
import math


class DijkstraSP(object):
    def __init__(self, graph, source_id):
        self._graph = graph
        self._source_id = source_id
        self._road_to = {}
        self._dist_to = {}
        self._pq = IndexMinPQ(graph.get_cross_num() + 1)

        for cross_id in graph.get_cross_ids():
            self._dist_to[cross_id] = math.inf
        self._dist_to[source_id] = 0.0
        self._pq.insert(source_id, 0.0)
        while not self._pq.is_empty():
            self.relax(self._graph, self._pq.delete_min())

    def relax(self, graph, v):
        for road, direction, weight in graph.adj[v]:
            w = road.get_destination_id() if direction == 'positive' else road.get_source_id()
            if self._dist_to[w] > self._dist_to[v] + weight:
                self._dist_to[w] = self._dist_to[v] + weight
                self._road_to[w] = (road, direction)
                if self._pq.contains(w):
                    self._pq.change_key(w, self._dist_to[w])
                else:
                    self._pq.insert(w, self._dist_to[w])

    def dist_to(self, v):
        return self._dist_to[v]

    def has_path_to(self, v):
        return self._dist_to[v] < math.inf

    def path_to(self, v):
        if not self.has_path_to(v):
            draw_graph(self, v)
            return None

        path = []
        while True:
            road, direction = self._road_to[v]
            path.insert(0, (road, direction))
            v = road.get_destination_id() if v == road.get_source_id() else road.get_source_id()
            if v == self._source_id:
                break
        return path

import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(dijkstra, v):
    G = nx.DiGraph()
    edges = []
    one_way_edges = []
    for road in dijkstra._graph.roads:
        edges.append((str(road.get_source_id()), str(road.get_destination_id())))
        if not road.is_duplex():
            one_way_edges.append((str(road.get_source_id()), str(road.get_destination_id())))
    G.add_edges_from(edges)
    node_values = [0.0 if node == str(v) or node == str(dijkstra._source_id) else 0.25 for node in G.nodes()]
    shortest_path = [(str(road.get_source_id()), str(road.get_destination_id())) for road, d in dijkstra._road_to.values()]
    print(dijkstra._road_to)
    print(dijkstra._dist_to)
    print(shortest_path)
    black_edges = [edge for edge in G.edges() if edge not in shortest_path]
    black_edges_with_arrows = []
    black_edges_without_arrows = []
    for edge in black_edges:
        if edge in one_way_edges:
            black_edges_with_arrows.append(edge)
        else:
            black_edges_without_arrows.append(edge)

    shortest_path_with_arrows = []
    shortest_path_without_arrows = []
    for edge in shortest_path:
        if edge in one_way_edges:
            shortest_path_with_arrows.append(edge)
        else:
            shortest_path_without_arrows.append(edge)

    # print(shortest_path_with_arrows)
    print(shortest_path_without_arrows)
    # print(black_edges_with_arrows)
    print(black_edges_without_arrows)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                           node_color=node_values, node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=shortest_path_with_arrows, edge_color='r', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=shortest_path_without_arrows, edge_color='r', arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges_with_arrows, arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges_without_arrows, arrows=False)
    plt.show()
