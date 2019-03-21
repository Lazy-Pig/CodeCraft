# -*- coding: UTF-8 -*-


class IndexMinPQ(object):
    def __init__(self, max_size):
        assert max_size > 0
        self._max_size = max_size
        self._index = [-1] * (max_size + 1)
        self._reverse_index = [-1] * (max_size + 1)
        self._keys = [None] * (max_size + 1)
        self._keys_size = 0

    def is_empty(self):
        return self._keys_size == 0

    def size(self):
        return self._keys_size

    def contains(self, index):
        if index < 0 or index >= self._max_size:
            return False
        return self._reverse_index[index] != -1

    def insert(self, index, element):
        if index < 0 or index >= self._max_size or self.contains(index):
            return

        self._keys_size += 1
        self._index[self._keys_size] = index
        self._reverse_index[index] = self._keys_size
        self._keys[index] = element
        self.swim(self._keys_size)

    def min_index(self):
        return None if self._keys_size == 0 else self._index[1]

    def min_key(self):
        return None if self._keys_size == 0 else self._keys[self._index[1]]

    def exchange(self, pos_a, pos_b):
        self._index[pos_a], self._index[pos_b] = self._index[pos_b], self._index[pos_a]
        self._reverse_index[self._index[pos_a]] = pos_a
        self._reverse_index[self._index[pos_b]] = pos_b

    def swim(self, pos):
        while pos > 1 and self._keys[self._index[pos // 2]] > self._keys[self._index[pos]]:
            self.exchange(pos // 2, pos)
            pos //= 2

    def sink(self, pos):
        length = self._keys_size
        while 2 * pos <= length:
            tmp = 2 * pos
            if tmp < length and self._keys[self._index[tmp]] > self._keys[self._index[tmp + 1]]:
                tmp += 1
            if not self._keys[self._index[tmp]] < self._keys[self._index[pos]]:
                break
            self.exchange(tmp, pos)
            pos = tmp

    def change_key(self, i, key):
        if i < 0 or i >= self._max_size or not self.contains(i):
            return
        self._keys[i] = key
        self.swim(self._reverse_index[i])
        self.sink(self._reverse_index[i])

    def delete_min(self):
        if self._keys_size == 0:
            return
        min_index = self._index[1]
        self.exchange(1, self._keys_size)
        self._keys_size -= 1
        self.sink(1)
        self._reverse_index[min_index] = -1
        self._keys[self._index[self._keys_size + 1]] = None
        self._index[self._keys_size + 1] = -1
        return min_index
