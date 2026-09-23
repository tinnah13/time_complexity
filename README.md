# Time Complexity Visualizer API

A Flask server that times an algorithm across a range of input sizes,
plots running time vs. input size, and returns the data plus a
base64-encoded PNG of the plot.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

The server runs at `http://localhost:8000`.

## Endpoint

```
GET /analyze?algo=<name>&step=<int>&n_max=<int>
```

- `algo` — one of the supported algorithm names (see below). `n_min` is
  always 0.
- `step` — increment between input sizes.
- `n_max` — largest input size to test.

Example:

```
http://localhost:8000/analyze?algo=linear_search&step=10&n_max=1000
```

### Supported algorithms

- `linear_search`
- `binary_search`
- `bubble_sort`
- `nested_loops`
- `insertion_sort` (bonus)
- `merge_sort` (bonus)
- `factorial` (bonus)
- `deduplicate_users` (bonus)

### Response

```json
{
  "algorithm": "linear_search",
  "n_min": 0,
  "n_max": 1000,
  "step": 10,
  "input_sizes": [1, 10, 20, ...],
  "times_seconds": [0.000002, 0.000004, ...],
  "image_path": "/absolute/path/to/static/linear_search_plot.png",
  "image_base64": "iVBORw0KG..."
}
```

The plot PNG is also saved locally under `static/`.

## Testing each algorithm and viewing the graphs

With the server running (`python app.py`), open each of these in your
browser one at a time:

```
http://localhost:8000/analyze?algo=linear_search&step=10&n_max=1000
http://localhost:8000/analyze?algo=binary_search&step=10&n_max=1000
http://localhost:8000/analyze?algo=bubble_sort&step=10&n_max=1000
http://localhost:8000/analyze?algo=nested_loops&step=10&n_max=1000
```

Each request returns a JSON blob in the browser (that's expected — it's
an API response, not a page) and creates/overwrites a PNG in `static/`,
e.g. `static/bubble_sort_plot.png`. Open that file in your editor or
image viewer to see the actual plot.

`bubble_sort` and `nested_loops` are O(n²), so their curve bends
upward more noticeably at larger input sizes — try `n_max=5000` or
`n_max=10000` for those two if you want to see the quadratic shape
more clearly. `linear_search` and `binary_search` stay comparatively
flat and can show minor timing noise (small spikes) at microsecond
scale — that's normal system jitter, not a bug.

### Testing the bonus algorithms

```
http://localhost:8000/analyze?algo=insertion_sort&step=10&n_max=1000
http://localhost:8000/analyze?algo=merge_sort&step=10&n_max=1000
http://localhost:8000/analyze?algo=factorial&step=100&n_max=10000
```

- `insertion_sort` is O(n²) like bubble sort, so it should show a
  similar upward-curving parabola.
- `merge_sort` is O(n log n), so its curve is noticeably flatter than
  the O(n²) algorithms — a gentle upward bend, not a steep one.
- `factorial` is O(n) (a single loop multiplying up to n), similar in
  shape to `linear_search`. A larger `n_max` (e.g. 10000) makes the
  trend easier to see since each iteration is cheap.
- `deduplicate_users` (bonus) — a naive nested-loop dedup-by-id check
  (no set/dict lookup), the kind of code that shows up in real API
  endpoints. O(n²), same shape as `bubble_sort`.

## Live view

For a live-updating chart while the algorithm runs (instead of
waiting for the full JSON response), open:

```
http://localhost:8000/live
```

Pick an algorithm, step, and n_max in the form and click Run. This
streams each timed data point to the browser via Server-Sent Events
(`GET /analyze/stream?algo=<name>&step=<int>&n_max=<int>`) and draws
the chart point-by-point as it computes, finishing with the same
saved PNG as `/analyze`.

## Notes

- Search algorithms use a target that is never found (worst case), so
  the timing reflects the algorithm's true complexity rather than
  getting lucky on an early match.
- Sort algorithms run on reverse-sorted input (worst case for the
  simple sorts implemented here).

## Stack & Queue (Home Activity)

`data_structures.py` implements:

- **`Stack`** — LIFO, backed by a Python list. `push`, `pop`, `peek`,
  `is_empty`, `size`. `pop`/`peek` on an empty stack raise
  `IndexError`.
- **`Queue`** — FIFO, backed by `collections.deque` for O(1)
  `enqueue`/`dequeue`. Same interface as `Stack` (`enqueue`/`dequeue`
  instead of `push`/`pop`).

There's also a second, simpler implementation used only by the
operation-timing algorithms below:

- **`stack.py`** — a module-level list plus free functions
  (`push`/`pop`/`peep`/`is_empty`).
- **`queue_ops.py`** — same idea for a queue
  (`enqueue`/`dequeue`/`peek`/`queis_empty`). Named `queue_ops.py`
  rather than `queue.py` to avoid shadowing Python's built-in `queue`
  standard library module.

### Running the tests

```bash
pip install -r requirements.txt
pytest test_stack.py test_queue.py -v
```

Each suite covers: empty-state behavior, size tracking, ordering
(LIFO for Stack, FIFO for Queue), peek not mutating the structure,
and `IndexError` on popping/dequeuing/peeking an empty structure.

### Testing Stack/Queue algorithms with the visualizer

Three algorithms built on `Stack`/`Queue` are registered in
`algorithms.py` and work through the same `/analyze` and `/live`
endpoints as everything else:

```
http://localhost:8000/analyze?algo=stack_balanced_parentheses&step=200&n_max=5000
http://localhost:8000/analyze?algo=stack_reverse&step=200&n_max=5000
http://localhost:8000/analyze?algo=queue_bfs_chain&step=200&n_max=5000
```

- `stack_balanced_parentheses` — builds a balanced `(((...)))`
  expression of length `2n` and checks it with a `Stack`. O(n).
- `stack_reverse` — pushes `n` items onto a `Stack` then pops them
  all off, reversing order. O(n).
- `queue_bfs_chain` — builds a simple `0 → 1 → 2 → ... → n-1` chain
  graph and does a breadth-first traversal with a `Queue`. O(n).

All three should plot as straight lines (O(n)), same shape as
`linear_search` and `factorial`.

### Testing individual stack operations

Four more algorithms isolate each core `Stack` operation on its own
(a plain list, not the `Stack` class), so you can see that each
operation is O(1) — doing `n` of them plots as a straight O(n) line:

```
http://localhost:8000/analyze?algo=stack_push&step=500&n_max=5000
http://localhost:8000/analyze?algo=stack_pop&step=500&n_max=5000
http://localhost:8000/analyze?algo=stack_peek&step=500&n_max=5000
http://localhost:8000/analyze?algo=stack_is_empty&step=500&n_max=5000
```

- `stack_push` — pushes n items.
- `stack_pop` — pushes n items, then pops them all.
- `stack_peek` — pushes n items, then peeks n times.
- `stack_is_empty` — checks `is_empty()` n times on an empty stack.

### Testing individual queue operations — and a Big-O trap

Four more algorithms mirror the stack ones above, but for a
**plain-list-based queue** (not the `deque`-backed `Queue` class):

```
http://localhost:8000/analyze?algo=queue_enqueue&step=2000&n_max=20000
http://localhost:8000/analyze?algo=queue_dequeue&step=2000&n_max=20000
http://localhost:8000/analyze?algo=queue_peek&step=2000&n_max=20000
http://localhost:8000/analyze?algo=queue_is_empty&step=2000&n_max=20000
```

**Important:** `queue_dequeue` uses `list.pop(0)`, which has to shift
every remaining element left — O(n) per call, not O(1). So doing n
dequeues is **O(n²)**, not O(n). At small `n_max` this is hidden by
system noise; at `n_max=20000` it shows a clear quadratic curve, in
contrast to `queue_enqueue`/`queue_peek`/`queue_is_empty`, which stay
O(n) (`list.append`, `list[0]`, and `len()` are all O(1)). This is
exactly why `Queue` in `data_structures.py` uses `collections.deque`
instead of a plain list — `deque` makes `popleft()` O(1).
