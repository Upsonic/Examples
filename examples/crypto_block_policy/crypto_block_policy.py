# task_examples/crypto_block_policy/crypto_block_policy.py

"""
Crypto Block Policy Agent Demo
------------------------------
Demonstrates how Upsonic's CryptoBlockPolicy enforces safety rules
by blocking cryptocurrency-related content in both user inputs
and agent outputs.

This example also compares two configurations:
1. Full bidirectional enforcement (input + output)
2. Input-only enforcement (blocks user queries but allows free responses)

Run:
    uv run task_examples/crypto_block_policy/crypto_block_policy.py
"""

from collections import Counter
from typing import Any

from upsonic import Agent, Task
from upsonic.safety_engine import CryptoBlockPolicy

RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

BLOCK_INDICATORS = (
    "detected and blocked",
    "blocked by policy",
    "policy violation",
)

# -------------------------------------------------------------------------
# Test helpers
# -------------------------------------------------------------------------
def detect_policy_block(result: Any) -> tuple[bool, str]:
    """Try to infer whether the policy blocked the request even without an exception."""
    # Upsonic may return a structured object; handle common possibilities defensively.
    message: str | None = None

    if hasattr(result, "blocked") and getattr(result, "blocked"):  # type: ignore[attr-defined]
        message = getattr(result, "message", None) or str(result)
        return True, message

    if isinstance(result, dict):
        if result.get("blocked") is True:
            return True, str(result.get("message") or result)
        message = result.get("message")

    if message is None:
        message = str(result)

    lower_message = message.lower()
    if any(indicator in lower_message for indicator in BLOCK_INDICATORS):
        return True, message

    return False, message


def run_test_case(title: str, description: str, agent: Agent, expect_blocked: bool) -> str:
    """Execute a single query and show whether it was blocked or allowed."""
    print(f"[TEST] {title}")
    print("-" * 70)
    print(f"{CYAN}Query:{RESET} {description}")
    task = Task(description=description, response_format=str)

    try:
        result = agent.do(task)
    except Exception as exc:
        policy_name = getattr(agent.user_policy, "__name__", "Policy") if agent.user_policy else "Policy"
        matched = getattr(exc, "matched_terms", None)
        print(f"{RED}Blocked by {policy_name}:{RESET} {exc}")
        if matched:
            print(f"   Matched terms: {', '.join(matched)}")
        elif hasattr(exc, "policy_name"):
            print(f"   Policy detail: {exc.policy_name}")
        status = "blocked"
    else:
        blocked, message = detect_policy_block(result)
        if blocked:
            status = "blocked"
            print(f"{RED}Blocked by runtime policy check:{RESET} {message}")
            if not expect_blocked:
                print(f"{RED}Unexpected block for a non-crypto query.{RESET}")
        else:
            status = "allowed"
            if expect_blocked:
                print(f"{RED}Expected a block, but the request was allowed.{RESET}")
            print(f"{GREEN}Allowed response:{RESET} {message}")

    print()
    return status


def run_suite(title: str, cases: list[tuple[str, str, Agent, bool]]) -> Counter:
    """Run a suite of test cases and print a result summary."""
    print("=" * 70)
    print(title)
    print("=" * 70)
    print()

    outcomes = Counter()
    for case in cases:
        outcomes[run_test_case(*case)] += 1

    blocked = outcomes.get("blocked", 0)
    allowed = outcomes.get("allowed", 0)

    print("Suite Summary")
    print(f"   • {GREEN}Allowed:{RESET} {allowed}")
    print(f"   • {RED}Blocked:{RESET} {blocked}")
    print()
    return outcomes


# -------------------------------------------------------------------------
# Agent creation
# -------------------------------------------------------------------------
def build_agents() -> tuple[Agent, Agent]:
    """Create two agents to demonstrate different enforcement configurations."""

    # Full bidirectional enforcement: blocks input + output
    crypto_agent = Agent(
        name="Crypto-Sensitive Agent",
        role="Policy-Compliant Assistant",
        goal="Provide information while blocking cryptocurrency-related content.",
        instructions="Avoid discussing or providing information about cryptocurrencies.",
        user_policy=CryptoBlockPolicy,   # Filter incoming user text
        agent_policy=CryptoBlockPolicy,  # Filter outgoing model text
    )

    # Input-only enforcement: blocks crypto questions, allows open answers
    input_only_agent = Agent(
        name="Input-Only Policy Agent",
        role="Assistant that filters only user queries.",
        goal="Block crypto-related questions but allow other discussions.",
        instructions="Handle allowed questions normally; rely on user policy for filtering.",
        user_policy=CryptoBlockPolicy,
        agent_policy=None,
    )

    return crypto_agent, input_only_agent


# -------------------------------------------------------------------------
# Main execution
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("\nUpsonic Safety Engine — Crypto Block Policy Demo")
    print("=" * 70)
    print("Policy in use: CryptoBlockPolicy")
    print("   - Blocks all cryptocurrency-related content.")
    print("   - Can be applied to user inputs, agent outputs, or both.\n")

    crypto_agent, input_only_agent = build_agents()

    # Core tests for full policy enforcement
    core_cases = [
        (
            "Test 1: Asking about Bitcoin",
            "Can you tell me the current price of Bitcoin and the best wallet to use?",
            crypto_agent,
            True,
        ),
        (
            "Test 2: Ethereum explainer",
            "What are the benefits of Ethereum smart contracts?",
            crypto_agent,
            True,
        ),
        (
            "Test 3: Soft crypto mention",
            "Can you outline blockchain basics but skip cryptocurrencies or investing tips?",
            crypto_agent,
            True,
        ),
        (
            "Test 4: Neutral trivia",
            "What is the capital of France?",
            crypto_agent,
            False,
        ),
    ]

    run_suite("Full Enforcement (Input + Output)", core_cases)

    # Variant tests for input-only enforcement
    print("Now testing input-only policy configuration...\n")

    variant_cases = [
        (
            "Variant 1: Crypto question still blocked",
            "Should I invest in cryptocurrency right now?",
            input_only_agent,
            True,
        ),
        (
            "Variant 2: Non-crypto question flows normally",
            "Give me three productivity tips for remote teams.",
            input_only_agent,
            False,
        ),
    ]

    run_suite("Input-Only Enforcement Variant", variant_cases)
