# Extract People

This example demonstrates how to build a simple **Upsonic LLM agent** that extracts all person names mentioned in a given text using structured output.

## Overview

The agent takes a paragraph of text as input and returns a list of all people mentioned in it. This is useful for:

- **Named Entity Recognition (NER)** — extracting people from articles, documents, or transcripts.
- **Contact Discovery** — identifying key individuals mentioned in meeting notes or emails.
- **Data Extraction** — parsing unstructured text for specific information.

The agent uses a single LLM Task with a structured response format to ensure consistent output.

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

---

## Run the Agent

### Example

The script includes a sample paragraph mentioning multiple famous individuals from various fields (tech, entertainment, sports, politics, etc.).

```bash
uv run task_examples/extract_people/extract_people.py
```

### Example Output

```python
PeopleResponse(
    people=[
        'Elon Musk',
        'Bill Gates',
        'Jeff Bezos',
        'Taylor Swift',
        'Beyoncé',
        'Oprah Winfrey',
        'Barack Obama',
        'Mark Zuckerberg',
        'Sundar Pichai',
        'Tim Cook',
        'Serena Williams',
        'LeBron James',
        'Michelle Obama',
        'Malala Yousafzai',
        'Greta Thunberg',
        'Pope Francis',
        'Dalai Lama',
        'Lionel Messi',
        'Cristiano Ronaldo',
        'Emma Watson',
        'Leonardo DiCaprio',
        'Natalie Portman',
        'Ryan Reynolds',
        'Warren Buffett',
        'Charlie Munger',
        'Melinda Gates',
        'Mackenzie Scott'
    ]
)
```

---

## How It Works

1. **Input**: The agent receives a paragraph of text containing mentions of various people.
2. **Processing**: The LLM analyzes the text and identifies all person names.
3. **Output**: Returns a structured `PeopleResponse` object with a list of names in the `people` field.

---

## File Structure

```bash
task_examples/extract_people/
├── extract_people.py      # Main people extraction agent
└── README.md              # This file
```

---
