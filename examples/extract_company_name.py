from upsonic import Task, Agent
from pydantic import BaseModel

# Define response format
class CompanyResponse(BaseModel):
    company_name: str

# Create an Agent
doc_agent = Agent(
    name="document_reader"
)

# Create a task
task = Task(
    description="Extract the company name from the provided document.",
    images=["examples/assets/vergi_levhasi.png"],
    response_format=CompanyResponse
)

# Run the task through the agent
result = doc_agent.do(task)

# Print result
print("Extracted Company Name:", result.company_name)
