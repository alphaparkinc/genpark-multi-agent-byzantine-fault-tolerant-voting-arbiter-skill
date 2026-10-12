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
