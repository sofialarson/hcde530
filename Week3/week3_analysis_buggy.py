import csv

#  Loads the rows from the CSV file into a list of dictionaries that will be used for
# the analysis.
def load_rows(filename: str) -> list[dict[str, str]]:
    """Load survey rows from a CSV file into a list of dictionaries."""
    rows = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

# Creates a list of products mentioned in the survey responses.
def create_list_of_products_mentioned_in_survey(rows: list[dict[str, str]]) -> list[str]:
    """Create list of products mentioned in survey responses.

    This function reads each row's `primary_tool`, trims extra whitespace,
    normalizes product names to title case, removes blanks, and returns a
    sorted unique list of product names.
    """
    #Extracts the product from the row and adds it to the set of products.
    products = set()
    for row in rows:
        product_name = (row.get("primary_tool") or "").strip().title()
        if product_name:
            products.add(product_name)
    return sorted(products)

# Main function that analyzes the survey data by role, experience, and 
#satisfaction scores.
def main() -> None:
    """Analyze survey data by role, experience, and satisfaction scores."""
    # Load the survey data from a CSV file
    filename = "week3_survey_messy.csv"
    rows = load_rows(filename)

    # Count responses by role
    # Normalize role names so "ux researcher" and "UX Researcher" are counted together
    role_counts = {}

# Counts the number of responses by role.
    for row in rows:
        role = row["role"].strip().title()
        if role in role_counts:
            role_counts[role] += 1
            # If the role is not in the dictionary, add it with a count of 1.
        else:
            role_counts[role] = 1

# Prints the number of responses by role for the output.
    print("Responses by role:")
    for role, count in sorted(role_counts.items()):
        print(f"  {role}: {count}")

    # Calculate the average years of experience
    total_experience = 0
    valid_experience_count = 0
    # Extracts the experience from the row and adds it to the total experience.
    for row in rows:
        experience_text = row["experience_years"].strip()
        if experience_text.isdigit():
            total_experience += int(experience_text)
            valid_experience_count += 1

# Calculates the average years of experience and prints it to the output.
    avg_experience = total_experience / valid_experience_count if valid_experience_count else 0
    print(f"\nAverage years of experience: {avg_experience:.1f}")

    # Find the top 5 highest satisfaction scores
    scored_rows = []
    for row in rows:
        if row["satisfaction_score"].strip():
            scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))
# Sorts the scored rows by satisfaction score in descending order.
    scored_rows.sort(key=lambda x: x[1], reverse=True)
    top5 = scored_rows[:5]
# Prints the top 5 satisfaction scores to the output.
    print("\nTop 5 satisfaction scores:")
    for name, score in top5:
        print(f"  {name}: {score}")

# Creates a list of products mentioned in the survey responses.
    unique_products = create_list_of_products_mentioned_in_survey(rows)
    print("\nProducts that received insights:")
    for product in unique_products:
        print(f"  {product}")

# Writes the cleaned data to a CSV file.
    output_filename = "Week3_survey_cleaned data.csv"
    with open(output_filename, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["section", "label", "value"])
        writer.writeheader()
        # Writes the number of responses by role to the CSV file.
        for role, count in sorted(role_counts.items()):
            writer.writerow(
                {
                    "section": "Responses by role",
                    "label": role if role else "Unknown",
                    "value": count,
                }
            )
        # Writes the average years of experience to the CSV file.
        writer.writerow(
            {
                "section": "Average years of experience",
                "label": "avg_experience",
                "value": f"{avg_experience:.1f}",
            }
        )
        # Writes the top 5 satisfaction scores to the CSV file.
        for name, score in top5:
            writer.writerow({"section": "Top 5 satisfaction scores", "label": name, "value": score})
        # Writes the products that received insights to the CSV file.
        for product in unique_products:
            writer.writerow({"section": "Products that received insights", "label": product, "value": ""})
    print(f"\nCleaned product insight data written to {output_filename}")

# Main function that runs the analysis.
if __name__ == "__main__":
    main()
