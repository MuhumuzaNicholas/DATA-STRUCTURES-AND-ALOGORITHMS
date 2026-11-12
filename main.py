"""Task 6 - Campus Navigation and Resource Management System (integrated prototype).

Run:  python main.py          interactive menu
      python main.py --demo   scripted demonstration (used for the sample output in the report)
"""
import sys

from task2_stack_queue import Stack, Queue
from task3_linked_lists import SinglyLinkedList
from task4_trees_heaps import BST, MinHeap
from task5_sort_search_hash import ChainingTable

INF = float("inf")

# ---------------------------------------------------------------------------
# 6(a) Weighted undirected graph: adjacency list (edge weight = walking minutes)
# ---------------------------------------------------------------------------
CAMPUS_GRAPH = {
    "Gate":      {"Admin": 4, "Library": 6, "HostelA": 8},
    "Admin":     {"Gate": 4, "Lecture1": 5, "Cafeteria": 7},
    "Library":   {"Gate": 6, "Lecture1": 3, "Lab": 4, "Annex": 5},
    "HostelA":   {"Gate": 8, "HostelB": 3, "Sports": 9},
    "Lecture1":  {"Admin": 5, "Library": 3, "Lecture2": 2, "Cafeteria": 4},
    "Cafeteria": {"Admin": 7, "Lecture1": 4, "Sports": 6},
    "Lab":       {"Library": 4, "Lecture2": 5, "Annex": 3},
    "Lecture2":  {"Lecture1": 2, "Lab": 5, "Sports": 5},
    "HostelB":   {"HostelA": 3, "Sports": 4, "Annex": 8},
    "Sports":    {"HostelA": 9, "Cafeteria": 6, "Lecture2": 5, "HostelB": 4},
    "Annex":     {"Library": 5, "Lab": 3, "HostelB": 8},
}


def check_graph(graph):
    """Every edge must appear in both directions with the same weight."""
    for u, nbrs in graph.items():
        for v, w in nbrs.items():
            assert graph[v].get(u) == w, f"edge {u}-{v} is not symmetric"
    return sum(len(n) for n in graph.values()) // 2


def adjacency_matrix(graph):
    names = list(graph)
    return names, [[graph[u].get(v, 0) for v in names] for u in names]


# ---------------------------------------------------------------------------
# 6(b) DFS, BFS, Dijkstra
# ---------------------------------------------------------------------------
def dfs(graph, start):
    visited, order = set(), []

    def visit(u):
        visited.add(u)
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visit(v)

    visit(start)
    return order


def bfs(graph, start):
    visited, order = {start}, []
    q = Queue()
    q.enqueue(start)
    while not q.is_empty():
        u = q.dequeue()
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                q.enqueue(v)
    return order


def dijkstra(graph, source, target):
    """Array-scan version, O(V^2). Returns (total_minutes, path) or (INF, [])."""
    dist = {v: INF for v in graph}
    prev, done = {}, set()
    dist[source] = 0
    while True:
        u, best = None, INF
        for v in graph:                          # pick the closest unfinished vertex
            if v not in done and dist[v] < best:
                u, best = v, dist[v]
        if u is None:
            break
        done.add(u)
        if u == target:
            break
        for v, w in graph[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
    if dist[target] == INF:
        return INF, []
    path, cur = [target], target
    while cur != source:
        cur = prev[cur]
        path.append(cur)
    return dist[target], list(reversed(path))


def dijkstra_heap(graph, source, target):
    """Priority-queue version using our own MinHeap: O((V+E) log V)."""
    dist = {v: INF for v in graph}
    prev = {}
    dist[source] = 0
    heap = MinHeap()
    heap.push((0, source))
    while len(heap):
        d, u = heap.pop()
        if d > dist[u]:
            continue
        if u == target:
            break
        for v, w in graph[u].items():
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heap.push((dist[v], v))
    if dist[target] == INF:
        return INF, []
    path, cur = [target], target
    while cur != source:
        cur = prev[cur]
        path.append(cur)
    return dist[target], list(reversed(path))


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
FOOTFALL = [("Gate", 4200), ("Cafeteria", 3100), ("Library", 2400), ("HostelA", 2700),
            ("Lecture1", 1800), ("Admin", 1500), ("Sports", 950), ("Annex", 700)]

ROOMS = [  # (room code, description, building)
    ("LIB101", "Library reading room", "Library"),
    ("LIB205", "Library computer lab", "Library"),
    ("ADM001", "Registrar's office", "Admin"),
    ("ADM014", "Dean of Students", "Admin"),
    ("LEC101", "Lecture Theatre 1", "Lecture1"),
    ("LEC201", "Lecture Theatre 2", "Lecture2"),
    ("LAB301", "Networks laboratory", "Lab"),
    ("CAF001", "Main cafeteria hall", "Cafeteria"),
    ("SPT010", "Indoor sports hall", "Sports"),
    ("ANX102", "Library annex study room", "Annex"),
]


class CampusSystem:
    def __init__(self):
        self.graph = CAMPUS_GRAPH
        self.history = Stack(limit=10)                   # navigation history
        self.shuttle = Queue()                           # shuttle requests at the main gate
        for s in ("Gate", "HostelA", "HostelB", "Town Centre"):
            self.shuttle.enqueue(s)
        self.route_stops = SinglyLinkedList()            # ordered shuttle stops
        for s in ("Main Gate", "Hostel A", "Hostel B", "Town Centre"):
            self.route_stops.insert_tail(s)
        self.room_bst = BST()                            # room lookup (ordered)
        self.room_hash = ChainingTable(size=11)          # room lookup (fast exact match)
        for code, desc, building in ROOMS:
            record = f"{desc} ({building})"
            self.room_bst.insert(code, record)
            self.room_hash.insert(code, record)
        self.busiest = MinHeap()                         # keeps the 8 busiest locations
        for name, f in FOOTFALL:
            self.busiest.push_top_k((f, name), 8)

    # -- operations -------------------------------------------------------
    def route(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None
        minutes, path = dijkstra(self.graph, start, end)
        if self.history.is_empty() or self.history.peek() != start:
            self.history.push(start)
        if start != end:
            self.history.push(end)
        return minutes, path

    def lookup_bst(self, code):
        return self.room_bst.search(code.strip().upper())

    def lookup_hash(self, code):
        return self.room_hash.search(code.strip().upper())

    def top_busiest(self, n=3):
        return self.busiest.top_n(n)


# ---------------------------------------------------------------------------
# User interface
# ---------------------------------------------------------------------------
MENU = """
CAMPUS NAVIGATION AND RESOURCE MANAGEMENT SYSTEM
1. Find shortest route
2. Search room using BST
3. Search room using hash table
4. Show top three busiest locations
5. Show navigation history and shuttle queue
6. Show DFS and BFS traversals from the main gate
7. Add a shuttle request
8. Dispatch next shuttle
9. Go back (undo last location in history)
0. Exit"""


def show_route(system, a, b):
    result = system.route(a, b)
    if result is None:
        print(f"Unknown building. Choose from: {', '.join(system.graph)}")
        return
    minutes, path = result
    print(f"Route: {' -> '.join(path)} | Walking time: {minutes} minutes")


def show_lookup(label, found, steps, unit):
    if found is None:
        print(f"{label}: room not found ({unit}: {steps})")
    else:
        print(f"{label}: found: {found} ({unit}: {steps})")


def run_choice(system, choice, ask):
    if choice == "1":
        a = ask("From building: ").strip()
        b = ask("To building: ").strip()
        show_route(system, a, b)
    elif choice == "2":
        code = ask("Room code (e.g. LIB101): ")
        found, steps = system.lookup_bst(code)
        show_lookup("BST", found, steps, "comparisons")
    elif choice == "3":
        code = ask("Room code (e.g. LIB101): ")
        found, probes = system.lookup_hash(code)
        show_lookup("Hash table", found, probes, "probes")
    elif choice == "4":
        print("Top three busiest:", [(f, n) for f, n in system.top_busiest(3)])
    elif choice == "5":
        print("History (latest first):", system.history.latest_first())
        print("Shuttle queue (front first):", system.shuttle.to_list())
        print("Shuttle route stops:", system.route_stops.traverse())
    elif choice == "6":
        print("DFS:", ", ".join(dfs(system.graph, "Gate")))
        print("BFS:", ", ".join(bfs(system.graph, "Gate")))
    elif choice == "7":
        stop = ask("Stop to add to the shuttle queue: ").strip()
        if stop:
            system.shuttle.enqueue(stop)
            print("Queue now:", system.shuttle.to_list())
    elif choice == "8":
        if system.shuttle.is_empty():
            print("No shuttle requests waiting.")
        else:
            print("Dispatching shuttle to:", system.shuttle.dequeue())
    elif choice == "9":
        if system.history.is_empty():
            print("History is empty.")
        else:
            print("Removed:", system.history.pop(), "| now at:",
                  system.history.peek() if not system.history.is_empty() else "(nowhere)")
    else:
        print("Invalid choice, please enter a number from the menu.")


def demo():
    system = CampusSystem()
    edges = check_graph(CAMPUS_GRAPH)
    print(f"Graph check passed: {len(CAMPUS_GRAPH)} buildings, {edges} pathways.")
    print(MENU)
    script = [
        ("1", ["Gate", "Sports"]),
        ("1", ["Library", "Cafeteria"]),
        ("1", ["Gate", "Mars"]),
        ("2", ["LAB301"]),
        ("3", ["LAB301"]),
        ("3", ["XYZ999"]),
        ("4", []),
        ("5", []),
        ("6", []),
    ]
    for choice, answers in script:
        print(f"\n>>> Choice {choice} {answers if answers else ''}")
        feed = iter(answers)
        run_choice(system, choice, lambda prompt: next(feed))


def main():
    if "--demo" in sys.argv:
        demo()
        return
    system = CampusSystem()
    check_graph(CAMPUS_GRAPH)
    while True:
        print(MENU)
        choice = input("Choice: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        run_choice(system, choice, input)


if __name__ == "__main__":
    main()
