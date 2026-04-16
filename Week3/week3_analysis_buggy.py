import csv


def load_rows(filename: str) -> list[dict[str, str]]:
    """Load survey rows from a CSV file into a list of dictionaries."""
    rows = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def main() -> None:
    """Analyze survey data by role, experience, and satisfaction scores."""
    # Load the survey data from a CSV file
    filename = "week3_survey_messy.csv"
    rows = load_rows(filename)

    # Count responses by role
    # Normalize role names so "ux researcher" and "UX Researcher" are counted together
    role_counts = {}

    for row in rows:
        role = row["role"].strip().title()
        if role in role_counts:
            role_counts[role] += 1
        else:
            role_counts[role] = 1

    print("Responses by role:")
    for role, count in sorted(role_counts.items()):
        print(f"  {role}: {count}")

    # Calculate the average years of experience
    total_experience = 0
    valid_experience_count = 0
    for row in rows:
        experience_text = row["experience_years"].strip()
        if experience_text.isdigit():
            total_experience += int(experience_text)
            valid_experience_count += 1

    avg_experience = total_experience / valid_experience_count if valid_experience_count else 0
    print(f"\nAverage years of experience: {avg_experience:.1f}")

    # Find the top 5 highest satisfaction scores
    scored_rows = []
    for row in rows:
        if row["satisfaction_score"].strip():
            scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

    scored_rows.sort(key=lambda x: x[1], reverse=True)
    top5 = scored_rows[:5]

    print("\nTop 5 satisfaction scores:")
    for name, score in top5:
        print(f"  {name}: {score}")


if __name__ == "__main__":
    main()
