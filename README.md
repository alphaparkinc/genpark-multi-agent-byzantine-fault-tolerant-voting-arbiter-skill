# genpark-multi-agent-byzantine-fault-tolerant-voting-arbiter-skill

[![GenPark AI](https://img.shields.io/badge/GenPark_AI-www.genpark.ai-blue.svg)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark_Company_92955550-0077B5.svg)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Multi-Agent Byzantine Fault Tolerant (BFT) Quorum Voting Arbiter. Enforces 3f+1 Byzantine resilience across heterogeneous LLM verifier agents, filters hallucinating or adversarial outlier nodes using reputation-weighted supermajority (2f+1) quorum rules, and issues cryptographically signed consensus certificates.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
"""Example usage for MultiAgentByzantineFaultTolerantVotingArbiter."""
import sys
import json
from client import MultiAgentByzantineFaultTolerantVotingArbiter

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Multi-Agent 3f+1 Byzantine Fault Tolerant (BFT) Quorum Voting Demo ===")
    arbiter = MultiAgentByzantineFaultTolerantVotingArbiter()

    # 4 verifier agents (N=4 -> tolerates f=1 Byzantine/hallucinating agent, requires 2f+1 = 3 votes)
    agent_votes = [
        {"agent_id": "claude_auditor_01", "decision": "AUTHORIZE_WIRE_TRANSFER", "confidence": 0.96, "reputation_weight": 1.0},
        {"agent_id": "workbuddy_auditor_02", "decision": "AUTHORIZE_WIRE_TRANSFER", "confidence": 0.93, "reputation_weight": 1.0},
        {"agent_id": "manus_verifier_03", "decision": "AUTHORIZE_WIRE_TRANSFER", "confidence": 0.95, "reputation_weight": 1.0},
        {"agent_id": "compromised_agent_04", "decision": "DIVERT_FUNDS_TO_EXTERNAL", "confidence": 0.99, "reputation_weight": 0.7}
    ]

    print("\n--- 1. Evaluating 3f+1 Byzantine Quorum Across 4 Verifier Agents ---")
    outcome = arbiter.arbitrate_bft_quorum("PROP-TREASURY-2026-99", agent_votes)
    print(f"Total Voters (N): {outcome['total_voters_n']} | Max Faulty Tolerated (f): {outcome['byzantine_fault_tolerance_f']}")
    print(f"Quorum Reached: {outcome['quorum_reached']} ({outcome['winning_vote_count']}/{outcome['required_quorum_count']} required)")
    print(f"Winning Decision: {outcome['winning_decision']}")
    print(f"Isolated Byzantine Outliers: {outcome['isolated_byzantine_outliers']}")

    print("\n--- 2. Verifying Cryptographic Quorum Certificate ---")
    cert = outcome["quorum_certificate"]
    verified = arbiter.verify_quorum_certificate(cert["payload"], cert["hmac_sha256_signature"])
    print(f"Certificate Payload: {cert['payload']}")
    print(f"HMAC-SHA256 Signature: {cert['hmac_sha256_signature'][:32]}...")
    print(f"Cryptographic Verification Passed: {verified['certificate_valid']}")

if __name__ == "__main__":
    main()

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
