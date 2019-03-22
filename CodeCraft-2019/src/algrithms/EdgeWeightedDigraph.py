# -*- coding: UTF-8 -*-


class EdgeWeightedDigraph(object):
    def __init__(self, car, roads):
        self._car = car
        self.adj = {}
        self.roads = roads
        for road in roads:
            self.add_road(road, 'positive')
            if road.is_duplex():
                self.add_road(road, 'negative')
        self._cross_num = len(self.adj)
        self._cross_ids = self.adj.keys()

    def add_road(self, road, direction):
        if direction == 'positive':
            if road.get_source_id() not in self.adj:
                self.adj[road.get_source_id()] = []
            self.adj[road.get_source_id()].append((road, direction, road.get_weight(self._car, direction)))
        else:
            if road.get_destination_id() not in self.adj:
                self.adj[road.get_destination_id()] = []
            self.adj[road.get_destination_id()].append((road, direction, road.get_weight(self._car, direction)))

    def get_cross_num(self):
        return self._cross_num

    def get_cross_ids(self):
        return self._cross_ids
