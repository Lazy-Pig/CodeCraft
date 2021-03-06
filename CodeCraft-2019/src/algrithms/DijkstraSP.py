# -*- coding: UTF-8 -*-
from algrithms.IndexMinPQ import IndexMinPQ
import math
from queue import Queue


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
        self._path = {}
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
        if v in self._path:
            return self._path[v]

        if not self.has_path_to(v):
            raise Exception("没有找到路径：%d -> %d" % (self._source_id, v))

        path = []
        while True:
            road, direction = self._road_to[v]
            path.insert(0, (road, direction))
            v = road.get_destination_id() if v == road.get_source_id() else road.get_source_id()
            if v == self._source_id:
                break
        self._path[v] = path[:]
        return path

    def bfs(self, v):
        if v in self._path:
            return self._path[v][:]
        marked = {id: False for id in self._graph.get_cross_ids()}
        path_from = {id: None for id in self._graph.get_cross_ids()}
        q = Queue()
        marked[v] = True
        q.put(v)
        src = None
        flag = True
        while flag:
            dest = q.get()
            for road, direction, weight in self._graph.reverse_adj[dest]:
                src = road.get_source_id() if direction == 'positive' else road.get_destination_id()
                if not marked[src]:
                    path_from[src] = (road, direction)
                    marked[src] = True
                    q.put(src)
                if self.has_path_to(src) or src == self._source_id:
                    flag = False
                    break
            else:
                flag = not q.empty()
        if src != self._source_id:
            path = self.path_to(src)[:]
        else:
            path = []
        while src != v:
            path.append(path_from[src])
            road, direction = path_from[src]
            src = road.get_destination_id() if direction == 'positive' else road.get_source_id()
        self._path[v] = path[:]
        return path
