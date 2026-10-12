"""MCP Server for Multi-Agent Byzantine Fault Tolerant Voting Arbiter."""
import sys
import json
import time
from client import MultiAgentByzantineFaultTolerantVotingArbiter

arbiter = MultiAgentByzantineFaultTolerantVotingArbiter()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "arbitrate_bft_agent_quorum":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "arbitrate_bft_quorum")
    if action == "arbitrate_bft_quorum":
        return arbiter.arbitrate_bft_quorum(
            proposal_id=args.get("proposal_id", "PROP-001"),
            votes=args.get("votes", [])
        )
    elif action == "verify_quorum_certificate":
        return arbiter.verify_quorum_certificate(
            payload=args.get("payload", ""),
            signature=args.get("signature", "")
        )
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        votes = [
            {"agent_id": "verifier_1", "decision": "APPROVE_ESCROW_RELEASE", "confidence": 0.95, "reputation_weight": 1.0},
            {"agent_id": "verifier_2", "decision": "APPROVE_ESCROW_RELEASE", "confidence": 0.91, "reputation_weight": 1.0},
            {"agent_id": "verifier_3", "decision": "APPROVE_ESCROW_RELEASE", "confidence": 0.94, "reputation_weight": 1.0},
            {"agent_id": "hallucinating_node_4", "decision": "REJECT_FAKE_ERROR", "confidence": 0.60, "reputation_weight": 0.8}
        ]
        res = arbiter.arbitrate_bft_quorum("TX-ESCROW-889", votes)
        assert res["byzantine_fault_tolerance_f"] == 1
        assert res["quorum_reached"] is True
        assert res["winning_decision"] == "APPROVE_ESCROW_RELEASE"
        assert "hallucinating_node_4" in res["isolated_byzantine_outliers"]

        cert = res["quorum_certificate"]
        ver = arbiter.verify_quorum_certificate(cert["payload"], cert["hmac_sha256_signature"])
        assert ver["certificate_valid"] is True
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "MultiAgentByzantineFaultTolerantVotingArbiter", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "arbitrate_bft_agent_quorum",
                            "description": "Evaluate multi-agent votes under 3f+1 Byzantine Fault Tolerance, isolate hallucinating/adversarial agents, and issue a signed quorum certificate.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["arbitrate_bft_quorum", "verify_quorum_certificate"]},
                                    "proposal_id": {"type": "string"},
                                    "votes": {"type": "array"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
