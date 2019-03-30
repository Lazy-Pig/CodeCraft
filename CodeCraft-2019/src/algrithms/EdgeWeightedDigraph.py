# -*- coding: UTF-8 -*-
import math


class EdgeWeightedDigraph(object):
    def __init__(self, roads, car=None, invalid_road_ids=[]):
        self._car = car
        self.adj = {}
        self.reverse_adj = {}
        self.roads = roads
        self.invalid_road_ids = invalid_road_ids
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
            if road.get_destination_id() not in self.reverse_adj:
                self.reverse_adj[road.get_destination_id()] = []
            if road.get_id() in self.invalid_road_ids:
                self.adj[road.get_source_id()].append((road, direction, math.inf))
                self.reverse_adj[road.get_destination_id()].append((road, direction, math.inf))
            else:
                # self.adj[road.get_source_id()].append((road, direction, road.get_weight(self._car, direction)))
                # self.adj[road.get_source_id()].append((road, direction, road.get_weight(self._car)))
                self.adj[road.get_source_id()].append((road, direction, road.get_weight()))
                self.reverse_adj[road.get_destination_id()].append((road, direction, road.get_weight()))
        else:
            if road.get_destination_id() not in self.adj:
                self.adj[road.get_destination_id()] = []
            if road.get_source_id() not in self.reverse_adj:
                self.reverse_adj[road.get_source_id()] = []
            if road.get_id() in self.invalid_road_ids:
                self.adj[road.get_source_id()].append((road, direction, math.inf))
                self.reverse_adj[road.get_source_id()].append((road, direction, math.inf))
            else:
                # self.adj[road.get_destination_id()].append((road, direction, road.get_weight(self._car, direction)))
                # self.adj[road.get_destination_id()].append((road, direction, road.get_weight(self._car)))
                self.adj[road.get_destination_id()].append((road, direction, road.get_weight()))
                self.reverse_adj[road.get_source_id()].append((road, direction, road.get_weight()))

    def get_cross_num(self):
        return self._cross_num

    def get_cross_ids(self):
        return self._cross_ids
