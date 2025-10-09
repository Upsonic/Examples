# task_examples/crypto_block_policy/crypto_block_policy.py

from upsonic import Agent, Task
from upsonic.safety_engine import CryptoBlockPolicy

# --- Step 1: Create an agent with CryptoBlockPolicy ---
# The CryptoBlockPolicy is a prebuilt policy from Upsonic that blocks cryptocurrency-related content
crypto_agent = Agent(
    name="Crypto-Sensitive Agent",
    role="Assistant adhering to content policies",
    goal="Provide information while blocking cryptocurrency-related content",
    instructions="Avoid discussing or providing information about cryptocurrencies.",
    user_policy=CryptoBlockPolicy,  # Apply policy to user inputs
    agent_policy=CryptoBlockPolicy  # Apply policy to agent outputs
)

# --- Step 2: Example usage - Testing with crypto-related content ---
if __name__ == "__main__":
    print("=" * 70)
    print("🛡️  Crypto Block Policy Demo - Upsonic Safety Engine")
    print("=" * 70)
    print()
    print("This demo shows how the CryptoBlockPolicy automatically blocks")
    print("cryptocurrency-related content in both user inputs and agent outputs.")
    print()
    print("=" * 70)
    print()
    
    # Test 1: Direct crypto query (Bitcoin)
    print("📝 Test 1: Asking about Bitcoin")
    print("-" * 70)
    crypto_query_1 = Task(
        description="Can you tell me the current price of Bitcoin and the best wallet to use?",
        response_format=str
    )
    
    try:
        crypto_agent.print_do(crypto_query_1)
    except Exception as e:
        print(f"❌ Content blocked: {str(e)}")
    print()
    
    # Test 2: Ethereum query
    print("📝 Test 2: Asking about Ethereum")
    print("-" * 70)
    crypto_query_2 = Task(
        description="What are the benefits of Ethereum smart contracts?",
        response_format=str
    )
    
    try:
        crypto_agent.print_do(crypto_query_2)
    except Exception as e:
        print(f"❌ Content blocked: {str(e)}")
    print()
    
    # Test 3: General crypto question
    print("📝 Test 3: Asking about cryptocurrency in general")
    print("-" * 70)
    crypto_query_3 = Task(
        description="Should I invest in cryptocurrency?",
        response_format=str
    )
    
    try:
        crypto_agent.print_do(crypto_query_3)
    except Exception as e:
        print(f"❌ Content blocked: {str(e)}")
    print()
    
    print("=" * 70)
    print("✅ Demo Complete! All crypto-related queries were blocked.")
    print("=" * 70)
    print()
    print("💡 Key Takeaway: The CryptoBlockPolicy successfully prevents")
    print("   discussions about Bitcoin, Ethereum, and other cryptocurrencies.")
    print("=" * 70)
