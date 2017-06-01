class FenwickTree():
    """
    Implementation of a Fenwick Tree. Only works with numbers.
    Supports RANGE UPDATE and POINT QUERY.
    Indexed from 0.
    """
    def __init__(self, size):
        # Index from 1 internally
        self.data = [0] * (size + 1)

    def _is_valid(self, key):
        if isinstance(key, int):
            if key < 0 or key >= len(self.data):
                raise KeyError()
        elif isinstance(key, slice):
            if key.start < 0 or key.stop >= len(self.data):
                raise KeyError()
        else:
            raise TypeError()

    def _lsb(self, idx):
        return idx & (-idx)

    def __getitem__(self, key):
        self._is_valid(key)
        if isinstance(key, slice):
            return self._get_range(slice.start, slice.stop)

        return self._get(key)

    def _get(self, idx):
        """
        Gets the value at index idx
        """
        # Adjunst index for internal idxing from 1
        idx += 1
        res = 0
        while idx > 0:
            res += self.data[idx]
            idx -= self._lsb(idx)

        return res

    def _add(self, idx, value):
        # Adjust index for internal idxing from 1
        self._is_valid(idx)
        idx += 1

        while idx < len(self.data):
            self.data[idx] += value
            idx += self._lsb(idx)

    def add_range(self, start, stop, value=1):
        self._is_valid(slice(start, stop))

        self._add(start, value)
        self._add(stop + 1, -value)
