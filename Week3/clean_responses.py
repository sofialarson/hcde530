import csv


INPUT_FILE = "responses.csv"
OUTPUT_FILE = "responses_cleaned.csv"


def clean_csv(input_path: str, output_path: str) -> None:
    """Read survey CSV data, drop rows with empty names, and uppercase role values.

    Args:
        input_path: Path to the source CSV file.
        output_path: Path where cleaned CSV data will be written.
    """
    with open(input_path, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        if not reader.fieldnames:
            raise ValueError("Input CSV has no header row.")

        fieldnames = reader.fieldnames
        cleaned_rows = []

        for row in reader:
            name_value = (row.get("name") or "").strip()
            if not name_value:
                continue

            row["role"] = (row.get("role") or "").upper()
            cleaned_rows.append(row)

    with open(output_path, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)


if __name__ == "__main__":
    clean_csv(INPUT_FILE, OUTPUT_FILE)
    print(f"Cleaned data written to {OUTPUT_FILE}")
