"""Call the Data.gov College Scorecard API using a key from the environment or key.env (one line = key)."""

import csv
import json
import os
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Optional, Tuple

# Base URL for the API to call the API and grab data for the script to analyze.
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
# Key.env: a single line with my Data.gov API key only (see load_key_env_file).
KEY_ENV = "DATA_GOV_API_KEY"
KEY_FILE = Path(__file__).with_name("key.env")

# CSV output next to this script (per assignment name).
OUTPUT_CSV = Path(__file__).with_name(
    "Top 50 Colleges in Washington State by Enrollment Size.csv"
)
CSV_COLUMNS = ("Rank", "ID", "School Name", "City", "State", "Enrollment")

# Request structure: ?api_key=...&{parameters}
# See https://api.data.gov/ed/collegescorecard/v1/schools

# How many of the largest schools (by latest student enrollment) to return.
TOP_N = 50
# API request size cap per call (Scorecard allows up to 100 per page).
CHUNK = 100

# Pulls names of colleges in Washington state from the API, along with the 
# city and enrollment size; sorted by enrollment largest first. 
# These parameters can help the script to identify the top colleges in
# Washington state by enrollment size, which could be useful for the state to know
# how to best allocate resources to the colleges.
BASE_PARAMS = {
    "school.state": "WA",
    "fields": "id,school.name,school.state,school.city,latest.student.size",
    "keys_nested": "true",
    "sort": "latest.student.size:desc",
}

# Loads the API key from the key.env file. If the file is not found, it returns None.
# API Key is needed to access the API and therefore, the college data.
def load_key_env_file() -> None:
    if os.environ.get(KEY_ENV):
        return
    if not KEY_FILE.is_file():
        return
    for raw in KEY_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        os.environ[KEY_ENV] = line
        break

# Builds the URL for the API request using the base URL, parameters, and API key.
# This URL is used to fetch the data about colleges in the US from the API for the
# script to analyze.
def build_url(extra_params: Optional[dict] = None) -> str:
    load_key_env_file()
    api_key = os.environ.get(KEY_ENV)
    # If the API key is not found, it raises a SystemExit error with a message for
    # troubleshoting.
    if not api_key:
        extra = ""
        if KEY_FILE.is_file() and KEY_FILE.stat().st_size == 0:
            extra = f" {KEY_FILE.name} is empty; paste your key into that file (or set {KEY_ENV})."
        raise SystemExit(
            f"Missing API key. Set {KEY_ENV} in the environment, or put your key on one line in "
            f"{KEY_FILE.name} (no variable name, key only).{extra}"
        )
    query: dict = {"api_key": api_key}
    # If extra parameters are provided, they are added to the query. This allows for
    # more flexibility in the API request.
    if extra_params:
        query.update(extra_params)
    return f"{BASE_URL}?{urllib.parse.urlencode(query)}"

# Reads a field from a result row from the API. The API may return either:
# - flat keys: "school.name", "latest.student.size", or
# - nested objects when keys_nested=true: school -> name, latest -> student -> size
# Flat keys and nested objects are both supported because the API returns both.
def field(row: dict, dotted: str) -> Any:
    # If the field is found in the row, it returns the value.
    if dotted in row:
        return row[dotted]
    # If the field is not found in the row, it splits the dotted string into parts and
    # checks if the parts are in the row. If they are, it returns the value.
    cur: Any = row
    # If the field is not found in the row, it returns None.
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur

# Pulls the top determined number of Washington schools (50)
# by latest.student.size (largest first) from the API.
def fetch_largest_wa_schools() -> Tuple[list, Optional[dict[str, Any]]]:
    """Largest schools in Washington by enrollment; each row includes school.city."""
    page = 0
    out: list = []
    first_meta: Optional[dict] = None
    # Loops through the pages until the last page is reached.
    while len(out) < TOP_N:
        # Calculates the number of schools needed to reach the top determined 
        # number of schools (50).
        need = TOP_N - len(out)
        per_page = min(CHUNK, need, 100)
        # Builds the URL for the API request using the base URL, parameters, and API key.
        url = build_url(
            extra_params={**BASE_PARAMS, "page": page, "per_page": per_page},
        )
        # Sends the API request to the URL.
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json"},
        )
        # Tries to open the URL and load the data from the API.
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise SystemExit(
                f"API error {e.code} for request (check fields/filters). Body: {err_body[:2000]}"
            ) from e
        if first_meta is None:
            first_meta = data.get("metadata")
        batch = data.get("results") or []
        out.extend(batch)
        # If the batch is empty or the number of schools in the batch is less than
        # the number of schools needed to reach the top determined number of schools (50),
        # it breaks the loop.
        if not batch or len(batch) < per_page:
            break
        page += 1
    return out[:TOP_N], first_meta


def build_output_rows(results: list) -> list[dict]:
    """Format API rows for printing and CSV (same values)."""
    rows: list[dict] = []
    for i, row in enumerate(results, start=1):
        name = field(row, "school.name")
        city = field(row, "school.city")
        st = field(row, "school.state")
        n = field(row, "latest.student.size")
        sid = field(row, "id")
        if name is None or name == "":
            name = f"(name missing in API) [id={sid}]"
        rows.append(
            {
                "Rank": i,
                "ID": sid if sid is not None else "",
                "School Name": name,
                "City": city if city is not None and city != "" else "",
                "State": st if st is not None and st != "" else "",
                "Enrollment": n if n is not None else "",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        w.writerows(rows)


# Calls the API and prints the request and the results in a readable format.
def main() -> None:
    sample = {**BASE_PARAMS, "page": 0, "per_page": min(100, TOP_N)}
    query_pairs = [("api_key", "<YOUR_API_KEY>")]
    query_pairs.extend((k, str(v)) for k, v in sample.items())
    print("Request (replace <YOUR_API_KEY> with your key) — first page, sorted by size desc:")
    print(f"{BASE_URL}?{urllib.parse.urlencode(query_pairs)}")
    print(f"(TOP_N = {TOP_N} largest in WA by latest student size)")
    print()
    # Pulls the top determined number of Washington schools (50)
    # by latest.student.size (largest first) from the API.
    results, first_meta = fetch_largest_wa_schools()
    # Gets the total number of schools in the API.
    total_reported = (first_meta or {}).get("total")
    # Prints the header with the total number of schools in the API.
    header = f"Top {len(results)} largest college(s) in Washington (by enrollment)"
    if total_reported is not None:
        header += f" — {total_reported} Washington school(s) in API"
    print(header)
    output_rows = build_output_rows(results)
    for r in output_rows:
        name = r["School Name"]
        city = r["City"] or "—"
        st = r["State"] or "—"
        n = r["Enrollment"]
        n_disp = n if n != "" else "—"
        i = r["Rank"]
        print(f"  {i:2d}. {name} | City: {city} | State: {st} | Students: {n_disp}")

    write_csv(OUTPUT_CSV, output_rows)
    print()
    print(f"Wrote CSV: {OUTPUT_CSV} ({len(output_rows)} rows)")

# Main function to run the program.
if __name__ == "__main__":
    main()
