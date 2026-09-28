# Algorithm Time Complexity Analyzer

A small Flask app that measures how long an algorithm takes to run as the input size grows, plots the result, and lets you save the run settings to a database using SQLAlchemy.

## Features

- **Analyze** an algorithm's running time across increasing input sizes and get back a plot (base64-encoded PNG) in a JSON response.
- **Save** an analysis (algorithm name, step, max input size) to a SQLite database through SQLAlchemy. No raw SQL is used.
- Includes stack and queue implementations that can be analyzed like any other algorithm.

## Project Structure

| File | Purpose |
|---|---|
| `app.py` | Flask app with the `/analyze` and `/save` routes |
| `algorithms.py` | Algorithm implementations and `time_complexity_visualizer` (timing + plotting) |
| `stk.py` | Stack operations |
| `que.py` | Queue operations |
| `algo_db.py` | SQLAlchemy setup and the `Analysis` model |
| `requirements.txt` | Python dependencies |
| `static/` | Generated plot images |
| `instance/analysis.db` | SQLite database (created automatically on first run) |

## Requirements

- Python 3.10+
- Flask, Flask-SQLAlchemy, matplotlib (see `requirements.txt`)

## Setup

```powershell
# 1. Clone the repository
git clone https://github.com/tinnah13/time_complexity
cd time_complexity

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
pip install flask-sqlalchemy
```

Activated with `source venv/bin/activate` instead.

## Run the App

```powershell
python app.py
```

The server starts at `http://127.0.0.1:5000`. There is no page at `/`; use the endpoints below.

## API Endpoints

### `GET /analyze`

Runs the chosen algorithm over increasing input sizes and returns a plot.

**Query parameters**

| Parameter | Type | Description |
|---|---|---|
| `algo` | string | Name of the algorithm (see list below) |
| `step` | int | Increment between input sizes |
| `n_max` | int | Largest input size |

**Example**

```
http://127.0.0.1:5000/analyze?algo=linear_search&step=10&n_max=200
```

**Response (JSON)**

```json
{
  "algorithm": "linear_search",
  "step": 10,
  "n_max": 200,
  "image": "<base64-encoded PNG>"
}
```

**Available `algo` values**

`linear_search`, `bubble_sort`, `binary_search`, `nested_loop`, `two_pointer`, `unique_users`, `push_algorithm`, `pop_algorithm`, `peep_algorithm`, `isempty_algorithm`, `enqueue_algorithm`, `dequeue_algorithm`, `peek_algorithm`, `queis_empty_algorithm`

> Tip: keep `n_max` small for slow algorithms such as `bubble_sort` and `nested_loop`.

### `POST /save`

Saves an analysis record to the database.

**Request body (JSON)**

```json
{
  "algo": "linear_search",
  "step": 10,
  "n_max": 200
}
```

**Example (PowerShell)**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/save" -Method Post -ContentType "application/json" -Body '{"algo":"linear_search","step":10,"n_max":200}'
```

**Response**

```json
{
  "message": "Analysis saved successfully"
}
```

## Database

Records are stored in SQLite (`instance/analysis.db`) using the `Analysis` model in `algo_db.py`:

| Column | Type |
|---|---|
| `id` | Integer (primary key) |
| `algorithm` | String(100) |
| `step` | Integer |
| `n_max` | Integer |

The table is created automatically when the app starts.

## Notes

- Execution times at small input sizes are very short, so the plots can look jagged. Larger `n_max` values show the trend more clearly.
- The Flask development server is for local use only.
