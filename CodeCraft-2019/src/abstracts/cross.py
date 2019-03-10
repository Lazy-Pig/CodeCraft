

class Cross(object):
    def __init__(self, id, up_road_id, right_road_id, down_road_id, left_road_id):
        self._id = id
        self._road_id_list = [up_road_id, right_road_id, down_road_id, left_road_id]
        self._road_list = None

    def get_id(self):
        return self._id

    def get_road_id_list(self):
        return self._road_id_list

    def get_road_list(self):
        return self._road_list

    def set_road_list(self, roads):
        self._road_list = roads
