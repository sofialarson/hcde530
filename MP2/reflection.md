# MP2 Reflection — Transcript Quote Finder

## What did you build?

Transcript Quote Finder is a UX research tool that helps researchers surface verbatim 
quotes from interview transcripts without manually reading through them. A researcher 
describes what they are looking for in plain language, something as vague as "participant 
seemed annoyed by the navigation" or as specific as "couldn't find the search bar", nd 
the tool interprets the meaning behind that description, searches the transcript, and 
returns the actual verbatim quotes that best match, ranked by relevance. Each result 
includes a match score, highlighted key terms, the speaker label, a timestamp if present, 
and a one-sentence explanation of why that quote was selected. Researchers can filter 
results to specific speakers, set a minimum match score threshold, and save quotes into 
named folders organized by theme — for example, "Navigation Issues" or "Positive 
Reactions" — which can then be exported as a .txt file. The tool runs as an interactive 
Jupyter notebook. It was built specifically for the Otter.ai transcript format but handles 
any plain text or PDF transcript.

## What decisions did you make?

The most significant decision was choosing to build in JupyterLab with ipywidgets rather 
than a hosted platform like Lovable or Bolt. I made this choice because the tool needed 
to handle file uploads, call an external API securely, and manage persistent UI state 
across interactions — constraints that were easier to control directly in Python than 
through a generative web app builder. I originally intended to use the Gemini API as a 
free alternative to Anthropic, but after spending significant time debugging quota errors 
and a deprecated SDK, I switched to Anthropic's Claude API which proved more reliable 
for structured JSON output. The quote library — the folder-based system for saving and 
organizing quotes — was not in my original MP2a declaration. I added it after recognizing 
that researchers don't just need to find one quote; they need to collect multiple quotes 
across several searches and organize them by theme before writing up findings. This 
changed the architecture significantly, requiring two separate output areas so the library 
would persist across searches without being cleared.

## What would you do differently?

I would separate the quote library into its own cell from the start rather than embedding 
it inside the results renderer. Midway through development I realized that re-rendering 
results on every search was destroying the library's DOM, which required a significant 
architectural change to split the output into two independent widget areas. Had I scoped 
this upfront the implementation would have been cleaner. I would also add a way for 
researchers to upload multiple transcripts and tag quotes by participant, so results across 
an entire study could be collected in one session rather than requiring the tool to be 
reloaded for each transcript. That would make it genuinely usable for synthesis across a 
full round of interviews rather than just a single session.

## What does this work demonstrate?

This project most directly demonstrates C8 — building and deploying a complete tool — 
through a working, polished, multi-feature application scoped around a real UX research 
workflow. The tool isn't a demo; it handles real transcripts, real edge cases like 
PDF extraction and Otter.ai speaker label formats, and produces output a researcher 
could actually use. It demonstrates C4 through secure API integration with the Anthropic 
Claude API — the key is stored in a .env file excluded from version control, and the 
system prompt enforces a strict JSON schema that the tool parses and validates client-side. 
It demonstrates C7 through several specific moments of catching and correcting AI behavior: 
the speaker detection regex initially returned 29 false positives because it matched 
timestamp fragments as speaker names, which I diagnosed by inspecting raw matched output 
and rewrote with a pattern anchored on the double-space separator. I also caught that 
Claude occasionally returned quotes with minor whitespace differences from the original, 
causing the jump-to-transcript feature to silently fail — I fixed this by rewriting the 
quote locator to try six progressively fuzzier matching strategies before giving up. 
Finally, it demonstrates C2 through thorough documentation: every function has plain-English 
comments explaining not just what the code does but why specific decisions were made, 
and a separate commented reference document walks through every cell for a non-technical 
reader.
