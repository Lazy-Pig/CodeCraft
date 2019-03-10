

class Road(object):
    def __init__(self, id, length, speed, channel, source_id, destination_id, is_duplex):
        self._id = id
        self._length = length
        self._speed = speed
        self._channel = channel
        self._source_id = source_id
        self._destination_id = destination_id
        self._is_duplex = is_duplex
        self._source = None
        self._destination = None

    def get_id(self):
        return self._id

    def get_length(self):
        return self._length

    def get_speed(self):
        return self._speed

    def get_channel_number(self):
        return self._channel

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

