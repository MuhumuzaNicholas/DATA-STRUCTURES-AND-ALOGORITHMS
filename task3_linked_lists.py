"""Task 3 - Linked lists: singly, doubly, circular, and Floyd cycle detection."""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_head(self, value):               # O(1)
        node = Node(value)
        node.next = self.head
        self.head = node

    def insert_tail(self, value):               # O(n): no tail pointer
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def delete(self, value):                    # O(n); returns True if something was removed
        prev, cur = None, self.head
        while cur:
            if cur.value == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return True
            prev, cur = cur, cur.next
        return False

    def traverse(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out


def has_cycle(head):
    """Floyd's tortoise-and-hare: O(n) time, O(1) extra space."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


class DNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_tail(self, value):
        node = DNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def forward(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def backward(self):
        out, cur = [], self.tail
        while cur:
            out.append(cur.value)
            cur = cur.prev
        return out


class CircularLinkedList:
    """Continuous shuttle route: the last node points back to the first."""

    def __init__(self):
        self.tail = None                        # tail.next is the head

    def insert_tail(self, value):
        node = Node(value)
        if self.tail is None:
            node.next = node
        else:
            node.next = self.tail.next
            self.tail.next = node
        self.tail = node

    def traverse_from(self, start):
        """List the stops starting at `start`, visiting each stop once."""
        if self.tail is None:
            return []
        cur = self.tail.next
        while cur.value != start:               # find the starting stop
            cur = cur.next
            if cur is self.tail.next:
                raise ValueError(f"{start!r} is not on the route")
        out, first = [], cur
        while True:
            out.append(cur.value)
            cur = cur.next
            if cur is first:
                break
        return out


if __name__ == "__main__":
    print("== 3(a) singly linked list of shuttle stops ==")
    stops = SinglyLinkedList()
    for s in ("Main Gate", "Hostel A", "Hostel B"):
        stops.insert_tail(s)
    stops.insert_head("Town Centre")
    print("traverse:", stops.traverse())
    print("delete 'Hostel A':", stops.delete("Hostel A"), "->", stops.traverse())
    print("delete 'Nowhere' :", stops.delete("Nowhere"))

    print("\n== 3(b) doubly linked list: moving back and forth ==")
    d = DoublyLinkedList()
    for s in ("Main Gate", "Hostel A", "Hostel B", "Town Centre"):
        d.insert_tail(s)
    print("forward :", d.forward())
    print("backward:", d.backward())

    print("\n== 3(c) Floyd cycle detection ==")
    plain = SinglyLinkedList()
    plain.insert_tail("Gate"); plain.insert_tail("Library")
    print("acyclic list ->", has_cycle(plain.head))
    cyclic = SinglyLinkedList()
    cyclic.insert_tail("Gate"); cyclic.insert_tail("Library")
    cyclic.head.next.next = cyclic.head
    print("cyclic list  ->", has_cycle(cyclic.head))

    print("\n== 3(e) circular linked list: continuous shuttle route ==")
    route = CircularLinkedList()
    for s in ("Main Gate", "Hostel A", "Hostel B", "Town Centre"):
        route.insert_tail(s)
    print("from Main Gate  :", route.traverse_from("Main Gate"))
    print("from Hostel B   :", route.traverse_from("Hostel B"))
