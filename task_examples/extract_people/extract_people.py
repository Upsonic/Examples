# task_examples/extract_people/extract_people.py

from pydantic import BaseModel, Field
from upsonic import Agent, Task

# --- Step 1: Define response format ---
class PeopleResponse(BaseModel):
    people: list[str] = Field(..., description="List of all people mentioned in the text")

# --- Step 2: Define the agent ---
extract_people_agent = Agent(name="people_extractor")

# --- Step 3: Example usage ---
if __name__ == "__main__":
    paragraph = (
        "Last week, Elon Musk met with Bill Gates and Jeff Bezos in California to discuss the future of space exploration and AI safety. "
        "Meanwhile, Taylor Swift and Beyoncé were seen attending a charity event organized by Oprah Winfrey and Barack Obama in New York. "
        "Mark Zuckerberg and Sundar Pichai joined Tim Cook for a roundtable about responsible technology innovation, while Serena Williams and LeBron James spoke about athlete mental health. "
        "Later in the evening, Michelle Obama delivered a heartfelt speech, joined by Malala Yousafzai and Greta Thunberg, who emphasized the importance of education and climate action. "
        "Across the globe, Pope Francis and the Dalai Lama held an interfaith dialogue in Rome, and Lionel Messi congratulated Cristiano Ronaldo on his milestone goal. "
        "At the same time, Emma Watson and Leonardo DiCaprio discussed sustainable fashion with Natalie Portman and Ryan Reynolds. "
        "Finally, in a surprising turn, Warren Buffett and Charlie Munger announced new philanthropic initiatives inspired by Melinda Gates and Mackenzie Scott."
    )

    task = Task(
        description=f"Extract all the person names mentioned in the following text:\n\n{paragraph}",
        response_format=PeopleResponse,
    )

    result = extract_people_agent.do(task)
    print(result)
