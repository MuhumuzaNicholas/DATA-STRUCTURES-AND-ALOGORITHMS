"""Task 5 - Sorting, searching and hashing."""


# ---------- 5(a) sorting ----------
def insertion_sort(values, trace=False):
    a = list(values)
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
        if trace:
            print(f"Pass {i}: {a}")
    return a


def merge_sort(values, trace=False, depth=0):
    a = list(values)
    pad = "  " * depth
    if len(a) <= 1:
        return a
    mid = (len(a) + 1) // 2                      # left half gets the extra element
    if trace:
        print(f"{pad}split {a} -> {a[:mid]} | {a[mid:]}")
    left = merge_sort(a[:mid], trace, depth + 1)
    right = merge_sort(a[mid:], trace, depth + 1)
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    if trace:
        print(f"{pad}merge {left} + {right} -> {merged}")
    return merged


def quick_sort(values):
    a = list(values)
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    return (quick_sort([x for x in a if x < pivot]) + [x for x in a if x == pivot]
            + quick_sort([x for x in a if x > pivot]))


# ---------- 5(c) binary search ----------
def binary_search(sorted_items, target):
    """Returns (index, steps); index is -1 when the target is absent. O(log n)."""
    lo, hi, steps = 0, len(sorted_items) - 1, 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if sorted_items[mid] == target:
            return mid, steps
        if sorted_items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, steps


# ---------- 5(d)-(f) hashing ----------
def key_to_int(key):
    """Integers are used as they are; strings (room codes) are turned into integers first."""
    if isinstance(key, int):
        return key
    h = 0
    for ch in str(key):
        h = h * 31 + ord(ch)
    return h


class LinearProbingTable:
    """Open addressing with linear probing. insert() returns the number of probes used."""

    def __init__(self, size=11):
        self.size = size
        self.slots = [None] * size

    def _h(self, key):
        return key_to_int(key) % self.size

    def insert(self, key, value=None):
        h, probes = self._h(key), 0
        for i in range(self.size):
            idx = (h + i) % self.size
            probes += 1
            if self.slots[idx] is None or self.slots[idx][0] == key:
                self.slots[idx] = (key, value)
                return probes
        raise OverflowError("hash table is full")

    def search(self, key):
        h, probes = self._h(key), 0
        for i in range(self.size):
            idx = (h + i) % self.size
            probes += 1
            if self.slots[idx] is None:
                return None, probes
            if self.slots[idx][0] == key:
                return self.slots[idx][1], probes
        return None, probes

    def keys_by_slot(self):
        return [s[0] if s else None for s in self.slots]


class ChainingTable:
    """Separate chaining. insert() returns probes = slot check + chain nodes examined."""

    def __init__(self, size=11):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _h(self, key):
        return key_to_int(key) % self.size

    def insert(self, key, value=None):
        bucket = self.buckets[self._h(key)]
        probes = 1
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return probes
            probes += 1
        bucket.append((key, value))
        return probes

    def search(self, key):
        bucket, probes = self.buckets[self._h(key)], 1
        for k, v in bucket:
            if k == key:
                return v, probes
            probes += 1
        return None, probes


class DoubleHashingTable:
    """h(k, i) = (h1(k) + i*h2(k)) mod m with h2(k) = 7 - (k mod 7); m must be prime."""

    def __init__(self, size=11):
        self.size = size
        self.slots = [None] * size

    def insert(self, key, value=None):
        k = key_to_int(key)
        h1, h2, probes = k % self.size, 7 - (k % 7), 0
        for i in range(self.size):
            idx = (h1 + i * h2) % self.size
            probes += 1
            if self.slots[idx] is None or self.slots[idx][0] == key:
                self.slots[idx] = (key, value)
                return probes
        raise OverflowError("hash table is full")


if __name__ == "__main__":
    data = [12, 11, 13, 5, 6]
    print("== 5(a) insertion sort trace ==")
    print("Start:", data)
    insertion_sort(data, trace=True)
    print("\n== 5(a) merge sort trace ==")
    print("Result:", merge_sort(data, trace=True))

    print("\n== 5(b) quicksort check ==", quick_sort([45, 12, 78, 33, 22, 90, 56]))

    print("\n== 5(c) binary search on a sorted building list ==")
    buildings = sorted(["ADM", "ART", "CAF", "ENG", "GYM", "HAL", "HST", "LEC1", "LIB", "MED", "SCI", "TEC"])
    for target in ("LIB", "ZZZ"):
        print(f"search {target}:", binary_search(buildings, target))

    keys = [22, 41, 53, 46, 30, 13, 1, 67]
    print("\n== 5(d) linear probing, m = 11, h(k) = k mod 11 ==")
    lp = LinearProbingTable(11)
    lp_probes = []
    for k in keys:
        p = lp.insert(k)
        lp_probes.append(p)
        print(f"insert {k:2d}: h = {k % 11:2d}, probes = {p}")
    print("slot :", list(range(11)))
    print("key  :", [x if x is not None else "-" for x in lp.keys_by_slot()])

    print("\n== 5(e) separate chaining ==")
    ch = ChainingTable(11)
    ch_probes = [ch.insert(k) for k in keys]
    for i, b in enumerate(ch.buckets):
        if b:
            print(f"slot {i:2d}:", " -> ".join(str(k) for k, _ in b))
    print("keys           :", keys)
    print("chaining probes:", ch_probes, "total =", sum(ch_probes), "avg =", sum(ch_probes) / 8)
    print("linear probes  :", lp_probes, "total =", sum(lp_probes), "avg =", sum(lp_probes) / 8)

    print("\n== 5(f) double hashing, h2(k) = 7 - (k mod 7) ==")
    dh = DoubleHashingTable(11)
    dh_probes = [dh.insert(k) for k in keys]
    print("probes:", dh_probes, "total =", sum(dh_probes))
    print("slot :", list(range(11)))
    print("key  :", [s[0] if s else "-" for s in dh.slots])
