# task_examples/document_analyzer/extract_company_name.py

from upsonic import Task, Agent
from pydantic import BaseModel

# Define the response format
class CompanyResponse(BaseModel):
    company_name: str

# Create the agent
doc_agent = Agent(name="document_reader")

# Create the task
task = Task(
    description=(
        "Read the attached Turkish tax certificate (Vergi Levhası) and return the company name "
        "exactly as it appears in the field 'TICARET UNVANI'. "
        "Do not invent, shorten, or replace words. "
        "Return only the full legal company name, nothing else."
    ),
    context=["task_examples/document_analyzer/assets/vergi_levhasi.png"],
    response_format=CompanyResponse
)

# Run the task
result = doc_agent.do(task)

# Print the result
print("Extracted Company Name:", result.company_name)
