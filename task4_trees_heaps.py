"""Task 4 - Binary search tree, min-heap and heap sort (all implemented from scratch)."""


class BSTNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key, value=None):
        if self.root is None:
            self.root = BSTNode(key, value)
            self.size += 1
            return
        cur = self.root
        while True:
            if key == cur.key:
                cur.value = value               # duplicate key: update the record
                return
            side = "left" if key < cur.key else "right"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, BSTNode(key, value))
                self.size += 1
                return
            cur = nxt

    def search(self, key):
        """Returns (value, comparisons) or (None, comparisons) when not found."""
        cur, steps = self.root, 0
        while cur:
            steps += 1
            if key == cur.key:
                return cur.value, steps
            cur = cur.left if key < cur.key else cur.right
        return None, steps

    def delete(self, key):
        self.root, removed = self._delete(self.root, key)
        if removed:
            self.size -= 1
        return removed

    def _delete(self, node, key):
        if node is None:
            return None, False
        if key < node.key:
            node.left, removed = self._delete(node.left, key)
        elif key > node.key:
            node.right, removed = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            succ = node.right                    # in-order successor = smallest in right subtree
            while succ.left:
                succ = succ.left
            node.key, node.value = succ.key, succ.value
            node.right, _ = self._delete(node.right, succ.key)
            removed = True
        return node, removed

    def inorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); out.append(n.key); go(n.right)
        go(self.root)
        return out

    def preorder(self):
        out = []
        def go(n):
            if n:
                out.append(n.key); go(n.left); go(n.right)
        go(self.root)
        return out

    def postorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); go(n.right); out.append(n.key)
        go(self.root)
        return out

    def height(self):
        def h(n):
            return 0 if n is None else 1 + max(h(n.left), h(n.right))
        return h(self.root)

    def draw(self):
        """Sideways text drawing (right subtree on top) for the report/demo."""
        lines = []
        def go(n, depth):
            if n:
                go(n.right, depth + 1)
                lines.append("    " * depth + str(n.key))
                go(n.left, depth + 1)
        go(self.root, 0)
        return "\n".join(lines)


class MinHeap:
    """Array-based binary min-heap. Children of index i are 2i+1 and 2i+2."""

    def __init__(self):
        self.a = []

    def __len__(self):
        return len(self.a)

    def push(self, item):
        self.a.append(item)
        i = len(self.a) - 1
        while i > 0 and self.a[(i - 1) // 2] > self.a[i]:       # bubble up
            p = (i - 1) // 2
            self.a[i], self.a[p] = self.a[p], self.a[i]
            i = p

    def peek(self):
        return self.a[0]

    def pop(self):
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            i, n = 0, len(self.a)
            while True:                                          # sift down
                l, r, s = 2 * i + 1, 2 * i + 2, i
                if l < n and self.a[l] < self.a[s]:
                    s = l
                if r < n and self.a[r] < self.a[s]:
                    s = r
                if s == i:
                    break
                self.a[i], self.a[s] = self.a[s], self.a[i]
                i = s
        return top

    def push_top_k(self, item, k):
        """Keep only the k largest items: a min-heap of size k has the k-th largest at its root."""
        if len(self.a) < k:
            self.push(item)
        elif item > self.a[0]:
            self.pop()
            self.push(item)

    def top_n(self, n):
        """n largest items, biggest first. Works on a copy, so the heap is unchanged."""
        copy = MinHeap()
        copy.a = list(self.a)
        ordered = []
        while len(copy):
            ordered.append(copy.pop())
        return list(reversed(ordered))[:n]


def _sift_down_max(a, i, n):
    while True:
        l, r, big = 2 * i + 1, 2 * i + 2, i
        if l < n and a[l] > a[big]:
            big = l
        if r < n and a[r] > a[big]:
            big = r
        if big == i:
            return
        a[i], a[big] = a[big], a[i]
        i = big


def heap_sort_trace(values):
    """Heap sort with a max-heap. Returns the built heap and the array after each extraction."""
    a = list(values)
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):                          # build max-heap
        _sift_down_max(a, i, n)
    built = list(a)
    steps = []
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]                              # move the maximum to its final place
        _sift_down_max(a, 0, end)
        steps.append((a[end], list(a)))
    return built, steps


if __name__ == "__main__":
    print("== 4(a) BST of campus buildings (insertion order below) ==")
    order = ["LIB", "HST", "SCI", "ADM", "LEC1", "MED", "TEC", "ENG", "CAF", "GYM", "ART", "HAL"]
    tree = BST()
    for code in order:
        tree.insert(code)
    print("inserted:", order)
    print(tree.draw())
    print("height:", tree.height())

    print("\n== 4(b) traversals ==")
    print("Inorder  :", tree.inorder())
    print("Preorder :", tree.preorder())
    print("Postorder:", tree.postorder())

    print("\n== 4(c) delete ENG (two children) ==")
    tree.delete("ENG")
    print(tree.draw())
    print("Preorder after deletion:", tree.preorder())

    print("\n== 4(d) min-heap of the 8 busiest locations ==")
    footfall = [("Gate", 4200), ("Cafeteria", 3100), ("Library", 2400), ("HostelA", 2700),
                ("Lecture1", 1800), ("Admin", 1500), ("Sports", 950), ("Annex", 700)]
    heap = MinHeap()
    for name, f in footfall:
        heap.push((f, name))
    print("heap array (footfall):", [f for f, _ in heap.a])
    print("heap array (names)   :", [n for _, n in heap.a])

    print("\n== 4(e) heap sort of [45, 12, 78, 33, 22, 90, 56] ==")
    built, steps = heap_sort_trace([45, 12, 78, 33, 22, 90, 56])
    print("max-heap built:", built)
    for val, arr in steps:
        print(f"after extracting {val:2d}:", arr)
    print("sorted:", steps[-1][1])
