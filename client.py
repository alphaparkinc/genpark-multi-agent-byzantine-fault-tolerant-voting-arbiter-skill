"""
Multi-Agent Byzantine Fault Tolerant (BFT) Voting Arbiter (Zero External Dependencies)
Implements 3f+1 Byzantine quorum calculation, outlier isolation, and SHA-256 quorum certification.
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import math
import hashlib
import hmac
import json
from typing import Dict, Any, List, Optional

class MultiAgentByzantineFaultTolerantVotingArbiter:
    def __init__(self, cluster_secret: str = "genpark_bft_quorum_secret_2026"):
        self.secret = cluster_secret

    def arbitrate_bft_quorum(
        self,
        proposal_id: str,
        votes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluates N agent votes under BFT theorem:
        Max tolerated faulty/hallucinating nodes: f = floor((N - 1) / 3)
        Required supermajority quorum size: Q = 2*f + 1 (or ceil(2*N / 3))
        """
        n = len(votes)
        if n == 0:
            return {"error": "No votes submitted"}

        max_faulty_f = max(0, (n - 1) // 3)
        required_quorum = (2 * max_faulty_f) + 1 if n >= 4 else math.ceil((2 * n) / 3)

        decision_buckets: Dict[str, Dict[str, Any]] = {}
        total_weight = 0.0

        for v in votes:
            agent_id = v.get("agent_id", "unknown")
            decision = str(v.get("decision", "ABSTAIN")).strip().upper()
            conf = float(v.get("confidence", 0.8))
            rep = float(v.get("reputation_weight", 1.0))
            effective_weight = round(conf * rep, 3)
            total_weight += effective_weight

            if decision not in decision_buckets:
                decision_buckets[decision] = {"count": 0, "weighted_score": 0.0, "voters": []}
            decision_buckets[decision]["count"] += 1
            decision_buckets[decision]["weighted_score"] += effective_weight
            decision_buckets[decision]["voters"].append(agent_id)

        # Find leading decision
        ranked = sorted(decision_buckets.items(), key=lambda item: (item[1]["count"], item[1]["weighted_score"]), reverse=True)
        top_decision, top_stats = ranked[0]

        quorum_reached = top_stats["count"] >= required_quorum

        # Identify Byzantine / outlier dissenting voters
        outlier_agents = []
        for dec, stats in ranked[1:]:
            outlier_agents.extend(stats["voters"])

        now = time.time()
        cert_payload = f"{proposal_id}:{top_decision}:{top_stats['count']}/{n}:{quorum_reached}"
        signature = hmac.new(self.secret.encode("utf-8"), cert_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        return {
            "proposal_id": proposal_id,
            "total_voters_n": n,
            "byzantine_fault_tolerance_f": max_faulty_f,
            "required_quorum_count": required_quorum,
            "quorum_reached": quorum_reached,
            "winning_decision": top_decision if quorum_reached else "UNRESOLVED_NO_QUORUM",
            "winning_vote_count": top_stats["count"],
            "weighted_agreement_ratio": round(top_stats["weighted_score"] / max(0.01, total_weight), 3),
            "isolated_byzantine_outliers": outlier_agents,
            "quorum_certificate": {
                "payload": cert_payload,
                "hmac_sha256_signature": signature,
                "issued_at": now
            }
        }

    def verify_quorum_certificate(self, payload: str, signature: str) -> Dict[str, Any]:
        """Verifies cryptographic authenticity of a BFT quorum certificate."""
        expected = hmac.new(self.secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
        valid = hmac.compare_digest(expected, signature)
        return {"certificate_valid": valid, "payload": payload}
