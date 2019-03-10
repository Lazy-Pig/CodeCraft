

class Car(object):
    def __init__(self, id, source_id, destination_id, speed, plan_time):
        self._id = id
        self._source_id = source_id
        self._destination_id = destination_id
        self._speed = speed
        self._plan_time = plan_time
        self._source = None
        self._destination = None

    def get_id(self):
        return self._id

    def get_source_id(self):
        return self._source_id

    def get_source(self):
        return self._source

    def set_source(self, obj):
        self._source = obj

    def get_destination_id(self):
        return self._destination_id

    def get_destination(self):
        return self._destination

    def set_destination(self, obj):
        self._destination = obj

    def get_speed(self):
        return self._speed

    def get_plan_time(self):
        return self._plan_time
