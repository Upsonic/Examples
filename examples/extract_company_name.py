from upsonic import Task, Direct
from pydantic import BaseModel

# Define response format
class CompanyResponse(BaseModel):
    company_name: str

# Initialize Upsonic Direct client
client = Direct()

# Create a task with the document as image
task = Task(
    description="Extract the company name from the provided document.",
    images=["examples/assets/vergi_levhasi.png"],
    response_format=CompanyResponse
)

# Run task
result = client.do(task)

# Print
print("Extracted Company Name:", result.company_name)
