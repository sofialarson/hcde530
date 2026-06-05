# Transcript Quote Finder

## What is this tool?

Transcript Quote Finder is a tool built for UX researchers who work with interview transcripts. 
Instead of manually scanning through long transcripts to find quotes that support a theme or 
observation, you describe what you're looking for in plain language, as vague or specific as 
you like, and the tool finds the best matching verbatim quotes from your transcript, ranked 
by how closely they match your description.

For example, you might type "participant seemed frustrated they couldn't find what they were
looking for" and the tool will return the actual quotes from the transcript that best capture 
that sentiment, complete with timestamps, speaker labels, and an explanation of why each quote 
was selected.

## Who is it for?

This tool is for UX researchers and designers who conduct user interviews and need to efficiently 
surface supporting quotes during analysis. It is especially useful when you remember the gist of 
something a participant said but can't locate the exact wording in a long transcript.

## What can it do?

- Accept transcripts by pasting text directly or uploading a .txt or .pdf file
- Show an inline PDF preview before extracting text
- Automatically detect speaker labels from Otter.ai-style transcripts
- Filter the search to specific speakers only (e.g. only the participant, not the interviewer)
- Return verbatim quotes ranked by match score with highlighted key terms
- Set a minimum match score threshold to filter out weak results
- Click any result card to jump to that quote's location in the transcript
- Save quotes to a persistent folder-based library organized by theme
- Export saved quotes from any folder as a .txt file

## How to run it

### Requirements

- Python 3.10 or later
- JupyterLab
- An Anthropic API key (get one at https://console.anthropic.com)

### Setup

1. Clone or download this repository
2. In the same folder as the notebook, create a file called `.env` containing: ANTHROPIC_API_KEY=your-key-here
3. Open a terminal in that folder and install dependencies: pip install anthropic python-dotenv pypdf ipywidgets
4. Launch JupyterLab
5. Open `MP2.ipynb` and run all cells from top to bottom

Then open the URL it prints in your browser.

## Viewing the notebook on GitHub

You can browse the full notebook with code and comments here:

**[github.com/YOUR-USERNAME/YOUR-REPO-NAME/blob/main/MP2.ipynb](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME/blob/main/MP2.ipynb)**
This tool requires a live Python kernel and an Anthropic API key to run. To use it locally, clone the repo, add your API key to a .env file, and launch the notebook in JupyterLab.
I'll include a link to a demonstration of this tool as a substitute to show that it works. 
Please use this link to see the tool when fully functional: https://www.loom.com/share/1f90719b1c854d95819c2e23703f4b38

## Note on API key security

This tool requires an Anthropic API key to function. The key is stored in a local `.env` 
file that is excluded from version control via `.gitignore`. Never paste your API key 
directly into the notebook or commit it to GitHub.
