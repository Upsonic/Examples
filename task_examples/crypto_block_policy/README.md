# Crypto Block Policy

This example demonstrates how to use **Upsonic's Safety Engine** with a prebuilt **CryptoBlockPolicy** to automatically block cryptocurrency-related content in both user inputs and agent outputs.

## Overview

The Safety Engine is a powerful feature in Upsonic that allows you to enforce content policies on your LLM agents. This example showcases:

1. **User Policy** — Blocks cryptocurrency-related queries from users
2. **Agent Policy** — Prevents the agent from discussing or providing crypto-related information

The `CryptoBlockPolicy` is a prebuilt policy that detects and blocks content related to:
- Bitcoin
- Ethereum
- Cryptocurrency
- Blockchain
- And other crypto-related terms

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

---

## Run the Agent

### Example Usage

The script includes three test cases demonstrating different crypto-related queries:

- **Test 1**: Question about Bitcoin (should be blocked)
- **Test 2**: Question about Ethereum (should be blocked)
- **Test 3**: General cryptocurrency question (should be blocked)

### Run the demo

```bash
uv run task_examples/crypto_block_policy/crypto_block_policy.py
```

### Example Output

```
======================================================================
🛡️  Crypto Block Policy Demo - Upsonic Safety Engine
======================================================================

This demo shows how the CryptoBlockPolicy automatically blocks
cryptocurrency-related content in both user inputs and agent outputs.

======================================================================

📝 Test 1: Asking about Bitcoin
----------------------------------------------------------------------
╭───────────────────────── 🤖 Agent Started ─────────────────────────╮
│  Agent Status:           🚀 Started to work                        │
│  Agent Name:             Crypto-Sensitive Agent                    │
╰────────────────────────────────────────────────────────────────────╯

Cryptocurrency related content detected and blocked.

📝 Test 2: Asking about Ethereum
----------------------------------------------------------------------
╭───────────────────────── 🤖 Agent Started ─────────────────────────╮
│  Agent Status:           🚀 Started to work                        │
│  Agent Name:             Crypto-Sensitive Agent                    │
╰────────────────────────────────────────────────────────────────────╯

Cryptocurrency related content detected and blocked.

📝 Test 3: Asking about cryptocurrency in general
----------------------------------------------------------------------
╭───────────────────────── 🤖 Agent Started ─────────────────────────╮
│  Agent Status:           🚀 Started to work                        │
│  Agent Name:             Crypto-Sensitive Agent                    │
╰────────────────────────────────────────────────────────────────────╯

Cryptocurrency related content detected and blocked.

======================================================================
✅ Demo Complete! All crypto-related queries were blocked.
======================================================================
```

---

## How It Works

1. **Policy Definition**: The `CryptoBlockPolicy` is imported from Upsonic's safety engine as a prebuilt policy.
2. **Policy Application**: The policy is applied to both:
   - `user_policy` — Filters incoming user messages
   - `agent_policy` — Filters outgoing agent responses
3. **Automatic Blocking**: When crypto-related content is detected, the Safety Engine automatically blocks it and returns a policy violation message.

---

## Code Example

```python
from upsonic import Agent, Task
from upsonic.safety_engine import CryptoBlockPolicy

# Create an agent with CryptoBlockPolicy
crypto_agent = Agent(
    name="Crypto-Sensitive Agent",
    role="Assistant adhering to content policies",
    goal="Provide information while blocking cryptocurrency-related content",
    instructions="Avoid discussing or providing information about cryptocurrencies.",
    user_policy=CryptoBlockPolicy,  # Apply to user inputs
    agent_policy=CryptoBlockPolicy  # Apply to agent outputs
)

# Test with a crypto query
task = Task(
    description="Can you tell me about Bitcoin?",
    response_format=str
)

crypto_agent.print_do(task)  # This will be blocked
```

---

## File Structure

```bash
task_examples/crypto_block_policy/
├── crypto_block_policy.py      # Main demo script
└── README.md                   # This file
```

---

## Use Cases

- **Financial compliance**: Block cryptocurrency discussions in regulated financial services
- **Enterprise policies**: Enforce company policies against crypto-related communications
- **Content moderation**: Automatically filter crypto content in customer support
- **Educational platforms**: Prevent crypto promotion in learning environments

---

## Notes

- **Prebuilt Policy**: No need to implement the blocking logic — Upsonic provides it out of the box
- **Dual Protection**: Policies can be applied to both user inputs and agent outputs
- **Easy Integration**: Just add the policy to your Agent constructor
- **Extensible**: You can combine multiple policies or create custom ones

For more information on Safety Engine and custom policies, visit: [Upsonic Safety Engine Documentation](https://docs.upsonic.ai/guides/3_add_a_safety_engine)

