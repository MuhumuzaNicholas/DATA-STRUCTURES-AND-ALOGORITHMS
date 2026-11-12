"""Task 1 - Algorithm analysis demonstrations (BCS 2105)."""
import time


def count_equal_pairs(A):
    """Task 1(c): the nested loop from the brief. Returns (count, comparisons)."""
    count = 0
    comparisons = 0
    n = len(A)
    for i in range(n):
        for j in range(n):
            comparisons += 1          # the A[i] == A[j] test
            if A[i] == A[j]:
                count += 1
    return count, comparisons


class DynamicArray:
    """Task 1(e): array that doubles its capacity when full, counting the work done."""

    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.data = [None] * self.capacity
        self.operations = 0           # element writes + element copies

    def append(self, item):
        if self.size == self.capacity:            # full -> resize
            self.capacity *= 2
            new_data = [None] * self.capacity
            for k in range(self.size):            # copy every old element
                new_data[k] = self.data[k]
                self.operations += 1
            self.data = new_data
        self.data[self.size] = item
        self.size += 1
        self.operations += 1                      # the ordinary write


def linear_search(items, target):
    for k, v in enumerate(items):
        if v == target:
            return k
    return -1


if __name__ == "__main__":
    print("== 1(c) nested loop: comparisons grow as n^2 ==")
    for n in (10, 20, 40, 80):
        _, comps = count_equal_pairs(list(range(n)))
        print(f"n={n:3d}  comparisons={comps:5d}  n^2={n*n}")

    print("\n== 1(e) dynamic array: total operations for n appends ==")
    for n in (8, 64, 1000, 100000):
        arr = DynamicArray()
        for k in range(n):
            arr.append(k)
        print(f"n={n:6d}  total ops={arr.operations:7d}  3n={3*n:7d}  ops/n={arr.operations/n:.2f}")

    print("\n== 1(d) linear search timing (illustration only; times depend on the machine) ==")
    for n in (12, 10000):
        data = list(range(n))
        t0 = time.perf_counter()
        for _ in range(2000):
            linear_search(data, n - 1)
        t1 = time.perf_counter()
        print(f"n={n:6d}  avg linear search = {(t1 - t0) / 2000 * 1e6:.2f} microseconds")
