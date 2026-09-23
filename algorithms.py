"""
Algorithms to be timed by the visualizer.
Each function takes a single integer n (input size) and does work
proportional to that size, using a worst-case input where relevant
so the measured time reflects the algorithm's real complexity.
"""
from data_structures import Stack, Queue
from stack import (
    push_algorithm,
    pop_algorithm,
    peep_algorithm,
    isempty_algorithm,
)
from queue_ops import (
    enqueue_algorithm,
    dequeue_algorithm,
    peek_algorithm,
    queis_empty_algorithm,
)


def linear_search(n):
    arr = list(range(n))
    target = -1  # guarantees a full worst-case scan
    for x in arr:
        if x == target:
            return True
    return False


def binary_search(n):
    arr = list(range(n))
    target = -1  # guarantees the search runs to completion (not found)
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False


def bubble_sort(n):
    arr = list(range(n, 0, -1))  # reverse-sorted = worst case for bubble sort
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def nested_loops(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total


# --- Bonus algorithms (extra credit per the activity) ---

def insertion_sort(n):
    arr = list(range(n, 0, -1))  # reverse-sorted = worst case
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(n):
    arr = list(range(n, 0, -1))

    def _merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _merge_sort(a[:mid])
        right = _merge_sort(a[mid:])
        return _merge(left, right)

    def _merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    return _merge_sort(arr)


def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def deduplicate_users(n):
    """
    Naive nested-loop deduplication by id (no set/dict lookup) — the
    kind of code that often shows up in real API endpoints. Demonstrates
    O(n^2) behavior since every user is checked against every
    already-kept unique user.
    """
    users = [{"id": i, "name": f"user{i}"} for i in range(n)]
    unique_users = []
    for i in range(len(users)):
        seen = False
        for j in range(len(unique_users)):
            if users[i]["id"] == unique_users[j]["id"]:
                seen = True
                break
        if not seen:
            unique_users.append(users[i])
    return unique_users


# --- Stack/Queue-backed algorithms (Home Activity) ---

def stack_balanced_parentheses(n):
    """
    Builds a balanced expression of n '(' followed by n ')' and checks
    it's balanced using a Stack. O(n) — each character is pushed or
    popped at most once.
    """
    expression = "(" * n + ")" * n
    stack = Stack()
    balanced = True
    for char in expression:
        if char == "(":
            stack.push(char)
        else:
            if stack.is_empty():
                balanced = False
                break
            stack.pop()
    return balanced and stack.is_empty()


def stack_reverse(n):
    """
    Reverses a list of n elements using a Stack (push everything, then
    pop everything). O(n).
    """
    stack = Stack()
    for item in range(n):
        stack.push(item)
    reversed_items = []
    while not stack.is_empty():
        reversed_items.append(stack.pop())
    return reversed_items


def queue_bfs_chain(n):
    """
    Builds a simple chain graph 0 -> 1 -> 2 -> ... -> n-1 and performs
    a breadth-first traversal using a Queue. O(n) since each node is
    enqueued and dequeued exactly once.
    """
    if n <= 0:
        return []

    graph = {i: [i + 1] for i in range(n - 1)}
    graph[n - 1] = []

    visited = {0}
    order = []
    queue = Queue()
    queue.enqueue(0)

    while not queue.is_empty():
        node = queue.dequeue()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

    return order


# --- Individual stack operation timing ---
# push/pop_algorithm/peep_algorithm/isempty_algorithm come from stack.py.
# Isolates each op (push/pop/peek/is_empty) so its own O(1)-per-call
# behavior is visible: doing n of them should plot as a straight O(n) line.
stack_push = push_algorithm
stack_pop = pop_algorithm
stack_peek = peep_algorithm
stack_is_empty = isempty_algorithm


# --- Individual queue operation timing ---
# enqueue/dequeue/peek/queis_empty_algorithm come from queue_ops.py.
# Note: dequeue() there uses list.pop(0), which is O(n) per call (it has
# to shift every remaining element), unlike Stack's pop() from the end.
# So n dequeues is O(n^2) total, not O(n) — the graph should show a
# quadratic curve, not a straight line, unlike stack_pop above.
queue_enqueue = enqueue_algorithm
queue_dequeue = dequeue_algorithm
queue_peek = peek_algorithm
queue_is_empty = queis_empty_algorithm


ALGORITHMS = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "nested_loops": nested_loops,
    "insertion_sort": insertion_sort,
    "merge_sort": merge_sort,
    "factorial": factorial,
    "deduplicate_users": deduplicate_users,
    "stack_balanced_parentheses": stack_balanced_parentheses,
    "stack_reverse": stack_reverse,
    "queue_bfs_chain": queue_bfs_chain,
    "stack_push": stack_push,
    "stack_pop": stack_pop,
    "stack_peek": stack_peek,
    "stack_is_empty": stack_is_empty,
    "queue_enqueue": queue_enqueue,
    "queue_dequeue": queue_dequeue,
    "queue_peek": queue_peek,
    "queue_is_empty": queue_is_empty,
}
