# Week 2 Project Context (HCDE530)

## Project Goal
This project demonstrates how to process a data file effectively and highlight the most important parts of the code.

## Audience
- Primary audience: course instructor.
- The instructor should be able to run the script easily and review both terminal output and a generated webpage report.

## Practitioner Context
- Project owner background: HCD/UX research practitioner (not a software engineer).
- Code should stay intro-level and readable.
- Explanations should prioritize clarity over technical complexity.

## Desired Outputs
The script should produce:
- Word counts for responses.
- Summary statistics (for example: total, min, max, average).
- A chart in a generated HTML report.
- Plain-language key insights written in straightforward tone.

## Technical Preferences
- Use standard Python only (no extra dependencies like pandas/matplotlib).
- Use one command to run the analysis and generate the HTML report.
- Save the generated report as `Week2/context.html`.

## Data and Fields
- Current data source: `Week2/demo_responses.csv`.
- Expected fields include: `participant_id`, `role`, and `response`.
- Keep participant identifiers visible in outputs (do not mask IDs).

## Missing Data Handling
- Do not crash when fields are missing.
- Show user-friendly placeholders such as `Not available` in output/report.

## Style Guidelines for Code
- Keep code beginner-friendly, with clear variable names and small functions.
- Include concise comments to highlight important logic.
- Avoid advanced patterns unless they are necessary.

## Definition of Success
This project is successful when:
1. The instructor can run one command without extra setup.
2. The script reads the CSV and computes response word counts correctly.
3. Terminal output includes a clear row-by-row and summary view.
4. `Week2/context.html` is generated with:
   - Project goal
   - Data overview
   - Word count chart
   - Summary stats
   - Plain-language insights
5. Missing fields are displayed as `Not available` instead of causing errors.
