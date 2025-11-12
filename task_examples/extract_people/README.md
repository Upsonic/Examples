# Extract People Intelligence Agent

This example shows how to build an Upsonic agent that reads a block of text, finds every person who is mentioned, and returns enriched, structured details for each mention. It is useful when you need people intelligence from meeting notes, news articles, transcripts, or any free-form document.

## Overview
- Single Upsonic `Agent` call per input text.
- Structured response powered by two `pydantic` models (`Person` and `PeopleResponse`).
- Captures richer context for each person: role, affiliation, mention summary, sentiment, and confidence.

---

## Requirements
Run the standard dependency install once per repository clone:

```bash
uv sync
```

---

## Running the example
Execute the script directly (it ships with a verbose demo paragraph):

```bash
uv run task_examples/extract_people/extract_people.py
```

You can swap the sample paragraph for any text you want to analyse.

---

## What the agent returns
The agent yields a `PeopleResponse` object containing a list of `Person` entries. Each entry may include:
- `name`: full name of the person mentioned.
- `role`: inferred title or occupation (e.g. "CEO", "athlete").
- `affiliation`: organisation associated with the person.
- `context`: short description of why the person was mentioned.
- `sentiment`: positive / neutral / negative sentiment of the mention.
- `confidence`: model-estimated confidence (0–1).

---

## Example output
```python
PeopleResponse(
    people=[
        Person(
            name='Elon Musk',
            role='Entrepreneur',
            affiliation='SpaceX',
            context='Met with Bill Gates and Jeff Bezos to discuss space exploration and AI safety.',
            sentiment='neutral',
            confidence=0.92
        ),
        Person(
            name='Taylor Swift',
            role='Singer',
            affiliation=None,
            context='Attended a charity event organised by Oprah Winfrey and Barack Obama.',
            sentiment='positive',
            confidence=0.87
        ),
        # ... additional people omitted for brevity ...
    ]
)
```

---

## How it works
1. Define the response schema (`Person`, `PeopleResponse`) that captures the enriched attributes.
2. Instantiate a single Upsonic `Agent` and create a `Task` instructing the model to extract each person with the required fields.
3. Call `agent.do(task)` and render the structured response.

---

## File structure
```bash
task_examples/extract_people/
├── extract_people.py   # Main example agent
└── README.md           # This guide
```
