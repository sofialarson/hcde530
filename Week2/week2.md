# Competency 2 — Code reading (Week 2)

**Course definition:** *“Code Reading. Read and explain what a given block of code does.”*

## Code block I’m explaining

I focused on the `count_words` function in `demo_word_count.py`, starting at **line 17**.

```python
def count_words(response):
    """Count words in a response string."""
    if response == NOT_AVAILABLE:
        return 0
    return len(response.split())
```

## What this block does (in plain language)

- **When the response is normal text:** The function counts how many words are in that string. It does that by **splitting** the response into smaller pieces (by default, split separates on whitespace) and then counting how many pieces there are.
- **When the response is not normal text** — for example, the value was missing and was replaced with `Not available` — the function **returns 0** instead of trying to count words.

## Why returning 0 matters (research + reliability)

I wanted the script **not to crash** when a field was empty or missing. As a researcher, I also care about having some **representation of a non-answer** so it’s clearer what share of participants actually provided usable text, rather than losing the row entirely or failing silently in a confusing way.

## What was confusing at first

The **`.split()`** part was a little confusing on its own: the name doesn’t spell out that it breaks the string into words (using whitespace). What helped it click was **reading official documentation** about Python’s `str.split` behavior.

## Habit I’ll keep for code reading

I will **keep looking up official documentation** when I hit an unfamiliar method, instead of guessing what it does from the name alone.
