#!/usr/bin/env python3
"""
Test script for the fraud detection example.
This script tests the example with JSON storage (no external dependencies).
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


from upsonic import Agent, Task
from upsonic.tools import tool
from upsonic.storage.memory.memory import Memory
from upsonic.storage.providers.json import JSONStorage
from upsonic.models import infer_model
from pydantic import BaseModel, Field


class FraudAnalysisResult(BaseModel):
    """Result of fraud analysis."""
    is_fraud: bool
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_factors: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    recommendation: str


@tool
def check_merchant_reputation(merchant_name: str) -> dict:
    """Check the reputation of a merchant for fraud indicators."""
    suspicious_merchants = ["unknown_merchant", "suspicious_store", "fraud_inc"]
    
    if merchant_name.lower() in suspicious_merchants:
        return {
            "reputation_score": 0.2,
            "is_blacklisted": True,
            "warnings": ["Merchant flagged for suspicious activity"]
        }
    
    return {
        "reputation_score": 0.8,
        "is_blacklisted": False,
        "warnings": []
    }


async def test_fraud_detection():
    """Test the fraud detection example with JSON storage."""
    print("🧪 Testing Fraud Detection Example")
    print("=" * 50)
    
    # Create storage and memory
    storage = JSONStorage("./test_fraud_data")
    await storage.connect_async()
    
    memory = Memory(
        storage=storage,
        session_id="test_session_001",
        user_id="test_user_001",
        full_session_memory=True,
        summary_memory=True,
        user_analysis_memory=True,
        model=infer_model("gpt-4o-mini"),
        debug=True
    )
    
    # Create agent
    agent = Agent(
        name="TestFraudAgent",
        memory=memory,
        model=infer_model("gpt-4o-mini"),
        debug=True
    )
    
    # Test transaction
    test_prompt = """
    Analyze this banking transaction for potential fraud:
    
    Transaction Details:
    - Amount: $15,000.00
    - Merchant: unknown_merchant
    - Location: Unknown Location
    - Account Balance: $1,000.00
    - Type: debit
    
    User Profile:
    - Risk Tolerance: medium
    - Typical Transaction Amount: $500.00
    - Usual Locations: New York, San Francisco
    - Account Age: 365 days
    
    Use the available tools to check merchant reputation and provide fraud analysis.
    """
    
    # Create task
    task = Task(
        description=test_prompt,
        response_format=FraudAnalysisResult,
        tools=[check_merchant_reputation]
    )
    
    try:
        # Execute analysis
        result = await agent.do_async(task)
        
        print("✅ Test completed successfully!")
        print(f"   Is Fraud: {result.is_fraud}")
        print(f"   Risk Score: {result.risk_score}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Risk Factors: {result.risk_factors}")
        print(f"   Recommendation: {result.recommendation}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        await storage.disconnect_async()


if __name__ == "__main__":
    success = asyncio.run(test_fraud_detection())
    sys.exit(0 if success else 1)
