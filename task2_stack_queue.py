"""Task 2 - Stacks, queues, circular queue and infix-to-postfix conversion."""


class Stack:
    """LIFO stack. With a limit, the oldest entry is discarded when full (navigation history)."""

    def __init__(self, limit=None):
        self._items = []
        self._limit = limit

    def push(self, item):
        if self._limit is not None and len(self._items) == self._limit:
            self._items.pop(0)               # drop the oldest entry
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def latest_first(self):
        return list(reversed(self._items))


class Queue:
    """FIFO queue backed by a Python list (simple version used for the shuttle schedule)."""

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)            # O(n): shifts the remaining items

    def front(self):
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def to_list(self):
        return list(self._items)


class CircularQueue:
    """Fixed-size circular array queue. One slot is kept empty, so it holds at most N-1 items.
    rear = index where the NEXT item will be written.
    empty: front == rear      full: (rear + 1) % N == front
    """

    def __init__(self, size):
        self.N = size
        self.data = [None] * size
        self.front_i = 0
        self.rear = 0

    def is_empty(self):
        return self.front_i == self.rear

    def is_full(self):
        return (self.rear + 1) % self.N == self.front_i

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("circular queue is full")
        self.data[self.rear] = item
        self.rear = (self.rear + 1) % self.N

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self.data[self.front_i]
        self.data[self.front_i] = None
        self.front_i = (self.front_i + 1) % self.N
        return item

    def front(self):
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self.data[self.front_i]


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def infix_to_postfix(tokens, show_trace=False):
    """Shunting-yard conversion (left-associative operators, parentheses supported)."""
    output, stack, rows = [], [], []
    for tok in tokens:
        if tok in PRECEDENCE:
            popped = []
            while stack and stack[-1] != "(" and PRECEDENCE[stack[-1]] >= PRECEDENCE[tok]:
                popped.append(stack[-1])
                output.append(stack.pop())
            stack.append(tok)
            action = (f"Pop {' '.join(popped)}, then push {tok}" if popped
                      else f"Push {tok}")
        elif tok == "(":
            stack.append(tok)
            action = "Push ("
        elif tok == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
            action = "Pop to output until ("
        else:
            output.append(tok)
            action = "Operand to output"
        rows.append((tok, " ".join(output), " ".join(stack) or "-", action))
    popped = []
    while stack:
        popped.append(stack[-1])
        output.append(stack.pop())
    rows.append(("End", " ".join(output), "-", f"Pop {' '.join(popped)}"))
    if show_trace:
        print(f"{'Token':6}{'Output':16}{'Stack (bottom->top)':22}Action")
        for r in rows:
            print(f"{r[0]:6}{r[1]:16}{r[2]:22}{r[3]}")
    return output, rows


if __name__ == "__main__":
    print("== 2(a) navigation history stack (limit 10) ==")
    history = Stack(limit=10)
    for b in ("Gate", "Admin", "Library"):
        history.push(b)
    print("peek:", history.peek())
    print("pop :", history.pop())
    print("is_empty:", history.is_empty(), "| latest first:", history.latest_first())
    big = Stack(limit=10)
    for k in range(1, 13):
        big.push(f"B{k}")
    print("after 12 pushes, limit 10 ->", big.latest_first())

    print("\n== 2(b) shuttle queue ==")
    shuttle = Queue()
    for s in ("Gate", "HostelA", "HostelB"):
        shuttle.enqueue(s)
    print("front   :", shuttle.front())
    print("dequeue :", shuttle.dequeue())
    print("remaining:", shuttle.to_list(), "| is_empty:", shuttle.is_empty())

    print("\n== 2(c) infix -> postfix:  A + B * C - D / E ==")
    out, _ = infix_to_postfix(["A", "+", "B", "*", "C", "-", "D", "/", "E"], show_trace=True)
    print("Postfix:", "".join(out))

    print("\n== 2(d) circular queue, N = 5 (holds 4 items) ==")
    cq = CircularQueue(5)
    for s in ("S1", "S2", "S3", "S4"):
        cq.enqueue(s)
    print("full after 4 enqueues:", cq.is_full())
    print("dequeue:", cq.dequeue(), cq.dequeue())
    cq.enqueue("S5"); cq.enqueue("S6")             # re-uses the freed slots (wrap-around)
    print("after wrap-around: front =", cq.front(), "| full:", cq.is_full(), "| array:", cq.data)
