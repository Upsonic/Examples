# Crypto Block Policy

This example demonstrates how to use **Upsonic's Safety Engine** with the prebuilt **CryptoBlockPolicy**. The repo contains a single Python script that:

- blocks cryptocurrency-related content in both user inputs and agent outputs, and
- contrasts that strict mode with a second agent that only filters user inputs.

## Overview

The Safety Engine is a powerful feature in Upsonic that allows you to enforce content policies on your LLM agents. This example showcases:

1. **User Policy** — blocks cryptocurrency-related queries from users  
2. **Agent Policy** — prevents the agent from responding with crypto-related information  
3. **Variant configuration** — shows how to run with user-policy-only filtering

The `CryptoBlockPolicy` detects a wide range of crypto terms (Bitcoin, Ethereum, alt coins, blockchain, wallet brands, etc.) and raises a policy violation when triggered.

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

---

## Run the Agent

### Run the demo

```bash
uv run task_examples/crypto_block_policy/crypto_block_policy.py
```

### Example Output

```
======================================================================
Upsonic Safety Engine — Crypto Block Policy Demo
======================================================================
Policy in use: CryptoBlockPolicy
   - Blocks all cryptocurrency-related content.
   - Can be applied to user inputs, agent outputs, or both.

======================================================================
Full Enforcement (Input + Output)
======================================================================

[TEST] Test 1: Asking about Bitcoin
----------------------------------------------------------------------
Query: Can you tell me the current price of Bitcoin and the best wallet to use?
Blocked by runtime policy check: Cryptocurrency related content detected and blocked.

...

Suite Summary
   • Allowed: 1
   • Blocked: 3

Now testing input-only policy configuration...

======================================================================
Input-Only Enforcement Variant
======================================================================

[TEST] Variant 1: Crypto question still blocked
----------------------------------------------------------------------
Query: Should I invest in cryptocurrency right now?
Blocked by runtime policy check: Cryptocurrency related content detected and blocked.

[TEST] Variant 2: Non-crypto question flows normally
----------------------------------------------------------------------
Query: Give me three productivity tips for remote teams.
Allowed response: Certainly! Here are three productivity tips for remote teams:
...

Suite Summary
   • Allowed: 1
   • Blocked: 1
```

---

## How It Works

1. **Policy Definition**: The `CryptoBlockPolicy` is imported from Upsonic's safety engine as a prebuilt rule set.  
2. **Policy Application**: The script applies the policy in two configurations:
   - `user_policy` and `agent_policy` together (full bidirectional filtering)
   - `user_policy` only (filters the audience’s questions but not the answers)  
3. **Automatic Blocking**: When crypto-related content is detected, the Safety Engine either raises an exception or returns a policy violation response. The helper function classifies the request as blocked, prints the matched terms when available, and keeps the suite totals accurate.

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

