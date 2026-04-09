import csv
import html
from pathlib import Path


CSV_FILENAME = "demo_responses.csv"
REPORT_FILENAME = "context.html"
# Shareable link when this repo uses GitHub Pages (copy from page source or here).
REPORT_PUBLIC_URL = "https://sofialarson.github.io/hcde530/Week2/context.html"
NOT_AVAILABLE = "Not available"


def safe_get(row, key):
    """Return a safe string value for a CSV field."""
    value = row.get(key, "").strip()
    return value if value else NOT_AVAILABLE


def count_words(response):
    """Count words in a response string."""
    if response == NOT_AVAILABLE:
        return 0
    return len(response.split())


def load_rows(filename):
    """Load rows from a CSV file and handle missing data safely."""
    rows = []
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for raw_row in reader:
            participant = safe_get(raw_row, "participant_id")
            role = safe_get(raw_row, "role")
            response = safe_get(raw_row, "response")
            words = count_words(response)
            preview = response if len(response) <= 60 else response[:60] + "..."
            rows.append(
                {
                    "participant_id": participant,
                    "role": role,
                    "response": response,
                    "preview": preview,
                    "words": words,
                }
            )
    return rows


def summarize(word_counts):
    """Create summary statistics from word counts."""
    if not word_counts:
        return {"total": 0, "shortest": 0, "longest": 0, "average": 0.0}
    return {
        "total": len(word_counts),
        "shortest": min(word_counts),
        "longest": max(word_counts),
        "average": sum(word_counts) / len(word_counts),
    }


def build_insights(summary):
    """Generate plain-language insights for the report."""
    if summary["total"] == 0:
        return ["No responses were found in the data file."]

    insights = []
    insights.append(
        f"There are {summary['total']} total responses in this dataset."
    )
    insights.append(
        "Response length ranges from "
        f"{summary['shortest']} to {summary['longest']} words."
    )
    insights.append(
        f"The average response length is {summary['average']:.1f} words."
    )
    if summary["average"] >= 20:
        insights.append("Overall, responses are moderately detailed.")
    else:
        insights.append("Overall, responses are brief and concise.")
    return insights


def print_terminal_report(rows, summary):
    """Print a clear row-by-row and summary report in the terminal."""
    print(f"{'ID':<12} {'Role':<22} {'Words':<6} {'Response (first 60 chars)'}")
    print("-" * 90)
    for row in rows:
        print(
            f"{row['participant_id']:<12} {row['role']:<22} "
            f"{row['words']:<6} {row['preview']}"
        )

    print()
    print("-- Summary ---------------------------------")
    print(f"  Total responses : {summary['total']}")
    print(f"  Shortest        : {summary['shortest']} words")
    print(f"  Longest         : {summary['longest']} words")
    print(f"  Average         : {summary['average']:.1f} words")


def write_html_report(output_path, rows, summary, insights):
    """Create an HTML report with chart, summary, and insights."""
    max_words = max([row["words"] for row in rows], default=1)
    table_rows_html = []
    chart_rows_html = []

    for row in rows:
        safe_id = html.escape(row["participant_id"])
        safe_role = html.escape(row["role"])
        safe_preview = html.escape(row["preview"])
        width_percent = int((row["words"] / max_words) * 100) if max_words else 0

        table_rows_html.append(
            "<tr>"
            f"<td>{safe_id}</td>"
            f"<td>{safe_role}</td>"
            f"<td>{row['words']}</td>"
            f"<td>{safe_preview}</td>"
            "</tr>"
        )
        chart_rows_html.append(
            "<div class='bar-row'>"
            f"<span class='bar-label'>{safe_id}</span>"
            f"<div class='bar'><div class='bar-fill' style='width:{width_percent}%;'></div></div>"
            f"<span class='bar-value'>{row['words']}</span>"
            "</div>"
        )

    insights_html = "".join([f"<li>{html.escape(item)}</li>" for item in insights])
    html_content = f"""<!DOCTYPE html>
<!-- GitHub Pages — share this report in a browser: {REPORT_PUBLIC_URL} -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 2 Context Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.4; color: #1f1f1f; }}
    h1, h2 {{ margin-bottom: 8px; }}
    .muted {{ color: #555; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 8px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f3f3f3; }}
    .bar-row {{ display: flex; align-items: center; gap: 8px; margin: 8px 0; }}
    .bar-label {{ width: 60px; font-weight: bold; }}
    .bar {{ flex: 1; background: #eee; height: 16px; border-radius: 4px; overflow: hidden; }}
    .bar-fill {{ background: #3b82f6; height: 16px; }}
    .bar-value {{ width: 40px; text-align: right; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 14px; margin: 14px 0; }}
  </style>
</head>
<body>
  <h1>Week 2 Data Processing Report</h1>
  <p class="muted">Generated from <code>{html.escape(CSV_FILENAME)}</code></p>

  <div class="card">
    <h2>Project Goal</h2>
    <p>Demonstrate effective data-file processing and highlight important code outcomes in a clear, beginner-friendly format.</p>
  </div>

  <div class="card">
    <h2>Data Overview</h2>
    <p>Total rows processed: <strong>{summary['total']}</strong></p>
  </div>

  <div class="card">
    <h2>Word Count Chart</h2>
    {"".join(chart_rows_html) if chart_rows_html else "<p>Not available</p>"}
  </div>

  <div class="card">
    <h2>Summary Stats</h2>
    <ul>
      <li>Total responses: {summary['total']}</li>
      <li>Shortest response: {summary['shortest']} words</li>
      <li>Longest response: {summary['longest']} words</li>
      <li>Average response length: {summary['average']:.1f} words</li>
    </ul>
  </div>

  <div class="card">
    <h2>Plain-Language Insights</h2>
    <ul>{insights_html}</ul>
  </div>

  <div class="card">
    <h2>Row-by-Row Results</h2>
    <table>
      <thead>
        <tr>
          <th>Participant ID</th>
          <th>Role</th>
          <th>Word Count</th>
          <th>Response Preview</th>
        </tr>
      </thead>
      <tbody>
        {"".join(table_rows_html) if table_rows_html else "<tr><td colspan='4'>Not available</td></tr>"}
      </tbody>
    </table>
  </div>
</body>
</html>
"""
    output_path.write_text(html_content, encoding="utf-8")


def main():
    """Run analysis and generate terminal + HTML outputs."""
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / CSV_FILENAME
    html_path = base_dir / REPORT_FILENAME

    rows = load_rows(csv_path)
    word_counts = [row["words"] for row in rows]
    summary = summarize(word_counts)
    insights = build_insights(summary)

    print_terminal_report(rows, summary)
    write_html_report(html_path, rows, summary, insights)
    print()
    print(f"HTML report generated: {html_path.name}")


if __name__ == "__main__":
    main()
