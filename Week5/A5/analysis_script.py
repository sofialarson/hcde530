import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")

DATA_DIR = Path(__file__).resolve().parent

# Cleans up the censsus data by converting the data to numeric columns to 
# uniformly format the data for analysis.
def load_clean_census_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df.shape[1] < 3:
        # Raises an error if the data does not have at least 3 columns.
        raise ValueError(f"Expected at least 3 columns in {path}, got {df.shape[1]}")

    # Renames the columns to make them more readable.
    df = df.rename(
        # label = category, estimate = value, moe = margin of error
        columns={
            df.columns[0]: "label",
            df.columns[1]: "estimate",
            df.columns[2]: "moe",
        }
    )

    # Removes the non-breaking space and strips the whitespace from the label column.
    df["label"] = (
        df["label"]
        .astype(str)
        .str.replace("\u00a0", " ", regex=False)
        .str.strip()
    )

    df["estimate"] = pd.to_numeric(
        df["estimate"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )

    df["moe"] = pd.to_numeric(
        df["moe"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("±", "", regex=False)
        .str.strip(),
        errors="coerce",
    )

    return df

def _parse_acs_cell(value) -> float:
    """Parse ACS export cells: counts with commas, (X) suppressed, or percentages like 3.9%."""
    if pd.isna(value):
        return float("nan")
    s = str(value).strip()
    if s in ("(X)", "", "--", "nan"):
        return float("nan")
    s = s.replace(",", "")
    if s.endswith("%"):
        return float(s[:-1])
    s = s.replace("±", "")
    return float(pd.to_numeric(s, errors="coerce"))

# Loads and cleans the households and families data by converting the data
# to numeric columns. This makes the data easier to analyze. Returns a 
# cleaned dataframe.
def load_clean_households_families_csv(path: Path) -> pd.DataFrame:
    """
    Load the wide 'Households and Families' ACS table: one label column plus
    Total / married-couple / male householder / female householder / nonfamily
    estimate + MOE pairs.
    """
    df = pd.read_csv(path)
    col_names = [
        "label",
        "total_estimate",
        "total_moe",
        "married_couple_estimate",
        "married_couple_moe",
        "male_householder_family_estimate",
        "male_householder_family_moe",
        "female_householder_family_estimate",
        "female_householder_family_moe",
        "nonfamily_estimate",
        "nonfamily_moe",
    ]
    if len(df.columns) != len(col_names):
        raise ValueError(
            f"Expected {len(col_names)} columns in {path}, got {len(df.columns)}"
        )
    df.columns = col_names
    # Removes the non-breaking space and strips the whitespace from the label column.
    df["label"] = (
        df["label"]
        .astype(str)
        .str.replace("\u00a0", " ", regex=False)
        .str.strip()
    )
    for c in col_names[1:]:
        df[c] = df[c].map(_parse_acs_cell)
    return df


# Calculates the total population across sexes by age bracket. 
# This function is used to answer question 1.
def population_by_age_bracket(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sum male + female estimates for each age label in a Sex by Age table.
    Skips Total / Male / Female summary rows.
    """
    section = None
    records: list[dict] = []
    for _, row in df.iterrows():
        lab = row["label"]
        if lab == "Male:":
            section = "male"
            continue
        if lab == "Female:":
            section = "female"
            continue
        if lab == "Total:":
            continue
        if section in ("male", "female"):
            records.append(
                {"age_bracket": lab, "estimate": row["estimate"]}
            )
    out = (
        pd.DataFrame(records)
        # Asking what the total population is for each age bracket after
        # combining the male and female populations. This will be used to answer
        # question 1 which determines the age bracket with the largest population, 
        # but also highlights that the data the full picture of population can only
        # be seen by combining the male and female populations.
        .groupby("age_bracket", as_index=False)["estimate"]
        .sum()
        .rename(columns={"estimate": "population"})
    )
    return out


# Loads and cleans the census data on the actual CSV files for analysis.
dfhouseholdincome = load_clean_census_csv(
    DATA_DIR / "Household Income in the Past Year.csv"
)
dfhouseholdincome_seattle = load_clean_census_csv(
    DATA_DIR / "Seattle Household Income for Past Year.csv"
)
dfsexbyage = load_clean_census_csv(DATA_DIR / "Sex by Age.csv")
dftotalpopulation = load_clean_census_csv(DATA_DIR / "Total Population.csv")
dfhouseholdsfamilies = load_clean_households_families_csv(
    DATA_DIR / "Households and Families.csv"
)

# The code below is used to answer the questions for the analysis.
# Question 1: What age bracket has the highest number of people in the
# dataset population? (Madison Park, WA)

# Calculates the total population by age bracket.
age_totals = population_by_age_bracket(dfsexbyage)

# Asking to drop age brackets where combined male+female count is zero. 
# This is used to ensure the data is not skewed by age brackets with no 
# population, and reveals that the data may have missing values in the age brackets.
age_totals_nonzero = age_totals[age_totals["population"] > 0].copy()

# Calculates the total population of the tract.
total_pop = int(dftotalpopulation.loc[0, "estimate"])
idx = age_totals_nonzero["population"].idxmax()
top = age_totals_nonzero.loc[idx]

# Prints the results of the analysis for question 1.
print("Question 1 - What is the age bracket with the largest population in Madison Park?:")
print(f"  Bracket: {top['age_bracket']}")
print(f"  Population: {int(top['population']):,}")
print(
    f"  Share of tract population: {100 * top['population'] / total_pop:.1f}% "
    f"(total population {total_pop:,} from Total Population table)"
)
print()

# Prints the supporting data for question 1.
print(
    "  Supporting data - population by age bracket (Sex by Age; male + female "
    "combined), sorted by population:"
)
age_support = age_totals_nonzero.assign(
    pct_of_tract=lambda x: (100.0 * x["population"] / total_pop).round(1)
).sort_values("population", ascending=False)
print(age_support.to_string(index=False))
print()
print()
print()

# Question 2: What percentage of households have own children under 18?
# Source: Households and Families.csv — row "Households with own children of
# the householder under 18 years" (total households with own children U18) and
# "Total households" for the denominator.

# Checks for null values in the dataframe.
# Asking how many missing values are in each column, which will be used to 
# help flag any large gaps in the data, or where the spreadsheet uses headers
# instead of actual data. 
_ = dfhouseholdsfamilies.isnull().sum()
# Asking for which row labels appear most often, which will be used to verify
# the table structure and ensure the data format is consistent and being read 
# correctly before picking rows by exact labels.
_ = dfhouseholdsfamilies["label"].value_counts().head(10)

# Defines the label for the households with own children of the householder under 18 years.
OWN_CHILDREN_LABEL = (
    "Households with own children of the householder under 18 years"
)

# Asking to filter rows on the total households row to just the rows where
# the total count is greater than zero. This is used to ensure the data is 
# not skewed by households with no total count, and reveals that data may have
# missing values in the total households row.
hh_totals = dfhouseholdsfamilies[
    (dfhouseholdsfamilies["label"] == "Total households")
    & (dfhouseholdsfamilies["total_estimate"] > 0)
]
total_households = int(hh_totals["total_estimate"].iloc[0])

own_children_row = dfhouseholdsfamilies[
    dfhouseholdsfamilies["label"] == OWN_CHILDREN_LABEL
].iloc[0]

# Calculates the total number of households with own children under 18 years.
households_with_own_children_u18 = int(own_children_row["total_estimate"])
pct_hh_with_children = 100 * households_with_own_children_u18 / total_households

# Calculates the total number of households with own children under 18 years by 
# family type (married-couple family, male householder, female householder).
breakdown = pd.DataFrame(
    {
        "family_type": [
            "Married-couple family household",
            "Male householder, no spouse present, family household",
            "Female householder, no spouse present, family household",
        ],
        "households_with_own_children_u18": [
            own_children_row["married_couple_estimate"],
            own_children_row["male_householder_family_estimate"],
            own_children_row["female_householder_family_estimate"],
        ],
    }
)
# Asking to drop rows where the total number of households with own children 
# under 18 is zero. This is used to ensure the data is not skewed by households 
# with no own children under 18, and reveals that data may have missing values 
# in the households with own children under 18 row.
breakdown = breakdown[breakdown["households_with_own_children_u18"] > 0]
breakdown = breakdown.assign(cohort="Own children under 18 (householder)")
# Asking what the total of households with own children under 18 acrosss 
# the different family types is. This highlights that in the data there are
# different family types that have own children under 18 that have to be accounted
# for in the analysis.
by_cohort = breakdown.groupby("cohort", as_index=False)[
    "households_with_own_children_u18"
].sum()

# Prints the results of the analysis for question 2.
print(
    "Question 2 - What percentage of households have own children of the "
    "householder under 18?"
)
print(f"  Households with own children under 18: {households_with_own_children_u18:,}")
print(f"  Total households: {total_households:,}")
print(f"  Percent of households: {pct_hh_with_children:.1f}%")
print()

# Supporting data for question 2.
print("  Supporting data - family-type counts (households with own children under 18):")
print(breakdown.drop(columns=["cohort"]).to_string(index=False))
print()
print("  Supporting data - groupby(cohort) sum check (matches total-with-children count):")
print(by_cohort.to_string(index=False))
print()
print()
print()

# Question 3: Share of households with income over $100K — Madison Park vs Seattle.
# ACS “Household Income in the Past Year” counts households by bracket (not people).
# Brackets strictly above $75k–$99k start at $100k–$124k through $200k+.

INCOME_BRACKETS_100K_PLUS = [
    "$100,000 to $124,999",
    "$125,000 to $149,999",
    "$150,000 to $199,999",
    "$200,000 or more",
]

# Asking to merge the Madison Park and Seattle household income data by the 
# label column. This is used to compare the household income data for the two areas.
madison_brackets = dfhouseholdincome[["label", "estimate"]].rename(
    columns={"estimate": "madison_households"}
)
seattle_brackets = dfhouseholdincome_seattle[["label", "estimate"]].rename(
    columns={"estimate": "seattle_households"}
)
income_compare = madison_brackets.merge(seattle_brackets, on="label", how="outer")
# Keep Census bracket order (merge alone sorts labels alphabetically).
_bracket_order = madison_brackets["label"].tolist()
income_compare = (
    income_compare.set_index("label").reindex(_bracket_order).reset_index(names="label")
)

# Print only rows needed for Q3: total households + income brackets strictly 
# over $100K.
_Q3_ROW_ORDER = ["Total:"] + INCOME_BRACKETS_100K_PLUS
income_compare_for_print = (
    income_compare.set_index("label")
    .loc[_Q3_ROW_ORDER]
    .reset_index(names="label")
)
# Asking to calculate the total number of households in Madison Park and Seattle.
total_mp = float(
    income_compare.loc[income_compare["label"] == "Total:", "madison_households"].iloc[0]
)
total_sea = float(
    income_compare.loc[income_compare["label"] == "Total:", "seattle_households"].iloc[0]
)
high_brackets = income_compare[income_compare["label"].isin(INCOME_BRACKETS_100K_PLUS)]
over_mp = float(high_brackets["madison_households"].sum())
over_sea = float(high_brackets["seattle_households"].sum())
# Calculates the percentage of households in Madison Park and Seattle that make over 
# $100K a year.
q3_summary = pd.DataFrame(
    {
        "area": ["Madison Park (Census Tract 63)", "Seattle city"],
        "total_households": [total_mp, total_sea],
        "households_over_100k": [over_mp, over_sea],
    }
).assign(
    pct_households_over_100k=lambda x: (
        100.0 * x["households_over_100k"] / x["total_households"]
    ).round(1)
)
# Prints the results of the analysis for question 3.
print(
    "Question 3 - What percent of the population in Madison Park makes over "
    "$100K a year in a household, compared to Seattle?"
)
print(
    "  (From ACS household-income brackets: reported as share of households "
    "with income over $100K, not a direct count of people.)"
)
# Prints the summary of the analysis for question 3.
print(q3_summary.to_string(index=False))
print()
mp_pct = float(q3_summary.iloc[0]["pct_households_over_100k"])
sea_pct = float(q3_summary.iloc[1]["pct_households_over_100k"])
print(f"  Madison Park (share of households): {mp_pct:.1f}%")
print(f"  Seattle (share of households):      {sea_pct:.1f}%")
print(f"  Difference (Madison Park - Seattle): {mp_pct - sea_pct:+.1f} percentage points")
print()

# Supporting data for question 3.
print(
    "  Supporting data - household income (total and brackets over $100K, "
    "Madison Park vs Seattle):"
)
print(income_compare_for_print.to_string(index=False))
print()
