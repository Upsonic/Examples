# task_examples/extract_people/extract_people.py

"""
Extract People Intelligence Agent (Optimized)
---------------------------------------------
Runs only one agent call per input text.

This agent identifies all people mentioned in text and returns
structured details (name, role, affiliation, context, sentiment, confidence).
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from upsonic import Agent, Task


# ======================================================
# 1. Define Response Schemas
# ======================================================

class Person(BaseModel):
    name: str = Field(..., description="Full name of the person")
    role: Optional[str] = Field(None, description="Known or inferred occupation/title (e.g., CEO, artist, president)")
    affiliation: Optional[str] = Field(None, description="Organization or company associated with the person")
    context: Optional[str] = Field(None, description="Short snippet or summary of what the person did or was mentioned for")
    sentiment: Optional[str] = Field(None, description="Sentiment of mention: positive, neutral, or negative")
    confidence: Optional[float] = Field(None, description="Model-estimated confidence score between 0 and 1")


class PeopleResponse(BaseModel):
    people: List[Person] = Field(..., description="List of all people and their contextual details")


# ======================================================
# 2. Initialize Agent
# ======================================================

extract_people_agent = Agent(name="people_intelligence_extractor")


# ======================================================
# 3. Main Example Usage
# ======================================================

if __name__ == "__main__":
    paragraph = (
    "During the recent World Economic Forum in Davos, Elon Musk joined a panel with Christine Lagarde, the President of the European Central Bank, "
    "and Satya Nadella, CEO of Microsoft, to discuss the regulatory challenges of artificial intelligence in global markets. "
    "In a separate session, Kamala Harris emphasized the importance of ethical AI frameworks, echoing earlier remarks made by António Guterres of the United Nations. "
    "Meanwhile, Tim Cook and Sundar Pichai were seen in private talks about developing unified privacy standards, while Meta’s Mark Zuckerberg "
    "announced a new digital responsibility initiative alongside philanthropist Melinda Gates. "
    "Back in the United States, President Donald Trump met with Janet Yellen and Federal Reserve Chair Jerome Powell to evaluate the economic impacts of rapid AI automation on employment. "
    "At the same time, OpenAI’s Sam Altman and Google DeepMind’s Demis Hassabis issued a joint statement with Yoshua Bengio and Geoffrey Hinton, "
    "calling for an international AI safety consortium to prevent misuse of advanced language models. "
    "In the cultural sphere, actress Emma Watson collaborated with environmentalist Leonardo DiCaprio and designer Stella McCartney "
    "on a sustainable fashion campaign supported by the United Nations. "
    "Elsewhere, entrepreneur Jack Ma reemerged publicly in Singapore, meeting with Prime Minister Lee Hsien Loong to discuss regional startup innovation. "
    "Later that evening, philanthropist MacKenzie Scott hosted a private fundraiser attended by Oprah Winfrey, Barack and Michelle Obama, "
    "and tennis champion Naomi Osaka, raising over $50 million for global education programs."
)


    # --- Step 1: Create single extraction task ---
    task = Task(
        description=(
            "Extract every person mentioned in the text below. "
            "For each, include their full name, inferred role, affiliation (if known or inferable), "
            "a concise context summary of their mention, sentiment (positive, neutral, or negative), "
            "and a confidence score between 0 and 1.\n\n"
            f"Text:\n{paragraph}"
        ),
        response_format=PeopleResponse,
    )

    # --- Step 2: Single agent call ---
    result = extract_people_agent.do(task)

    # --- Step 3: Display results ---
    print("\n=== Extracted People Intelligence ===\n")
    for p in result.people:
        print(f"Name: {p.name}")
        if p.role:
            print(f"  Role: {p.role}")
        if p.affiliation:
            print(f"  Affiliation: {p.affiliation}")
        if p.context:
            print(f"  Context: {p.context}")
        if p.sentiment:
            print(f"  Sentiment: {p.sentiment}")
        if p.confidence is not None:
            print(f"  Confidence: {p.confidence:.2f}")
        print("-" * 50)
