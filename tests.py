"""Quick self-checks for the key results in the report. Run: python tests.py"""
from task2_stack_queue import Stack, Queue, CircularQueue, infix_to_postfix
from task3_linked_lists import SinglyLinkedList, has_cycle, CircularLinkedList
from task4_trees_heaps import BST, MinHeap, heap_sort_trace
from task5_sort_search_hash import (insertion_sort, merge_sort, binary_search,
                                    LinearProbingTable, ChainingTable)
from main import (CAMPUS_GRAPH, check_graph, dfs, bfs, dijkstra, dijkstra_heap)


def test_stack_queue():
    s = Stack(limit=3)
    for x in "abcd":
        s.push(x)
    assert s.latest_first() == ["d", "c", "b"]
    q = Queue(); q.enqueue(1); q.enqueue(2)
    assert q.dequeue() == 1 and q.front() == 2
    cq = CircularQueue(5)
    for x in range(4):
        cq.enqueue(x)
    assert cq.is_full()
    assert "".join(infix_to_postfix(list("A+B*C-D/E"))[0]) == "ABC*+DE/-"


def test_linked_lists():
    l = SinglyLinkedList()
    l.insert_tail("b"); l.insert_head("a"); l.insert_tail("c")
    assert l.traverse() == ["a", "b", "c"] and l.delete("b") and l.traverse() == ["a", "c"]
    assert not has_cycle(l.head)
    l.head.next.next = l.head
    assert has_cycle(l.head)
    c = CircularLinkedList()
    for x in "wxyz":
        c.insert_tail(x)
    assert c.traverse_from("y") == ["y", "z", "w", "x"]


def test_trees_heaps():
    t = BST()
    for k in ["LIB", "HST", "SCI", "ADM", "LEC1", "MED", "TEC", "ENG", "CAF", "GYM", "ART", "HAL"]:
        t.insert(k)
    assert t.inorder() == sorted(t.inorder())
    t.delete("ENG")
    assert "ENG" not in t.inorder() and t.size == 11
    h = MinHeap()
    for v in [4200, 3100, 2400, 2700, 1800, 1500, 950, 700]:
        h.push(v)
    assert h.a == [700, 950, 1500, 2400, 2700, 3100, 1800, 4200]
    built, steps = heap_sort_trace([45, 12, 78, 33, 22, 90, 56])
    assert built == [90, 33, 78, 12, 22, 45, 56]
    assert steps[-1][1] == [12, 22, 33, 45, 56, 78, 90]


def test_sort_search_hash():
    assert insertion_sort([12, 11, 13, 5, 6]) == merge_sort([12, 11, 13, 5, 6]) == [5, 6, 11, 12, 13]
    assert binary_search([1, 3, 5, 7], 7)[0] == 3 and binary_search([1, 3, 5, 7], 4)[0] == -1
    keys = [22, 41, 53, 46, 30, 13, 1, 67]
    lp, ch = LinearProbingTable(11), ChainingTable(11)
    lp_p = [lp.insert(k) for k in keys]
    ch_p = [ch.insert(k) for k in keys]
    assert lp.keys_by_slot() == [22, 1, 46, 13, 67, None, None, None, 41, 53, 30]
    assert sum(lp_p) == 14 and sum(ch_p) == 11


def test_graph():
    assert check_graph(CAMPUS_GRAPH) == 18
    assert dfs(CAMPUS_GRAPH, "Gate") == ["Gate", "Admin", "Lecture1", "Library", "Lab", "Lecture2",
                                         "Sports", "HostelA", "HostelB", "Annex", "Cafeteria"]
    assert bfs(CAMPUS_GRAPH, "Gate") == ["Gate", "Admin", "Library", "HostelA", "Lecture1", "Cafeteria",
                                         "Lab", "Annex", "HostelB", "Sports", "Lecture2"]
    assert dijkstra(CAMPUS_GRAPH, "Gate", "Sports") == (15, ["Gate", "HostelA", "HostelB", "Sports"])
    for a in CAMPUS_GRAPH:
        for b in CAMPUS_GRAPH:
            assert dijkstra(CAMPUS_GRAPH, a, b)[0] == dijkstra_heap(CAMPUS_GRAPH, a, b)[0]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
