#!/usr/bin/env python3
"""
Banking Fraud Detection Agent

This example demonstrates a comprehensive fintech fraud detection system using
Upsonic's Agent, Task, Memory, and all available Storage providers.

The agent analyzes banking transactions and user behavior to detect potential fraud,
maintaining persistent memory across sessions and using various storage backends.
"""

import asyncio
import argparse
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import random

from upsonic import Agent, Task
from upsonic.tools import tool
from upsonic.storage.memory.memory import Memory
from upsonic.storage.providers.json import JSONStorage
from upsonic.storage.providers.sqlite import SqliteStorage
from upsonic.storage.providers.redis import RedisStorage
from upsonic.storage.providers.mongo import MongoStorage
from upsonic.storage.providers.postgres import PostgresStorage
try:
    from upsonic.storage.providers.mem0 import Mem0Storage
    _MEM0_AVAILABLE = True
except ImportError:
    Mem0Storage = None
    _MEM0_AVAILABLE = False
from upsonic.storage.providers.in_memory import InMemoryStorage
from upsonic.models import infer_model


class Transaction(BaseModel):
    """Represents a banking transaction."""
    transaction_id: str
    user_id: str
    amount: float
    currency: str = "USD"
    merchant: str
    location: str
    timestamp: datetime
    transaction_type: str  # "debit", "credit", "transfer"
    account_balance: float


class FraudAnalysisResult(BaseModel):
    """Result of fraud analysis."""
    is_fraud: bool
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_factors: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    recommendation: str
    suspicious_patterns: List[str] = Field(default_factory=list)


class UserProfile(BaseModel):
    """User profile for fraud detection."""
    user_id: str
    risk_tolerance: str  # "low", "medium", "high"
    typical_transaction_amount: float
    frequent_merchants: List[str]
    usual_locations: List[str]
    account_age_days: int


@tool
def check_merchant_reputation(merchant_name: str) -> Dict[str, Any]:
    """Check the reputation of a merchant for fraud indicators."""
    # Simulate merchant reputation check
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


@tool
def verify_location_consistency(user_id: str, transaction_location: str) -> Dict[str, Any]:
    """Verify if transaction location is consistent with user's usual locations."""
    # Simulate location verification
    usual_locations = ["New York", "San Francisco", "Los Angeles"]
    
    if transaction_location not in usual_locations:
        return {
            "is_consistent": False,
            "risk_factor": "Unusual location",
            "distance_from_usual": "High"
        }
    
    return {
        "is_consistent": True,
        "risk_factor": None,
        "distance_from_usual": "Low"
    }


@tool
def check_transaction_frequency(user_id: str, amount: float) -> Dict[str, Any]:
    """Check if transaction frequency and amount are within normal patterns."""
    # Simulate frequency check
    if amount > 10000:  # High amount
        return {
            "frequency_risk": "High",
            "amount_risk": "High",
            "pattern_deviation": "Significant"
        }
    elif amount > 5000:  # Medium amount
        return {
            "frequency_risk": "Medium",
            "amount_risk": "Medium", 
            "pattern_deviation": "Moderate"
        }
    
    return {
        "frequency_risk": "Low",
        "amount_risk": "Low",
        "pattern_deviation": "Minimal"
    }


def create_sample_transactions() -> List[Transaction]:
    """Create sample transactions for testing."""
    transactions = [
        Transaction(
            transaction_id="TXN001",
            user_id="user_001",
            amount=150.00,
            merchant="Starbucks Coffee",
            location="New York",
            timestamp=datetime.now() - timedelta(hours=2),
            transaction_type="debit",
            account_balance=5000.00
        ),
        Transaction(
            transaction_id="TXN002", 
            user_id="user_001",
            amount=2500.00,
            merchant="Electronics Store",
            location="San Francisco",
            timestamp=datetime.now() - timedelta(hours=1),
            transaction_type="debit",
            account_balance=2500.00
        ),
        Transaction(
            transaction_id="TXN003",
            user_id="user_001", 
            amount=15000.00,
            merchant="unknown_merchant",
            location="Unknown Location",
            timestamp=datetime.now() - timedelta(minutes=30),
            transaction_type="debit",
            account_balance=1000.00
        ),
        Transaction(
            transaction_id="TXN004",
            user_id="user_002",
            amount=50.00,
            merchant="Gas Station",
            location="Los Angeles", 
            timestamp=datetime.now() - timedelta(minutes=15),
            transaction_type="debit",
            account_balance=2000.00
        )
    ]
    return transactions


def create_sample_user_profiles() -> List[UserProfile]:
    """Create sample user profiles."""
    return [
        UserProfile(
            user_id="user_001",
            risk_tolerance="medium",
            typical_transaction_amount=500.00,
            frequent_merchants=["Starbucks Coffee", "Amazon", "Target"],
            usual_locations=["New York", "San Francisco"],
            account_age_days=365
        ),
        UserProfile(
            user_id="user_002", 
            risk_tolerance="low",
            typical_transaction_amount=100.00,
            frequent_merchants=["Gas Station", "Grocery Store"],
            usual_locations=["Los Angeles"],
            account_age_days=180
        )
    ]


async def run_fraud_detection_with_storage(storage_provider: str, storage_instance):
    """Run fraud detection with a specific storage provider."""
    print(f"\n{'='*80}")
    print(f"🔍 FRAUD DETECTION WITH {storage_provider.upper()} STORAGE")
    print(f"{'='*80}")
    
    # Create memory system
    memory = Memory(
        storage=storage_instance,
        session_id=f"fraud_session_{random.randint(1000, 9999)}",
        user_id="fraud_analyst_001",
        full_session_memory=True,
        summary_memory=True,
        user_analysis_memory=True,
        model=infer_model("gpt-4o-mini"),
        debug=True
    )
    
    # Create fraud detection agent
    agent = Agent(
        name="FraudDetectionAgent",
        memory=memory,
        model=infer_model("gpt-4o-mini"),
        debug=True
    )
    
    # Get sample data
    transactions = create_sample_transactions()
    user_profiles = create_sample_user_profiles()
    
    # Process each transaction
    for i, transaction in enumerate(transactions, 1):
        print(f"\n📊 ANALYZING TRANSACTION {i}: {transaction.transaction_id}")
        print(f"Amount: ${transaction.amount} | Merchant: {transaction.merchant}")
        print(f"Location: {transaction.location} | User: {transaction.user_id}")
        
        # Find user profile
        user_profile = next((p for p in user_profiles if p.user_id == transaction.user_id), None)
        
        # Create analysis prompt
        analysis_prompt = f"""
        Analyze this banking transaction for potential fraud:
        
        Transaction Details:
        - ID: {transaction.transaction_id}
        - Amount: ${transaction.amount} {transaction.currency}
        - Merchant: {transaction.merchant}
        - Location: {transaction.location}
        - Type: {transaction.transaction_type}
        - Account Balance: ${transaction.account_balance}
        - Timestamp: {transaction.timestamp}
        
        User Profile:
        - Risk Tolerance: {user_profile.risk_tolerance if user_profile else 'Unknown'}
        - Typical Transaction Amount: ${user_profile.typical_transaction_amount if user_profile else 'Unknown'}
        - Frequent Merchants: {user_profile.frequent_merchants if user_profile else 'Unknown'}
        - Usual Locations: {user_profile.usual_locations if user_profile else 'Unknown'}
        - Account Age: {user_profile.account_age_days if user_profile else 'Unknown'} days
        
        Use the available tools to check merchant reputation, location consistency, and transaction patterns.
        Provide a comprehensive fraud analysis with risk assessment.
        """
        
        # Create task
        task = Task(
            description=analysis_prompt,
            response_format=FraudAnalysisResult,
            tools=[check_merchant_reputation, verify_location_consistency, check_transaction_frequency]
        )
        
        # Execute fraud analysis
        try:
            result = await agent.do_async(task)
            
            print(f"\n🎯 FRAUD ANALYSIS RESULT:")
            print(f"   Is Fraud: {'🚨 YES' if result.is_fraud else '✅ NO'}")
            print(f"   Risk Score: {result.risk_score:.2f}/1.0")
            print(f"   Confidence: {result.confidence:.2f}/1.0")
            print(f"   Risk Factors: {', '.join(result.risk_factors)}")
            print(f"   Recommendation: {result.recommendation}")
            if result.suspicious_patterns:
                print(f"   Suspicious Patterns: {', '.join(result.suspicious_patterns)}")
                
        except Exception as e:
            print(f"❌ Error analyzing transaction: {e}")
    
    # Display memory statistics
    print(f"\n📈 MEMORY STATISTICS:")
    print(f"   Session ID: {memory.session_id}")
    print(f"   User ID: {memory.user_id}")
    print(f"   Storage Provider: {storage_provider}")


async def main():
    """Main function to run fraud detection with all storage providers."""
    parser = argparse.ArgumentParser(description="Banking Fraud Detection Agent")
    parser.add_argument("--storage", choices=[
        "json", "sqlite", "redis", "mongo", "postgres", "mem0", "inmemory", "all"
    ], default="all", help="Storage provider to use")
    args = parser.parse_args()
    
    print("🏦 BANKING FRAUD DETECTION AGENT")
    print("=" * 50)
    print("This example demonstrates fraud detection using various storage providers.")
    print("The agent analyzes transactions and maintains persistent memory.")
    
    if args.storage == "all":
        # Test all storage providers
        storage_configs = [
            ("JSON", JSONStorage("./fraud_data")),
            ("SQLite", SqliteStorage("sessions", "profiles", "./fraud_data.db")),
            ("InMemory", InMemoryStorage(max_sessions=100, max_profiles=50))
        ]
        
        # Add Redis if available
        try:
            storage_configs.append(("Redis", RedisStorage("fraud_detection", host="localhost", port=6379)))
        except Exception as e:
            print(f"⚠️  Redis not available: {e}")
        
        # Add MongoDB if available  
        try:
            storage_configs.append(("MongoDB", MongoStorage("mongodb://localhost:27017", "fraud_detection")))
        except Exception as e:
            print(f"⚠️  MongoDB not available: {e}")
            
        # Add PostgreSQL if available
        try:
            storage_configs.append(("PostgreSQL", PostgresStorage("sessions", "profiles", "postgresql://postgres:password@localhost:5432/fraud_detection")))
        except Exception as e:
            print(f"⚠️  PostgreSQL not available: {e}")
            
        # Add Mem0 if available
        try:
            from upsonic.storage.providers.mem0 import Mem0Storage
            storage_configs.append(("Mem0", Mem0Storage(namespace="fraud_detection")))
        except Exception as e:
            print(f"⚠️  Mem0 not available: {e}")
        
        # Run with each storage provider
        for storage_name, storage_instance in storage_configs:
            try:
                await storage_instance.connect_async()
                await run_fraud_detection_with_storage(storage_name, storage_instance)
                await storage_instance.disconnect_async()
            except Exception as e:
                print(f"❌ Error with {storage_name}: {e}")
                continue
                
    else:
        # Test specific storage provider
        storage_map = {
            "json": JSONStorage("./fraud_data"),
            "sqlite": SqliteStorage("sessions", "profiles", "./fraud_data.db"),
            "redis": RedisStorage("fraud_detection", host="localhost", port=6379),
            "mongo": MongoStorage("mongodb://admin:password@localhost:27017", "fraud_detection"),
            "postgres": PostgresStorage("sessions", "profiles", "postgresql://localhost:5432/postgres"),
            "inmemory": InMemoryStorage(max_sessions=100, max_profiles=50)
        }
        
        # Add Mem0 if available
        try:
            if _MEM0_AVAILABLE:
                storage_map["mem0"] = Mem0Storage(namespace="fraud_detection")
        except NameError:
            pass
        
        storage_instance = storage_map[args.storage]
        if storage_instance is None:
            print(f"❌ Storage provider '{args.storage}' is not available")
            return
        await storage_instance.connect_async()
        await run_fraud_detection_with_storage(args.storage, storage_instance)
        await storage_instance.disconnect_async()


if __name__ == "__main__":
    asyncio.run(main())
