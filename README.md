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
- `insertion_sort` 
- `merge_sort` 
- `factorial` 

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
http://localhost:8000/analyze?algo=insertion_sort&step=10&n_max=1000
http://localhost:8000/analyze?algo=merge_sort&step=10&n_max=1000
http://localhost:8000/analyze?algo=factorial&step=100&n_max=10000
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


- `insertion_sort` is O(n²) like bubble sort, so it should show a
  similar upward-curving parabola.
- `merge_sort` is O(n log n), so its curve is noticeably flatter than
  the O(n²) algorithms — a gentle upward bend, not a steep one.
- `factorial` is O(n) (a single loop multiplying up to n), similar in
  shape to `linear_search`. A larger `n_max` (e.g. 10000) makes the
  trend easier to see since each iteration is cheap.

## Notes

- Search algorithms use a target that is never found (worst case), so
  the timing reflects the algorithm's true complexity rather than
  getting lucky on an early match.
- Sort algorithms run on reverse-sorted input (worst case for the
  simple sorts implemented here).