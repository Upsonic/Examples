from pydantic import BaseModel, Field
from typing import Optional


class ExpenseData(BaseModel):
    date: str = Field(description="Invoice date (YYYY-MM-DD)")
    amount: float = Field(description="Total amount (TL)")
    merchant: str = Field(description="Merchant/store name")
    category: str = Field(description="Expense category")
    description: Optional[str] = Field(default=None, description="Description")
    ocr_confidence: float = Field(description="OCR confidence score (0-1)")
