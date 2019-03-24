from algrithms.DijkstraSP import DijkstraSP


class BaseScheduler(object):
    def __init__(self, id_2_cars, id_2_roads, id_2_cross):
        self._id_2_cars = id_2_cars
        self._id_2_roads = id_2_roads
        self._id_2_cross = id_2_cross
        self._not_start_cars_ids = sorted(id_2_cars.keys())
        self._running_cars = []
        self._arrived_cars = []

    def is_all_arrived(self):
        return len(self._arrived_cars) == len(self._id_2_cars)

    def scheduling(self, global_tick):
        raise NotImplementedError

    def _plan_path(self, graph, source_id, destination_id):
        shortest = DijkstraSP(graph, source_id)
        path = shortest.path_to(destination_id)
        return path

    def arrived(self, car):
        self._arrived_cars.append(car.get_id())
        self._running_cars.remove(car.get_id())
