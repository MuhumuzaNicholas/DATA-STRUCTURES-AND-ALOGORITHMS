# BCS 2105 Coursework - Campus Navigation and Resource Management System

Group: Muhumuza Nichola, Adupa Jackson, Isingoma Joseph, Tibesigwa Lorrine
Repository link: (add your Git repository URL here)

## Requirements
Python 3.8 or newer. No third-party packages are needed (see `requirements.txt`).
Every data structure (stack, queue, linked lists, BST, heap, hash tables, graph) is implemented
from scratch; `heapq`, `collections` and `networkx` are NOT used.

## Files
| File | Task | What it shows |
|---|---|---|
| `task1_analysis.py` | 1 | Nested-loop operation count, dynamic array amortised cost, search timing |
| `task2_stack_queue.py` | 2 | Stack, queue, circular queue, infix-to-postfix trace |
| `task3_linked_lists.py` | 3 | Singly/doubly/circular linked lists, Floyd cycle detection |
| `task4_trees_heaps.py` | 4 | BST (traversals, deletion), min-heap, heap sort trace |
| `task5_sort_search_hash.py` | 5 | Insertion/merge/quick sort, binary search, linear probing, chaining, double hashing |
| `main.py` | 6 | Integrated system: graph, DFS, BFS, Dijkstra, menu |
| `tests.py` | all | Automatic checks of the key results in the report |

## How to run
```
python task1_analysis.py          # repeat for task2 ... task5 (each prints its own demo)
python main.py                    # interactive menu
python main.py --demo             # scripted demonstration (sample output in the report)
python tests.py                   # self-checks, prints PASS for each group
```
Building names for routes: Gate, Admin, Library, HostelA, Lecture1, Cafeteria, Lab, Lecture2, HostelB, Sports, Annex.
Sample room codes: LIB101, LIB205, ADM001, ADM014, LEC101, LEC201, LAB301, CAF001, SPT010, ANX102.
